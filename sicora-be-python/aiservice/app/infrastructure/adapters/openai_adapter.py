"""OpenAI adapter implementation."""

import asyncio
from typing import List, Dict, Any, Optional, AsyncIterator
import openai
from openai import AsyncOpenAI

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


class OpenAIAdapter(AIProviderInterface):
    """OpenAI service adapter implementation."""
    
    def __init__(self, api_key: str, organization: Optional[str] = None):
        """Initialize OpenAI adapter."""
        self.client = AsyncOpenAI(
            api_key=api_key,
            organization=organization
        )
    
    async def generate_response(
        self,
        messages: List[Message],
        model: AIModel,
        **kwargs
    ) -> Message:
        """Generate a response using OpenAI models."""
        try:
            openai_messages = self._convert_messages_to_openai(messages)
            
            response = await self.client.chat.completions.create(
                model=model.model_name,
                messages=openai_messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000),
                top_p=kwargs.get('top_p', 1.0),
                frequency_penalty=kwargs.get('frequency_penalty', 0.0),
                presence_penalty=kwargs.get('presence_penalty', 0.0)
            )
            
            content = response.choices[0].message.content
            return Message(
                content=content,
                message_type=MessageType.ASSISTANT,
                metadata={
                    'model': model.model_name,
                    'usage': response.usage.model_dump() if response.usage else {},
                    'finish_reason': response.choices[0].finish_reason
                }
            )
            
        except openai.RateLimitError as e:
            raise RateLimitError(f"OpenAI rate limit exceeded: {str(e)}")
        except openai.BadRequestError as e:
            raise InvalidInputError(f"Invalid request to OpenAI: {str(e)}")
        except openai.NotFoundError as e:
            raise ModelNotFoundError(f"Model not found: {str(e)}")
        except Exception as e:
            raise AIProviderError(f"OpenAI API error: {str(e)}")
    
    async def generate_streaming_response(
        self,
        messages: List[Message],
        model: AIModel,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate a streaming response using OpenAI models."""
        try:
            openai_messages = self._convert_messages_to_openai(messages)
            
            stream = await self.client.chat.completions.create(
                model=model.model_name,
                messages=openai_messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000),
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except openai.RateLimitError as e:
            raise RateLimitError(f"OpenAI rate limit exceeded: {str(e)}")
        except Exception as e:
            raise AIProviderError(f"OpenAI streaming error: {str(e)}")
    
    async def generate_completion(
        self,
        prompt: AIPrompt,
        model: AIModel,
        **kwargs
    ) -> str:
        """Generate a text completion using OpenAI."""
        try:
            messages = [{"role": "user", "content": prompt.content}]
            
            response = await self.client.chat.completions.create(
                model=model.model_name,
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise AIProviderError(f"OpenAI completion error: {str(e)}")
    
    async def generate_embedding(
        self,
        text: str,
        model_name: Optional[str] = None
    ) -> List[float]:
        """Generate text embedding using OpenAI."""
        try:
            model = model_name or "text-embedding-3-small"
            
            response = await self.client.embeddings.create(
                model=model,
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            raise AIProviderError(f"OpenAI embedding error: {str(e)}")
    
    async def analyze_sentiment(
        self,
        text: str,
        model: Optional[AIModel] = None
    ) -> Dict[str, Any]:
        """Analyze text sentiment using OpenAI."""
        try:
            model_name = model.model_name if model else "gpt-3.5-turbo"
            
            messages = [{
                "role": "user",
                "content": f"""Analyze the sentiment of the following text and return a JSON response with:
                - sentiment: positive, negative, or neutral
                - confidence: a score between 0 and 1
                - emotions: list of detected emotions

                Text: {text}

                Respond only with valid JSON."""
            }]
            
            response = await self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.1
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise AIProviderError(f"OpenAI sentiment analysis error: {str(e)}")
    
    async def summarize_text(
        self,
        text: str,
        model: AIModel,
        max_length: Optional[int] = None
    ) -> str:
        """Summarize text content using OpenAI."""
        try:
            max_words = max_length or 100
            
            messages = [{
                "role": "user",
                "content": f"Summarize the following text in no more than {max_words} words:\n\n{text}"
            }]
            
            response = await self.client.chat.completions.create(
                model=model.model_name,
                messages=messages,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise AIProviderError(f"OpenAI summarization error: {str(e)}")
    
    async def extract_keywords(
        self,
        text: str,
        model: Optional[AIModel] = None,
        max_keywords: int = 10
    ) -> List[str]:
        """Extract keywords from text using OpenAI."""
        try:
            model_name = model.model_name if model else "gpt-3.5-turbo"
            
            messages = [{
                "role": "user",
                "content": f"""Extract up to {max_keywords} relevant keywords from the following text.
                Return only a JSON array of keywords.

                Text: {text}

                Respond only with a valid JSON array."""
            }]
            
            response = await self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.1
            )
            
            import json
            keywords = json.loads(response.choices[0].message.content)
            return keywords if isinstance(keywords, list) else []
            
        except Exception as e:
            raise AIProviderError(f"OpenAI keyword extraction error: {str(e)}")
    
    async def classify_content(
        self,
        text: str,
        categories: List[str],
        model: Optional[AIModel] = None
    ) -> Dict[str, float]:
        """Classify text content into categories using OpenAI."""
        try:
            model_name = model.model_name if model else "gpt-3.5-turbo"
            categories_str = ", ".join(categories)
            
            messages = [{
                "role": "user",
                "content": f"""Classify the following text into these categories: {categories_str}
                Return a JSON object with category names as keys and confidence scores (0-1) as values.

                Text: {text}

                Respond only with valid JSON."""
            }]
            
            response = await self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.1
            )
            
            import json
            classification = json.loads(response.choices[0].message.content)
            return classification if isinstance(classification, dict) else {}
            
        except Exception as e:
            raise AIProviderError(f"OpenAI classification error: {str(e)}")
    
    async def check_model_availability(self, model: AIModel) -> bool:
        """Check if an OpenAI model is available."""
        try:
            models = await self.client.models.list()
            available_models = [m.id for m in models.data]
            return model.model_name in available_models
            
        except Exception:
            return False
    
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about an OpenAI model."""
        try:
            model = await self.client.models.retrieve(model_name)
            return model.model_dump()
            
        except Exception as e:
            raise ModelNotFoundError(f"Model {model_name} not found: {str(e)}")
    
    async def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens in text for OpenAI models."""
        try:
            import tiktoken
            
            encoding = tiktoken.encoding_for_model(model_name)
            tokens = encoding.encode(text)
            return len(tokens)
            
        except Exception:
            return len(text.split())
    
    def _convert_messages_to_openai(self, messages: List[Message]) -> List[Dict[str, str]]:
        """Convert internal Message objects to OpenAI format."""
        openai_messages = []
        
        for message in messages:
            role = "user" if message.message_type == MessageType.USER else "assistant"
            if message.message_type == MessageType.SYSTEM:
                role = "system"
                
            openai_messages.append({
                "role": role,
                "content": message.content
            })
        
        return openai_messages
