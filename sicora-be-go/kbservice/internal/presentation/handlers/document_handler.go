package handlers

import (
	"net/http"
	"strconv"
	"time"

	"kbservice/internal/application/dto"
	"kbservice/internal/application/usecases"
	"kbservice/internal/domain/entities"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

// DocumentHandler handles HTTP requests for documents
type DocumentHandler struct {
	documentUseCase *usecases.DocumentUseCase
}

// NewDocumentHandler creates a new document handler
func NewDocumentHandler(documentUseCase *usecases.DocumentUseCase) *DocumentHandler {
	return &DocumentHandler{
		documentUseCase: documentUseCase,
	}
}

// CreateDocument handles document creation
func (h *DocumentHandler) CreateDocument(c *gin.Context) {
	var req dto.CreateDocumentRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	document, err := h.documentUseCase.CreateDocument(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"data": document})
}

// GetDocument handles document retrieval by ID
func (h *DocumentHandler) GetDocument(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid document ID"})
		return
	}

	// Get user ID from context (would be set by auth middleware)
	var userID *uuid.UUID
	if userIDStr := c.GetHeader("X-User-ID"); userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			userID = &uid
		}
	}

	document, err := h.documentUseCase.GetDocument(c.Request.Context(), id, userID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": document})
}

// GetDocumentBySlug handles document retrieval by slug
func (h *DocumentHandler) GetDocumentBySlug(c *gin.Context) {
	slug := c.Param("slug")
	if slug == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Slug is required"})
		return
	}

	// Get user ID from context
	var userID *uuid.UUID
	if userIDStr := c.GetHeader("X-User-ID"); userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			userID = &uid
		}
	}

	document, err := h.documentUseCase.GetDocumentBySlug(c.Request.Context(), slug, userID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": document})
}

// UpdateDocument handles document updates
func (h *DocumentHandler) UpdateDocument(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid document ID"})
		return
	}

	var req dto.UpdateDocumentRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Set user info from headers (would be set by auth middleware)
	if userIDStr := c.GetHeader("X-User-ID"); userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			req.UserID = uid
		}
	}
	req.UserRole = c.GetHeader("X-User-Role")

	document, err := h.documentUseCase.UpdateDocument(c.Request.Context(), id, &req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": document})
}

// DeleteDocument handles document deletion
func (h *DocumentHandler) DeleteDocument(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid document ID"})
		return
	}

	// Get user info from headers
	userIDStr := c.GetHeader("X-User-ID")
	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User ID is required"})
		return
	}

	userRole := c.GetHeader("X-User-Role")

	err = h.documentUseCase.DeleteDocument(c.Request.Context(), id, userID, userRole)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

// SearchDocuments handles document search
func (h *DocumentHandler) SearchDocuments(c *gin.Context) {
	var req dto.SearchDocumentsRequest

	// Parse query parameters
	req.Query = c.Query("q")
	
	if categories := c.QueryArray("categories"); len(categories) > 0 {
		req.Categories = make([]entities.DocumentCategory, len(categories))
		for i, cat := range categories {
			req.Categories[i] = entities.DocumentCategory(cat)
		}
	}

	if audiences := c.QueryArray("audiences"); len(audiences) > 0 {
		req.Audiences = make([]entities.AudienceType, len(audiences))
		for i, aud := range audiences {
			req.Audiences[i] = entities.AudienceType(aud)
		}
	}

	if types := c.QueryArray("types"); len(types) > 0 {
		req.Types = make([]entities.DocumentType, len(types))
		for i, typ := range types {
			req.Types[i] = entities.DocumentType(typ)
		}
	}

	req.Tags = c.QueryArray("tags")
	req.SortBy = c.Query("sortBy")
	req.SortOrder = c.Query("sortOrder")

	if limitStr := c.Query("limit"); limitStr != "" {
		if limit, err := strconv.Atoi(limitStr); err == nil {
			req.Limit = limit
		}
	}

	if offsetStr := c.Query("offset"); offsetStr != "" {
		if offset, err := strconv.Atoi(offsetStr); err == nil {
			req.Offset = offset
		}
	}

	// Set default limit if not provided
	if req.Limit == 0 {
		req.Limit = 20
	}

	results, err := h.documentUseCase.SearchDocuments(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": results})
}

// SemanticSearchDocuments handles semantic search
func (h *DocumentHandler) SemanticSearchDocuments(c *gin.Context) {
	var req dto.SemanticSearchRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Set defaults
	if req.Limit == 0 {
		req.Limit = 10
	}
	if req.Threshold == 0 {
		req.Threshold = 0.7
	}

	results, err := h.documentUseCase.SemanticSearchDocuments(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": results})
}

// SubmitForReview handles document review submission
func (h *DocumentHandler) SubmitForReview(c *gin.Context) {
	idStr := c.Param("id")
	documentID, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid document ID"})
		return
	}

	var req struct {
		ReviewerID uuid.UUID `json:"reviewerId" binding:"required"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Get user info from headers
	userIDStr := c.GetHeader("X-User-ID")
	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User ID is required"})
		return
	}

	userRole := c.GetHeader("X-User-Role")

	err = h.documentUseCase.SubmitForReview(c.Request.Context(), documentID, req.ReviewerID, userID, userRole)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Document submitted for review"})
}

// ApproveDocument handles document approval
func (h *DocumentHandler) ApproveDocument(c *gin.Context) {
	idStr := c.Param("id")
	documentID, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid document ID"})
		return
	}

	// Get reviewer ID from headers
	reviewerIDStr := c.GetHeader("X-User-ID")
	reviewerID, err := uuid.Parse(reviewerIDStr)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User ID is required"})
		return
	}

	err = h.documentUseCase.ApproveDocument(c.Request.Context(), documentID, reviewerID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Document approved"})
}

// PublishDocument handles document publication
func (h *DocumentHandler) PublishDocument(c *gin.Context) {
	idStr := c.Param("id")
	documentID, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid document ID"})
		return
	}

	// Get user info from headers
	userIDStr := c.GetHeader("X-User-ID")
	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User ID is required"})
		return
	}

	userRole := c.GetHeader("X-User-Role")

	err = h.documentUseCase.PublishDocument(c.Request.Context(), documentID, userID, userRole)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Document published"})
}

// GetDocumentAnalytics handles analytics retrieval
func (h *DocumentHandler) GetDocumentAnalytics(c *gin.Context) {
	idStr := c.Param("id")
	documentID, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid document ID"})
		return
	}

	// Parse date range
	fromStr := c.Query("from")
	toStr := c.Query("to")
	
	var from, to time.Time
	if fromStr != "" {
		from, err = time.Parse("2006-01-02", fromStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid from date format"})
			return
		}
	} else {
		from = time.Now().AddDate(0, 0, -30) // Default to last 30 days
	}

	if toStr != "" {
		to, err = time.Parse("2006-01-02", toStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid to date format"})
			return
		}
	} else {
		to = time.Now()
	}

	analytics, err := h.documentUseCase.GetDocumentAnalytics(c.Request.Context(), documentID, from, to)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": analytics})
}
