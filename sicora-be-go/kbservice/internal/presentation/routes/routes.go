package routes

import (
	"kbservice/internal/presentation/handlers"

	"github.com/gin-gonic/gin"
)

// SetupDocumentRoutes sets up document-related routes
func SetupDocumentRoutes(router *gin.Engine, documentHandler *handlers.DocumentHandler) {
	v1 := router.Group("/api/v1")
	{
		documents := v1.Group("/documents")
		{
			// CRUD operations
			documents.POST("", documentHandler.CreateDocument)
			documents.GET("/:id", documentHandler.GetDocument)
			documents.PUT("/:id", documentHandler.UpdateDocument)
			documents.DELETE("/:id", documentHandler.DeleteDocument)
			
			// Search
			documents.GET("", documentHandler.SearchDocuments)
			documents.POST("/search/semantic", documentHandler.SemanticSearchDocuments)
			
			// Workflow operations
			documents.POST("/:id/submit-for-review", documentHandler.SubmitForReview)
			documents.POST("/:id/approve", documentHandler.ApproveDocument)
			documents.POST("/:id/publish", documentHandler.PublishDocument)
			
			// Analytics
			documents.GET("/:id/analytics", documentHandler.GetDocumentAnalytics)
		}
		
		// Alternative slug-based access
		v1.GET("/docs/:slug", documentHandler.GetDocumentBySlug)
	}
}

// SetupFAQRoutes sets up FAQ-related routes
func SetupFAQRoutes(router *gin.Engine, faqHandler *handlers.FAQHandler) {
	v1 := router.Group("/api/v1")
	{
		faqs := v1.Group("/faqs")
		{
			// CRUD operations
			faqs.POST("", faqHandler.CreateFAQ)
			faqs.GET("/:id", faqHandler.GetFAQ)
			faqs.PUT("/:id", faqHandler.UpdateFAQ)
			faqs.DELETE("/:id", faqHandler.DeleteFAQ)
			
			// Search and discovery
			faqs.GET("", faqHandler.SearchFAQs)
			faqs.POST("/search/semantic", faqHandler.SemanticSearchFAQs)
			faqs.GET("/popular", faqHandler.GetPopularFAQs)
			faqs.GET("/trending", faqHandler.GetTrendingFAQs)
			
			// Rating and feedback
			faqs.POST("/:id/rate", faqHandler.RateFAQ)
			
			// Workflow
			faqs.POST("/:id/publish", faqHandler.PublishFAQ)
			
			// Analytics
			faqs.GET("/:id/analytics", faqHandler.GetFAQAnalytics)
			faqs.GET("/:id/related", faqHandler.GetRelatedFAQs)
		}
	}
}

// SetupAnalyticsRoutes sets up analytics-related routes
func SetupAnalyticsRoutes(router *gin.Engine, analyticsHandler *handlers.AnalyticsHandler) {
	v1 := router.Group("/api/v1")
	{
		analytics := v1.Group("/analytics")
		{
			// General analytics
			analytics.GET("/content", analyticsHandler.GetContentStats)
			analytics.GET("/engagement", analyticsHandler.GetUserEngagement)
			analytics.GET("/search", analyticsHandler.GetSearchStats)
			
			// Performance analytics
			analytics.GET("/top-content", analyticsHandler.GetTopContent)
			analytics.GET("/trends", analyticsHandler.GetContentTrends)
			
			// Knowledge gaps
			analytics.GET("/unanswered-questions", analyticsHandler.GetUnansweredQuestions)
			analytics.GET("/content-gaps", analyticsHandler.GetContentGaps)
			
			// Real-time
			analytics.GET("/realtime", analyticsHandler.GetRealTimeStats)
			
			// Reports
			analytics.POST("/reports", analyticsHandler.GenerateReport)
			analytics.GET("/reports", analyticsHandler.GetScheduledReports)
		}
	}
}

// SetupHealthRoutes sets up health check routes
func SetupHealthRoutes(router *gin.Engine) {
	router.GET("/health", func(c *gin.Context) {
		// Health check logic would be implemented here
		c.JSON(200, gin.H{
			"status":  "healthy",
			"service": "kbservice",
		})
	})

	router.GET("/ready", func(c *gin.Context) {
		// Readiness check logic would be implemented here
		c.JSON(200, gin.H{
			"status": "ready",
		})
	})
}

// SetupAllRoutes sets up all application routes
func SetupAllRoutes(
	router *gin.Engine,
	documentHandler *handlers.DocumentHandler,
	faqHandler *handlers.FAQHandler,
	analyticsHandler *handlers.AnalyticsHandler,
) {
	// Health checks
	SetupHealthRoutes(router)
	
	// API routes
	SetupDocumentRoutes(router, documentHandler)
	SetupFAQRoutes(router, faqHandler)
	SetupAnalyticsRoutes(router, analyticsHandler)
	
	// API documentation
	router.GET("/api/docs", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "API documentation would be served here",
			"swagger": "/api/docs/swagger.json",
		})
	})
}
