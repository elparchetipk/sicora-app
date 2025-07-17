"""Analytics use cases for AI Service."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from uuid import UUID

from app.domain.repositories.conversation_repository import ConversationRepository
from app.domain.repositories.ai_model_repository import AIModelRepository
from app.domain.repositories.knowledge_repository import KnowledgeRepository
from app.application.interfaces.cache_interface import CacheInterface
from app.application.dtos.ai_dtos import AnalyticsRequestDTO, AnalyticsResponseDTO

logger = logging.getLogger(__name__)


class AnalyticsUseCase:
    """Use case for analytics and reporting."""
    
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        ai_model_repo: AIModelRepository,
        knowledge_repo: KnowledgeRepository,
        cache: CacheInterface
    ):
        self.conversation_repo = conversation_repo
        self.ai_model_repo = ai_model_repo
        self.knowledge_repo = knowledge_repo
        self.cache = cache
    
    async def get_analytics(self, request: AnalyticsRequestDTO) -> AnalyticsResponseDTO:
        """Get analytics data based on request parameters."""
        try:
            # Set default date range if not provided
            end_date = request.end_date or datetime.utcnow()
            start_date = request.start_date or (end_date - timedelta(days=30))
            
            # Check cache for recent analytics
            cache_key = f"analytics:{request.user_id}:{start_date.date()}:{end_date.date()}"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return AnalyticsResponseDTO(**cached_result)
            
            # Gather analytics data
            analytics_data = await self._gather_analytics_data(
                user_id=request.user_id,
                start_date=start_date,
                end_date=end_date,
                metric_types=request.metric_types or []
            )
            
            response = AnalyticsResponseDTO(
                total_conversations=analytics_data["total_conversations"],
                total_messages=analytics_data["total_messages"],
                total_tokens=analytics_data["total_tokens"],
                avg_response_time=analytics_data["avg_response_time"],
                most_used_models=analytics_data["most_used_models"],
                user_activity=analytics_data["user_activity"],
                time_period={
                    "start_date": start_date,
                    "end_date": end_date
                },
                detailed_metrics=analytics_data.get("detailed_metrics")
            )
            
            # Cache result for 30 minutes
            await self.cache.set(
                cache_key,
                response.model_dump(),
                expire=timedelta(minutes=30)
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating analytics: {str(e)}", exc_info=True)
            # Return empty analytics on error
            return AnalyticsResponseDTO(
                total_conversations=0,
                total_messages=0,
                total_tokens=0,
                avg_response_time=0.0,
                most_used_models={},
                user_activity={},
                time_period={
                    "start_date": request.start_date or datetime.utcnow() - timedelta(days=30),
                    "end_date": request.end_date or datetime.utcnow()
                }
            )
    
    async def get_system_analytics(self) -> Dict[str, Any]:
        """Get system-wide analytics."""
        try:
            # Check cache
            cached_result = await self.cache.get("system_analytics")
            if cached_result:
                return cached_result
            
            # Get model statistics
            model_stats = await self.ai_model_repo.get_model_statistics()
            
            # Get knowledge base statistics
            knowledge_stats = await self.knowledge_repo.get_statistics()
            
            # Calculate system metrics
            now = datetime.utcnow()
            last_24h = now - timedelta(hours=24)
            last_7d = now - timedelta(days=7)
            
            system_analytics = {
                "models": {
                    "total_models": len(await self.ai_model_repo.get_active_models()),
                    "available_models": len(await self.ai_model_repo.get_available_models()),
                    "model_statistics": model_stats
                },
                "knowledge_base": knowledge_stats,
                "system_health": {
                    "uptime_start": now.isoformat(),
                    "last_updated": now.isoformat()
                },
                "performance_metrics": await self._get_performance_metrics()
            }
            
            # Cache for 15 minutes
            await self.cache.set(
                "system_analytics",
                system_analytics,
                expire=timedelta(minutes=15)
            )
            
            return system_analytics
            
        except Exception as e:
            logger.error(f"Error getting system analytics: {str(e)}", exc_info=True)
            return {
                "error": "Failed to generate system analytics",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_user_analytics(self, user_id: UUID, days: int = 30) -> Dict[str, Any]:
        """Get analytics for a specific user."""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get user's conversations
            conversations = await self.conversation_repo.get_by_user_id(
                user_id=user_id,
                limit=1000  # Get all conversations in period
            )
            
            # Filter by date range
            filtered_conversations = [
                conv for conv in conversations
                if start_date <= conv.created_at <= end_date
            ]
            
            # Calculate user metrics
            total_conversations = len(filtered_conversations)
            total_messages = sum(conv.get_messages_count() for conv in filtered_conversations)
            total_tokens = sum(conv.get_total_tokens() for conv in filtered_conversations)
            
            # Activity patterns
            daily_activity = {}
            for conv in filtered_conversations:
                date_key = conv.created_at.date().isoformat()
                daily_activity[date_key] = daily_activity.get(date_key, 0) + 1
            
            # Model usage
            model_usage = {}
            for conv in filtered_conversations:
                most_used_model = conv.metadata.get_most_used_model()
                if most_used_model:
                    model_usage[most_used_model] = model_usage.get(most_used_model, 0) + 1
            
            return {
                "user_id": str(user_id),
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "metrics": {
                    "total_conversations": total_conversations,
                    "total_messages": total_messages,
                    "total_tokens": total_tokens,
                    "avg_messages_per_conversation": total_messages / max(total_conversations, 1),
                    "avg_tokens_per_message": total_tokens / max(total_messages, 1)
                },
                "activity_patterns": {
                    "daily_activity": daily_activity,
                    "most_active_day": max(daily_activity.items(), key=lambda x: x[1])[0] if daily_activity else None,
                    "total_active_days": len(daily_activity)
                },
                "model_usage": model_usage,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting user analytics: {str(e)}", exc_info=True)
            return {
                "user_id": str(user_id),
                "error": "Failed to generate user analytics",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _gather_analytics_data(
        self,
        user_id: Optional[UUID],
        start_date: datetime,
        end_date: datetime,
        metric_types: List[str]
    ) -> Dict[str, Any]:
        """Gather analytics data from repositories."""
        data = {
            "total_conversations": 0,
            "total_messages": 0,
            "total_tokens": 0,
            "avg_response_time": 0.0,
            "most_used_models": {},
            "user_activity": {}
        }
        
        try:
            # Get conversations
            if user_id:
                conversations = await self.conversation_repo.get_by_user_id(
                    user_id=user_id,
                    limit=1000
                )
            else:
                # This would need to be implemented in the repository
                conversations = []
            
            # Filter by date range
            filtered_conversations = [
                conv for conv in conversations
                if start_date <= conv.created_at <= end_date
            ]
            
            data["total_conversations"] = len(filtered_conversations)
            data["total_messages"] = sum(conv.get_messages_count() for conv in filtered_conversations)
            data["total_tokens"] = sum(conv.get_total_tokens() for conv in filtered_conversations)
            
            # Calculate model usage
            model_usage = {}
            total_response_time = 0
            response_count = 0
            
            for conv in filtered_conversations:
                # Model usage
                most_used_model = conv.metadata.get_most_used_model()
                if most_used_model:
                    model_usage[most_used_model] = model_usage.get(most_used_model, 0) + 1
                
                # Response times (from message metadata)
                for message in conv.messages:
                    if message.processing_time:
                        total_response_time += message.processing_time
                        response_count += 1
            
            data["most_used_models"] = model_usage
            data["avg_response_time"] = total_response_time / max(response_count, 1)
            
            # User activity patterns
            daily_activity = {}
            for conv in filtered_conversations:
                date_key = conv.created_at.date().isoformat()
                daily_activity[date_key] = daily_activity.get(date_key, 0) + 1
            
            data["user_activity"] = {
                "daily_counts": daily_activity,
                "peak_activity_day": max(daily_activity.items(), key=lambda x: x[1])[0] if daily_activity else None
            }
            
            # Add detailed metrics if requested
            if "detailed" in metric_types:
                data["detailed_metrics"] = await self._get_detailed_metrics(
                    filtered_conversations,
                    start_date,
                    end_date
                )
            
        except Exception as e:
            logger.error(f"Error gathering analytics data: {str(e)}", exc_info=True)
        
        return data
    
    async def _get_detailed_metrics(
        self,
        conversations: List,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get detailed analytics metrics."""
        try:
            # Conversation length distribution
            length_distribution = {}
            for conv in conversations:
                length_bucket = self._get_length_bucket(conv.get_messages_count())
                length_distribution[length_bucket] = length_distribution.get(length_bucket, 0) + 1
            
            # Token usage distribution
            token_distribution = {}
            for conv in conversations:
                token_bucket = self._get_token_bucket(conv.get_total_tokens())
                token_distribution[token_bucket] = token_distribution.get(token_bucket, 0) + 1
            
            # Time-based patterns
            hourly_activity = {}
            for conv in conversations:
                hour = conv.created_at.hour
                hourly_activity[hour] = hourly_activity.get(hour, 0) + 1
            
            return {
                "conversation_length_distribution": length_distribution,
                "token_usage_distribution": token_distribution,
                "hourly_activity_pattern": hourly_activity,
                "avg_conversation_length": sum(conv.get_messages_count() for conv in conversations) / max(len(conversations), 1),
                "avg_tokens_per_conversation": sum(conv.get_total_tokens() for conv in conversations) / max(len(conversations), 1)
            }
            
        except Exception as e:
            logger.error(f"Error calculating detailed metrics: {str(e)}", exc_info=True)
            return {}
    
    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics."""
        try:
            # This would integrate with monitoring tools
            # For now, return basic metrics
            return {
                "cache_hit_rate": await self._calculate_cache_hit_rate(),
                "avg_response_time_24h": 0.0,  # Would be calculated from logs
                "error_rate_24h": 0.0,  # Would be calculated from logs
                "active_conversations": 0,  # Would be calculated from active sessions
                "requests_per_minute": 0.0  # Would be calculated from request logs
            }
        except Exception as e:
            logger.error(f"Error getting performance metrics: {str(e)}", exc_info=True)
            return {}
    
    async def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        try:
            cache_stats = await self.cache.get_stats()
            hits = cache_stats.get("hits", 0)
            misses = cache_stats.get("misses", 0)
            total = hits + misses
            return (hits / max(total, 1)) * 100
        except Exception:
            return 0.0
    
    def _get_length_bucket(self, message_count: int) -> str:
        """Get conversation length bucket."""
        if message_count <= 5:
            return "short (1-5)"
        elif message_count <= 15:
            return "medium (6-15)"
        elif message_count <= 30:
            return "long (16-30)"
        else:
            return "very_long (30+)"
    
    def _get_token_bucket(self, token_count: int) -> str:
        """Get token usage bucket."""
        if token_count <= 1000:
            return "low (0-1K)"
        elif token_count <= 5000:
            return "medium (1K-5K)"
        elif token_count <= 15000:
            return "high (5K-15K)"
        else:
            return "very_high (15K+)"
