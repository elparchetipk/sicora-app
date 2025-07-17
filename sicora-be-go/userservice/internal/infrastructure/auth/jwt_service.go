package auth

import (
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
)

// UserClaims representa los claims del JWT del usuario
type UserClaims struct {
	UserID             uuid.UUID `json:"user_id"`
	Email              string    `json:"email"`
	Role               string    `json:"role"`
	IsActive           bool      `json:"is_active"`
	MustChangePassword bool      `json:"must_change_password"`
	jwt.RegisteredClaims
}

// JWTService maneja la generación y validación de tokens JWT
type JWTService struct {
	secret     []byte
	issuer     string
	expiration time.Duration
}

// NewJWTService crea un nuevo servicio JWT
func NewJWTService(secret, issuer string, expiration time.Duration) *JWTService {
	return &JWTService{
		secret:     []byte(secret),
		issuer:     issuer,
		expiration: expiration,
	}
}

// GenerateToken genera un token JWT para un usuario
func (j *JWTService) GenerateToken(userID uuid.UUID, email, role string, isActive, mustChangePassword bool) (string, error) {
	now := time.Now()
	claims := UserClaims{
		UserID:             userID,
		Email:              email,
		Role:               role,
		IsActive:           isActive,
		MustChangePassword: mustChangePassword,
		RegisteredClaims: jwt.RegisteredClaims{
			Issuer:    j.issuer,
			Subject:   userID.String(),
			IssuedAt:  jwt.NewNumericDate(now),
			ExpiresAt: jwt.NewNumericDate(now.Add(j.expiration)),
			NotBefore: jwt.NewNumericDate(now),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(j.secret)
}

// ValidateToken valida un token JWT y retorna los claims
func (j *JWTService) ValidateToken(tokenString string) (*UserClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &UserClaims{}, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, jwt.ErrSignatureInvalid
		}
		return j.secret, nil
	})

	if err != nil {
		return nil, err
	}

	if claims, ok := token.Claims.(*UserClaims); ok && token.Valid {
		// Validaciones adicionales
		if !claims.IsActive {
			return nil, errors.New("user is not active")
		}

		return claims, nil
	}

	return nil, errors.New("invalid token claims")
}

// RefreshToken genera un nuevo token basado en uno existente válido
func (j *JWTService) RefreshToken(tokenString string) (string, error) {
	claims, err := j.ValidateToken(tokenString)
	if err != nil {
		return "", err
	}

	// Generar nuevo token con los mismos datos pero nueva expiración
	return j.GenerateToken(
		claims.UserID,
		claims.Email,
		claims.Role,
		claims.IsActive,
		claims.MustChangePassword,
	)
}

// ExtractUserID extrae el ID del usuario del token
func (j *JWTService) ExtractUserID(tokenString string) (uuid.UUID, error) {
	claims, err := j.ValidateToken(tokenString)
	if err != nil {
		return uuid.Nil, err
	}
	return claims.UserID, nil
}

// ExtractRole extrae el rol del usuario del token
func (j *JWTService) ExtractRole(tokenString string) (string, error) {
	claims, err := j.ValidateToken(tokenString)
	if err != nil {
		return "", err
	}
	return claims.Role, nil
}

// IsTokenExpired verifica si un token está expirado sin validar la signature
func (j *JWTService) IsTokenExpired(tokenString string) bool {
	token, _ := jwt.ParseWithClaims(tokenString, &UserClaims{}, func(token *jwt.Token) (interface{}, error) {
		return j.secret, nil
	})

	if claims, ok := token.Claims.(*UserClaims); ok {
		return claims.ExpiresAt.Before(time.Now())
	}

	return true
}
