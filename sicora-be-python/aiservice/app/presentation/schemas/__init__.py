"""Presentation layer schemas for the AI Service."""

from .chat_schemas import *
from .knowledge_schemas import *
from .model_schemas import *
from .analytics_schemas import *

__all__ = [
    # Chat schemas
    "MessageTypeEnum",
    "ConversationStatusEnum", 
    "MessageCreate",
    "MessageResponse",
    "ConversationCreate",
    "ConversationUpdate",
    "ConversationResponse",
    "ConversationWithMessages",
    "ChatRequest",
    "ChatResponse",
    "StreamChatResponse",
    "ConversationListQuery",
    "ConversationListResponse",
    "ConversationStats",
    
    # Knowledge schemas
    "KnowledgeEntryCreate",
    "KnowledgeEntryUpdate", 
    "KnowledgeEntryResponse",
    "KnowledgeSearchRequest",
    "KnowledgeSearchResult",
    "KnowledgeSearchResponse",
    "KnowledgeListQuery",
    "KnowledgeListResponse",
    "KnowledgeBulkCreate",
    "KnowledgeBulkCreateResponse",
    "KnowledgeStats",
    "KnowledgeEmbeddingRequest",
    "KnowledgeEmbeddingResponse",
    "KnowledgeAnalysisRequest",
    "KnowledgeAnalysisResponse",
    
    # Model schemas
    "ModelTypeEnum",
    "ModelProviderEnum",
    "ModelStatusEnum",
    "AIModelCreate",
    "AIModelUpdate",
    "AIModelResponse",
    "ModelTestRequest",
    "ModelTestResponse",
    "ModelAvailabilityCheck",
    "ModelAvailabilityResponse",
    "ModelListQuery",
    "ModelListResponse",
    "ModelUsageStats",
    "ModelComparisonRequest",
    "ModelComparisonResult",
    "ModelComparisonResponse",
    "ModelRecommendationRequest",
    "ModelRecommendationResponse",
    
    # Analytics schemas
    "AnalyticsPeriod",
    "MetricType",
    "AnalyticsQuery",
    "MetricValue",
    "TimeSeriesDataPoint",
    "AnalyticsResponse",
    "ConversationAnalytics",
    "MessageAnalytics",
    "ModelAnalytics",
    "KnowledgeAnalytics",
    "UserAnalytics",
    "SystemAnalytics",
    "ComprehensiveAnalytics",
    "AlertThreshold",
    "AnalyticsAlert",
    "CustomReport",
    "CustomReportResponse",
    "ReportExecution"
]
