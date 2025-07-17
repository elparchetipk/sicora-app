package middleware

import (
	"net/http"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

// AuthMiddleware maneja la autenticación JWT
type AuthMiddleware struct {
	jwtSecret string
}

// UserClaims representa las claims del JWT
type UserClaims struct {
	UserID uuid.UUID `json:"user_id"`
	Email  string    `json:"email"`
	Role   string    `json:"role"`
	exp    int64     `json:"exp"`
}

// NewAuthMiddleware crea un nuevo middleware de autenticación
func NewAuthMiddleware(jwtSecret string) *AuthMiddleware {
	return &AuthMiddleware{
		jwtSecret: jwtSecret,
	}
}

// Authenticate middleware que valida el token JWT
func (m *AuthMiddleware) Authenticate() gin.HandlerFunc {
	return func(c *gin.Context) {
		token := extractToken(c)
		if token == "" {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "Missing or invalid authorization header",
				"message": "Authorization token is required",
			})
			c.Abort()
			return
		}

		claims, err := m.validateToken(token)
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "Invalid token",
				"message": err.Error(),
			})
			c.Abort()
			return
		}

		// Verificar si el token ha expirado
		if time.Now().Unix() > claims.exp {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "Token expired",
				"message": "Please login again",
			})
			c.Abort()
			return
		}

		// Agregar información del usuario al contexto
		c.Set("user_id", claims.UserID)
		c.Set("user_email", claims.Email)
		c.Set("user_role", claims.Role)

		c.Next()
	}
}

// RequireRole middleware que requiere un rol específico
func (m *AuthMiddleware) RequireRole(allowedRoles ...string) gin.HandlerFunc {
	return func(c *gin.Context) {
		userRole, exists := c.Get("user_role")
		if !exists {
			c.JSON(http.StatusForbidden, gin.H{
				"error":   "Access denied",
				"message": "User role not found in context",
			})
			c.Abort()
			return
		}

		role, ok := userRole.(string)
		if !ok {
			c.JSON(http.StatusForbidden, gin.H{
				"error":   "Access denied",
				"message": "Invalid user role format",
			})
			c.Abort()
			return
		}

		// Verificar si el rol del usuario está en la lista de roles permitidos
		for _, allowedRole := range allowedRoles {
			if role == allowedRole {
				c.Next()
				return
			}
		}

		c.JSON(http.StatusForbidden, gin.H{
			"error":   "Access denied",
			"message": "Insufficient permissions for this operation",
		})
		c.Abort()
	}
}

// RequireAdminOrOwner middleware que requiere ser admin o propietario del recurso
func (m *AuthMiddleware) RequireAdminOrOwner(ownerIDParam string) gin.HandlerFunc {
	return func(c *gin.Context) {
		userRole, _ := c.Get("user_role")
		userID, _ := c.Get("user_id")

		// Si es admin, permitir acceso
		if userRole == "admin" {
			c.Next()
			return
		}

		// Si no es admin, verificar si es el propietario
		ownerIDStr := c.Param(ownerIDParam)
		if ownerIDStr == "" {
			ownerIDStr = c.Query(ownerIDParam)
		}

		if ownerIDStr == "" {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":   "Bad request",
				"message": "Owner ID parameter is required",
			})
			c.Abort()
			return
		}

		ownerID, err := uuid.Parse(ownerIDStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":   "Bad request",
				"message": "Invalid owner ID format",
			})
			c.Abort()
			return
		}

		currentUserID, ok := userID.(uuid.UUID)
		if !ok || currentUserID != ownerID {
			c.JSON(http.StatusForbidden, gin.H{
				"error":   "Access denied",
				"message": "You can only access your own resources",
			})
			c.Abort()
			return
		}

		c.Next()
	}
}

// extractToken extrae el token del header Authorization
func extractToken(c *gin.Context) string {
	bearerToken := c.GetHeader("Authorization")
	if len(strings.Split(bearerToken, " ")) == 2 {
		return strings.Split(bearerToken, " ")[1]
	}
	return ""
}

// validateToken valida el token JWT y extrae las claims
func (m *AuthMiddleware) validateToken(tokenString string) (*UserClaims, error) {
	// Esta es una implementación simplificada
	// En producción, usar una librería como github.com/golang-jwt/jwt/v5

	// Por ahora, simulamos la validación
	// TODO: Implementar validación real de JWT
	claims := &UserClaims{
		UserID: uuid.New(), // En producción, extraer del token
		Email:  "user@example.com",
		Role:   "student",
		exp:    time.Now().Add(24 * time.Hour).Unix(),
	}

	return claims, nil
}

// GetUserIDFromContext obtiene el ID del usuario desde el contexto
func GetUserIDFromContext(c *gin.Context) (uuid.UUID, bool) {
	userID, exists := c.Get("user_id")
	if !exists {
		return uuid.Nil, false
	}

	id, ok := userID.(uuid.UUID)
	return id, ok
}

// GetUserRoleFromContext obtiene el rol del usuario desde el contexto
func GetUserRoleFromContext(c *gin.Context) (string, bool) {
	userRole, exists := c.Get("user_role")
	if !exists {
		return "", false
	}

	role, ok := userRole.(string)
	return role, ok
}
