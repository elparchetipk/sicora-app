"""Conversation metadata value object."""

from datetime import datetime
from typing import Dict, Any, Optional


class ConversationMetadata:
    """Value object for conversation metadata."""
    
    def __init__(
        self,
        message_count: int = 0,
        total_tokens: int = 0,
        model_usage: Optional[Dict[str, int]] = None,
        tags: Optional[list] = None,
        language: str = "es",
        topic: Optional[str] = None,
        sentiment: Optional[str] = None,
        last_activity: Optional[datetime] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ):
        self.message_count = message_count
        self.total_tokens = total_tokens
        self.model_usage = model_usage or {}
        self.tags = tags or []
        self.language = language
        self.topic = topic
        self.sentiment = sentiment
        self.last_activity = last_activity
        self.custom_fields = custom_fields or {}
    
    def increment_message_count(self) -> None:
        """Increment the message count."""
        self.message_count += 1
        self.last_activity = datetime.utcnow()
    
    def add_tokens(self, token_count: int) -> None:
        """Add tokens to the total count."""
        self.total_tokens += token_count
    
    def record_model_usage(self, model_name: str, token_count: int = 1) -> None:
        """Record usage of a specific model."""
        if model_name not in self.model_usage:
            self.model_usage[model_name] = 0
        self.model_usage[model_name] += token_count
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the conversation."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the conversation."""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def set_topic(self, topic: str) -> None:
        """Set the conversation topic."""
        self.topic = topic
    
    def set_sentiment(self, sentiment: str) -> None:
        """Set the conversation sentiment."""
        self.sentiment = sentiment
    
    def set_language(self, language: str) -> None:
        """Set the conversation language."""
        self.language = language
    
    def add_custom_field(self, key: str, value: Any) -> None:
        """Add a custom field to metadata."""
        self.custom_fields[key] = value
    
    def get_most_used_model(self) -> Optional[str]:
        """Get the most used model in this conversation."""
        if not self.model_usage:
            return None
        return max(self.model_usage.items(), key=lambda x: x[1])[0]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "message_count": self.message_count,
            "total_tokens": self.total_tokens,
            "model_usage": self.model_usage,
            "tags": self.tags,
            "language": self.language,
            "topic": self.topic,
            "sentiment": self.sentiment,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "custom_fields": self.custom_fields,
            "most_used_model": self.get_most_used_model()
        }
    
    def __str__(self) -> str:
        return f"ConversationMetadata(messages={self.message_count}, tokens={self.total_tokens}, language='{self.language}')"
    
    def __repr__(self) -> str:
        return self.__str__()
