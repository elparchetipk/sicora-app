"""Hugging Face Transformers adapter implementation."""

from typing import List, Dict, Any, Optional, AsyncIterator
import asyncio
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
from sentence_transformers import SentenceTransformer

from app.application.interfaces.ai_provider_interface import AIProviderInterface
from app.domain.value_objects.message import Message, MessageType
from app.domain.value_objects.ai_prompt import AIPrompt
from app.domain.entities.ai_model import AIModel
from app.domain.exceptions.ai_exceptions import (
    AIProviderError,
    ModelNotFoundError,
    InvalidInputError
)


class HuggingFaceAdapter(AIProviderInterface):
    """Hugging Face Transformers adapter for local AI models."""
    
    def __init__(self, device: str = "auto"):
        """Initialize Hugging Face adapter."""
        self.device = device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
        self.loaded_models = {}
        self.tokenizers = {}
        self.embedding_models = {}
    
    def _get_or_load_pipeline(self, model_name: str, task: str = "text-generation"):
        """Get or load a Hugging Face pipeline."""
        cache_key = f"{model_name}_{task}"
        
        if cache_key not in self.loaded_models:
            try:
                self.loaded_models[cache_key] = pipeline(
                    task,
                    model=model_name,
                    device=0 if self.device == "cuda" else -1,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
            except Exception as e:
                raise ModelNotFoundError(f"Failed to load model {model_name}: {str(e)}")
        
        return self.loaded_models[cache_key]
    
    def _get_or_load_tokenizer(self, model_name: str):
        """Get or load a tokenizer."""
        if model_name not in self.tokenizers:
            try:
                self.tokenizers[model_name] = AutoTokenizer.from_pretrained(model_name)
            except Exception as e:
                raise ModelNotFoundError(f"Failed to load tokenizer for {model_name}: {str(e)}")
        
        return self.tokenizers[model_name]
    
    def _get_or_load_embedding_model(self, model_name: str):
        """Get or load a sentence transformer model for embeddings."""
        if model_name not in self.embedding_models:
            try:
                self.embedding_models[model_name] = SentenceTransformer(model_name, device=self.device)
            except Exception as e:
                raise ModelNotFoundError(f"Failed to load embedding model {model_name}: {str(e)}")
        
        return self.embedding_models[model_name]
    
    async def generate_response(
        self,
        messages: List[Message],
        model: AIModel,
        **kwargs
    ) -> Message:
        """Generate a response using Hugging Face models."""
        try:
            # Convert messages to prompt
            prompt = self._convert_messages_to_prompt(messages)
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._generate_text,
                prompt,
                model.model_name,
                kwargs
            )
            
            return Message(
                content=response,
                message_type=MessageType.ASSISTANT,
                metadata={
                    'model': model.model_name,
                    'device': self.device
                }
            )
            
        except Exception as e:
            raise AIProviderError(f"Hugging Face generation error: {str(e)}")
    
    def _generate_text(self, prompt: str, model_name: str, kwargs: dict) -> str:
        """Generate text using the model (blocking)."""
        generator = self._get_or_load_pipeline(model_name, "text-generation")
        
        result = generator(
            prompt,
            max_length=kwargs.get('max_tokens', 100) + len(prompt.split()),
            temperature=kwargs.get('temperature', 0.7),
            do_sample=True,
            num_return_sequences=1,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        
        generated_text = result[0]['generated_text']
        # Remove the original prompt from the response
        response = generated_text[len(prompt):].strip()
        return response
    
    async def generate_streaming_response(
        self,
        messages: List[Message],
        model: AIModel,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate a streaming response (simulated for HF models)."""
        try:
            # HF models don't support true streaming, so we simulate it
            prompt = self._convert_messages_to_prompt(messages)
            
            loop = asyncio.get_event_loop()
            full_response = await loop.run_in_executor(
                None,
                self._generate_text,
                prompt,
                model.model_name,
                kwargs
            )
            
            # Simulate streaming by yielding chunks
            words = full_response.split()
            for i, word in enumerate(words):
                yield word + (" " if i < len(words) - 1 else "")
                await asyncio.sleep(0.05)  # Small delay to simulate streaming
                
        except Exception as e:
            raise AIProviderError(f"Hugging Face streaming error: {str(e)}")
    
    async def generate_completion(
        self,
        prompt: AIPrompt,
        model: AIModel,
        **kwargs
    ) -> str:
        """Generate a text completion using Hugging Face models."""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._generate_text,
                prompt.content,
                model.model_name,
                kwargs
            )
            return response
            
        except Exception as e:
            raise AIProviderError(f"Hugging Face completion error: {str(e)}")
    
    async def generate_embedding(
        self,
        text: str,
        model_name: Optional[str] = None
    ) -> List[float]:
        """Generate text embedding using Sentence Transformers."""
        try:
            embedding_model_name = model_name or "all-MiniLM-L6-v2"
            
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None,
                self._compute_embedding,
                text,
                embedding_model_name
            )
            
            return embedding.tolist()
            
        except Exception as e:
            raise AIProviderError(f"Hugging Face embedding error: {str(e)}")
    
    def _compute_embedding(self, text: str, model_name: str):
        """Compute embedding (blocking)."""
        model = self._get_or_load_embedding_model(model_name)
        return model.encode(text)
    
    async def analyze_sentiment(
        self,
        text: str,
        model: Optional[AIModel] = None
    ) -> Dict[str, Any]:
        """Analyze text sentiment using Hugging Face models."""
        try:
            model_name = model.model_name if model else "cardiffnlp/twitter-roberta-base-sentiment-latest"
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._analyze_sentiment_blocking,
                text,
                model_name
            )
            
            return result
            
        except Exception as e:
            raise AIProviderError(f"Hugging Face sentiment analysis error: {str(e)}")
    
    def _analyze_sentiment_blocking(self, text: str, model_name: str) -> Dict[str, Any]:
        """Analyze sentiment (blocking)."""
        classifier = self._get_or_load_pipeline(model_name, "sentiment-analysis")
        result = classifier(text)[0]
        
        return {
            "sentiment": result["label"].lower(),
            "confidence": result["score"],
            "emotions": [result["label"]]
        }
    
    async def summarize_text(
        self,
        text: str,
        model: AIModel,
        max_length: Optional[int] = None
    ) -> str:
        """Summarize text content using Hugging Face models."""
        try:
            max_len = max_length or 100
            
            loop = asyncio.get_event_loop()
            summary = await loop.run_in_executor(
                None,
                self._summarize_blocking,
                text,
                model.model_name,
                max_len
            )
            
            return summary
            
        except Exception as e:
            raise AIProviderError(f"Hugging Face summarization error: {str(e)}")
    
    def _summarize_blocking(self, text: str, model_name: str, max_length: int) -> str:
        """Summarize text (blocking)."""
        summarizer = self._get_or_load_pipeline(model_name, "summarization")
        
        # Calculate appropriate max_length based on input
        input_length = len(text.split())
        max_len = min(max_length, input_length // 2)
        min_len = max(10, max_len // 4)
        
        result = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )
        
        return result[0]['summary_text']
    
    async def extract_keywords(
        self,
        text: str,
        model: Optional[AIModel] = None,
        max_keywords: int = 10
    ) -> List[str]:
        """Extract keywords from text using NER models."""
        try:
            model_name = model.model_name if model else "dbmdz/bert-large-cased-finetuned-conll03-english"
            
            loop = asyncio.get_event_loop()
            keywords = await loop.run_in_executor(
                None,
                self._extract_keywords_blocking,
                text,
                model_name,
                max_keywords
            )
            
            return keywords
            
        except Exception as e:
            raise AIProviderError(f"Hugging Face keyword extraction error: {str(e)}")
    
    def _extract_keywords_blocking(self, text: str, model_name: str, max_keywords: int) -> List[str]:
        """Extract keywords using NER (blocking)."""
        ner = self._get_or_load_pipeline(model_name, "ner")
        entities = ner(text)
        
        # Extract unique entity words
        keywords = set()
        for entity in entities:
            if entity['score'] > 0.8:  # High confidence entities
                keywords.add(entity['word'].replace('##', ''))
        
        return list(keywords)[:max_keywords]
    
    async def classify_content(
        self,
        text: str,
        categories: List[str],
        model: Optional[AIModel] = None
    ) -> Dict[str, float]:
        """Classify text content into categories."""
        try:
            model_name = model.model_name if model else "facebook/bart-large-mnli"
            
            loop = asyncio.get_event_loop()
            classification = await loop.run_in_executor(
                None,
                self._classify_content_blocking,
                text,
                categories,
                model_name
            )
            
            return classification
            
        except Exception as e:
            raise AIProviderError(f"Hugging Face classification error: {str(e)}")
    
    def _classify_content_blocking(self, text: str, categories: List[str], model_name: str) -> Dict[str, float]:
        """Classify content (blocking)."""
        classifier = self._get_or_load_pipeline(model_name, "zero-shot-classification")
        
        result = classifier(text, categories)
        
        classification = {}
        for label, score in zip(result['labels'], result['scores']):
            classification[label] = score
        
        return classification
    
    async def check_model_availability(self, model: AIModel) -> bool:
        """Check if a Hugging Face model is available."""
        try:
            from huggingface_hub import model_info
            model_info(model.model_name)
            return True
        except Exception:
            return False
    
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a Hugging Face model."""
        try:
            from huggingface_hub import model_info
            info = model_info(model_name)
            
            return {
                "name": model_name,
                "downloads": getattr(info, 'downloads', 0),
                "likes": getattr(info, 'likes', 0),
                "tags": getattr(info, 'tags', []),
                "pipeline_tag": getattr(info, 'pipeline_tag', None),
                "library_name": getattr(info, 'library_name', None)
            }
            
        except Exception as e:
            raise ModelNotFoundError(f"Model {model_name} not found: {str(e)}")
    
    async def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens in text for Hugging Face models."""
        try:
            tokenizer = self._get_or_load_tokenizer(model_name)
            tokens = tokenizer.encode(text)
            return len(tokens)
            
        except Exception:
            # Fallback to word count
            return len(text.split())
    
    def _convert_messages_to_prompt(self, messages: List[Message]) -> str:
        """Convert messages to a single prompt string."""
        prompt_parts = []
        
        for message in messages:
            if message.message_type == MessageType.SYSTEM:
                prompt_parts.append(f"System: {message.content}")
            elif message.message_type == MessageType.USER:
                prompt_parts.append(f"User: {message.content}")
            elif message.message_type == MessageType.ASSISTANT:
                prompt_parts.append(f"Assistant: {message.content}")
        
        prompt_parts.append("Assistant: ")
        return "\n".join(prompt_parts)
