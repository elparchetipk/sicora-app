package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// BasicScheduleHandler handler temporal básico
type BasicScheduleHandler struct{}

// NewBasicScheduleHandler crea un handler básico temporal
func NewBasicScheduleHandler() *BasicScheduleHandler {
	return &BasicScheduleHandler{}
}

// CreateSchedule placeholder
func (h *BasicScheduleHandler) CreateSchedule(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "CreateSchedule not implemented yet",
	})
}

// GetSchedule placeholder
func (h *BasicScheduleHandler) GetSchedule(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "GetSchedule not implemented yet",
	})
}

// ListSchedules placeholder
func (h *BasicScheduleHandler) ListSchedules(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "ListSchedules not implemented yet",
	})
}

// UpdateSchedule placeholder
func (h *BasicScheduleHandler) UpdateSchedule(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "UpdateSchedule not implemented yet",
	})
}

// DeleteSchedule placeholder
func (h *BasicScheduleHandler) DeleteSchedule(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "DeleteSchedule not implemented yet",
	})
}

// BasicMasterDataHandler handler temporal básico para datos maestros
type BasicMasterDataHandler struct{}

// NewBasicMasterDataHandler crea un handler básico temporal
func NewBasicMasterDataHandler() *BasicMasterDataHandler {
	return &BasicMasterDataHandler{}
}

// CreateAcademicProgram placeholder
func (h *BasicMasterDataHandler) CreateAcademicProgram(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "CreateAcademicProgram not implemented yet",
	})
}

// ListAcademicPrograms placeholder
func (h *BasicMasterDataHandler) ListAcademicPrograms(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "ListAcademicPrograms not implemented yet",
	})
}

// CreateAcademicGroup placeholder
func (h *BasicMasterDataHandler) CreateAcademicGroup(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "CreateAcademicGroup not implemented yet",
	})
}

// ListAcademicGroups placeholder
func (h *BasicMasterDataHandler) ListAcademicGroups(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "ListAcademicGroups not implemented yet",
	})
}

// CreateVenue placeholder
func (h *BasicMasterDataHandler) CreateVenue(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "CreateVenue not implemented yet",
	})
}

// ListVenues placeholder
func (h *BasicMasterDataHandler) ListVenues(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "ListVenues not implemented yet",
	})
}

// CreateCampus placeholder
func (h *BasicMasterDataHandler) CreateCampus(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "CreateCampus not implemented yet",
	})
}

// ListCampuses placeholder
func (h *BasicMasterDataHandler) ListCampuses(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{
		"message": "ListCampuses not implemented yet",
	})
}
