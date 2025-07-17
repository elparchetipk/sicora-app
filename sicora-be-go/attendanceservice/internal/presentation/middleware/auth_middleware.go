package middleware

import (
	"net/http"
	"strings"

	"attendanceservice/configs"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

// AuthMiddleware middleware de autenticación JWT
func AuthMiddleware(config *configs.Config) gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "Authorization header required",
				"code":    "AUTH_HEADER_MISSING",
				"message": "Authorization header is required",
			})
			c.Abort()
			return
		}

		// Verificar formato Bearer token
		bearerToken := strings.Split(authHeader, " ")
		if len(bearerToken) != 2 || bearerToken[0] != "Bearer" {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "Invalid authorization header format",
				"code":    "INVALID_AUTH_FORMAT",
				"message": "Authorization header must be in format: Bearer <token>",
			})
			c.Abort()
			return
		}

		tokenString := bearerToken[1]

		// Verificar y parsear el token
		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, jwt.ErrSignatureInvalid
			}
			return []byte(config.JWT.Secret), nil
		})

		if err != nil || !token.Valid {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "Invalid token",
				"code":    "INVALID_TOKEN",
				"message": "The provided token is invalid or expired",
			})
			c.Abort()
			return
		}

		// Extraer claims del token
		if claims, ok := token.Claims.(jwt.MapClaims); ok {
			c.Set("user_id", claims["user_id"])
			c.Set("role", claims["role"])
			c.Set("exp", claims["exp"])
		}

		c.Next()
	}
}

// OptionalAuthMiddleware middleware de autenticación opcional
func OptionalAuthMiddleware(config *configs.Config) gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.Next()
			return
		}

		bearerToken := strings.Split(authHeader, " ")
		if len(bearerToken) != 2 || bearerToken[0] != "Bearer" {
			c.Next()
			return
		}

		tokenString := bearerToken[1]
		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, jwt.ErrSignatureInvalid
			}
			return []byte(config.JWT.Secret), nil
		})

		if err == nil && token.Valid {
			if claims, ok := token.Claims.(jwt.MapClaims); ok {
				c.Set("user_id", claims["user_id"])
				c.Set("role", claims["role"])
				c.Set("exp", claims["exp"])
			}
		}

		c.Next()
	}
}

// RequireRole middleware que requiere un rol específico
func RequireRole(roles ...string) gin.HandlerFunc {
	return func(c *gin.Context) {
		userRole, exists := c.Get("role")
		if !exists {
			c.JSON(http.StatusForbidden, gin.H{
				"error":   "Role not found",
				"code":    "ROLE_NOT_FOUND",
				"message": "User role not found in token",
			})
			c.Abort()
			return
		}

		roleStr, ok := userRole.(string)
		if !ok {
			c.JSON(http.StatusForbidden, gin.H{
				"error":   "Invalid role format",
				"code":    "INVALID_ROLE_FORMAT",
				"message": "User role has invalid format",
			})
			c.Abort()
			return
		}

		// Verificar si el rol del usuario está en la lista de roles permitidos
		for _, allowedRole := range roles {
			if roleStr == allowedRole {
				c.Next()
				return
			}
		}

		c.JSON(http.StatusForbidden, gin.H{
			"error":   "Insufficient permissions",
			"code":    "INSUFFICIENT_PERMISSIONS",
			"message": "User does not have required permissions",
		})
		c.Abort()
	}
}
