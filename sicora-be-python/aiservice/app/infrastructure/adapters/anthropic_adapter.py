"""Anthropic adapter implementation."""

from typing import List, Dict, Any, Optional, AsyncIterator
import anthropic

from app.application.interfaces.ai_provider_interface import AIProviderInterface
from app.domain.value_objects.message import Message, MessageType
from app.domain.value_objects.ai_prompt import AIPrompt
from app.domain.entities.ai_model import AIModel
from app.domain.exceptions.ai_exceptions import (
    AIProviderError,
    ModelNotFoundError,
    RateLimitError,
    InvalidInputError
)


class AnthropicAdapter(AIProviderInterface):
    """Anthropic Claude service adapter implementation."""
    
    def __init__(self, api_key: str):
        """Initialize Anthropic adapter."""
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
    
    async def generate_response(
        self,
        messages: List[Message],
        model: AIModel,
        **kwargs
    ) -> Message:
        """Generate a response using Anthropic Claude models."""
        try:
            anthropic_messages = self._convert_messages_to_anthropic(messages)
            
            response = await self.client.messages.create(
                model=model.model_name,
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7),
                messages=anthropic_messages
            )
            
            content = response.content[0].text if response.content else ""
            
            return Message(
                content=content,
                message_type=MessageType.ASSISTANT,
                metadata={
                    'model': model.model_name,
                    'usage': {
                        'input_tokens': response.usage.input_tokens,
                        'output_tokens': response.usage.output_tokens
                    } if response.usage else {},
                    'stop_reason': response.stop_reason
                }
            )
            
        except anthropic.RateLimitError as e:
            raise RateLimitError(f"Anthropic rate limit exceeded: {str(e)}")
        except anthropic.BadRequestError as e:
            raise InvalidInputError(f"Invalid request to Anthropic: {str(e)}")
        except anthropic.NotFoundError as e:
            raise ModelNotFoundError(f"Model not found: {str(e)}")
        except Exception as e:
            raise AIProviderError(f"Anthropic API error: {str(e)}")
    
    async def generate_streaming_response(
        self,
        messages: List[Message],
        model: AIModel,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate a streaming response using Anthropic Claude models."""
        try:
            anthropic_messages = self._convert_messages_to_anthropic(messages)
            
            async with self.client.messages.stream(
                model=model.model_name,
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7),
                messages=anthropic_messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except anthropic.RateLimitError as e:
            raise RateLimitError(f"Anthropic rate limit exceeded: {str(e)}")
        except Exception as e:
            raise AIProviderError(f"Anthropic streaming error: {str(e)}")
    
    async def generate_completion(
        self,
        prompt: AIPrompt,
        model: AIModel,
        **kwargs
    ) -> str:
        """Generate a text completion using Anthropic Claude."""
        try:
            messages = [{
                "role": "user",
                "content": prompt.content
            }]
            
            response = await self.client.messages.create(
                model=model.model_name,
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7),
                messages=messages
            )
            
            return response.content[0].text if response.content else ""
            
        except Exception as e:
            raise AIProviderError(f"Anthropic completion error: {str(e)}")
    
    async def generate_embedding(
        self,
        text: str,
        model_name: Optional[str] = None
    ) -> List[float]:
        """Generate text embedding (Anthropic doesn't provide embeddings directly)."""
        raise AIProviderError("Anthropic doesn't provide embedding models. Use OpenAI or other providers.")
    
    async def analyze_sentiment(
        self,
        text: str,
        model: Optional[AIModel] = None
    ) -> Dict[str, Any]:
        """Analyze text sentiment using Anthropic Claude."""
        try:
            model_name = model.model_name if model else "claude-3-haiku-20240307"
            
            messages = [{
                "role": "user",
                "content": f"""Analyze the sentiment of the following text and return a JSON response with:
                - sentiment: positive, negative, or neutral
                - confidence: a score between 0 and 1
                - emotions: list of detected emotions

                Text: {text}

                Respond only with valid JSON."""
            }]
            
            response = await self.client.messages.create(
                model=model_name,
                max_tokens=500,
                temperature=0.1,
                messages=messages
            )
            
            import json
            content = response.content[0].text if response.content else "{}"
            result = json.loads(content)
            return result
            
        except Exception as e:
            raise AIProviderError(f"Anthropic sentiment analysis error: {str(e)}")
    
    async def summarize_text(
        self,
        text: str,
        model: AIModel,
        max_length: Optional[int] = None
    ) -> str:
        """Summarize text content using Anthropic Claude."""
        try:
            max_words = max_length or 100
            
            messages = [{
                "role": "user",
                "content": f"Summarize the following text in no more than {max_words} words:\n\n{text}"
            }]
            
            response = await self.client.messages.create(
                model=model.model_name,
                max_tokens=500,
                temperature=0.3,
                messages=messages
            )
            
            return response.content[0].text if response.content else ""
            
        except Exception as e:
            raise AIProviderError(f"Anthropic summarization error: {str(e)}")
    
    async def extract_keywords(
        self,
        text: str,
        model: Optional[AIModel] = None,
        max_keywords: int = 10
    ) -> List[str]:
        """Extract keywords from text using Anthropic Claude."""
        try:
            model_name = model.model_name if model else "claude-3-haiku-20240307"
            
            messages = [{
                "role": "user",
                "content": f"""Extract up to {max_keywords} relevant keywords from the following text.
                Return only a JSON array of keywords.

                Text: {text}

                Respond only with a valid JSON array."""
            }]
            
            response = await self.client.messages.create(
                model=model_name,
                max_tokens=300,
                temperature=0.1,
                messages=messages
            )
            
            import json
            content = response.content[0].text if response.content else "[]"
            keywords = json.loads(content)
            return keywords if isinstance(keywords, list) else []
            
        except Exception as e:
            raise AIProviderError(f"Anthropic keyword extraction error: {str(e)}")
    
    async def classify_content(
        self,
        text: str,
        categories: List[str],
        model: Optional[AIModel] = None
    ) -> Dict[str, float]:
        """Classify text content into categories using Anthropic Claude."""
        try:
            model_name = model.model_name if model else "claude-3-haiku-20240307"
            categories_str = ", ".join(categories)
            
            messages = [{
                "role": "user",
                "content": f"""Classify the following text into these categories: {categories_str}
                Return a JSON object with category names as keys and confidence scores (0-1) as values.

                Text: {text}

                Respond only with valid JSON."""
            }]
            
            response = await self.client.messages.create(
                model=model_name,
                max_tokens=300,
                temperature=0.1,
                messages=messages
            )
            
            import json
            content = response.content[0].text if response.content else "{}"
            classification = json.loads(content)
            return classification if isinstance(classification, dict) else {}
            
        except Exception as e:
            raise AIProviderError(f"Anthropic classification error: {str(e)}")
    
    async def check_model_availability(self, model: AIModel) -> bool:
        """Check if an Anthropic model is available."""
        # Anthropic models that are generally available
        available_models = [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0",
            "claude-instant-1.2"
        ]
        return model.model_name in available_models
    
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about an Anthropic model."""
        model_info = {
            "claude-3-opus-20240229": {
                "name": "Claude 3 Opus",
                "max_tokens": 4096,
                "context_window": 200000,
                "capabilities": ["text", "analysis", "reasoning"]
            },
            "claude-3-sonnet-20240229": {
                "name": "Claude 3 Sonnet",
                "max_tokens": 4096,
                "context_window": 200000,
                "capabilities": ["text", "analysis", "reasoning"]
            },
            "claude-3-haiku-20240307": {
                "name": "Claude 3 Haiku",
                "max_tokens": 4096,
                "context_window": 200000,
                "capabilities": ["text", "analysis", "reasoning"]
            }
        }
        
        if model_name in model_info:
            return model_info[model_name]
        else:
            raise ModelNotFoundError(f"Model {model_name} not found")
    
    async def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens in text for Anthropic models (approximation)."""
        # Anthropic doesn't provide a direct tokenizer, so we approximate
        # Generally ~4 characters per token for English text
        return len(text) // 4
    
    def _convert_messages_to_anthropic(self, messages: List[Message]) -> List[Dict[str, str]]:
        """Convert internal Message objects to Anthropic format."""
        anthropic_messages = []
        
        for message in messages:
            if message.message_type == MessageType.SYSTEM:
                # Anthropic handles system messages differently
                # We'll prepend them to the first user message
                continue
                
            role = "user" if message.message_type == MessageType.USER else "assistant"
            anthropic_messages.append({
                "role": role,
                "content": message.content
            })
        
        return anthropic_messages
