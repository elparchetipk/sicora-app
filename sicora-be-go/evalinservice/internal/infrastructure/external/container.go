package external

// ExternalServiceContainer contiene todos los adaptadores de servicios externos
type ExternalServiceContainer struct {
	UserService         *UserServiceAdapter
	NotificationService *NotificationServiceAdapter
	ScheduleService     *ScheduleServiceAdapter
}

// ExternalServiceConfig contiene la configuración para los servicios externos
type ExternalServiceConfig struct {
	UserService struct {
		BaseURL string
		APIKey  string
	}
	NotificationService struct {
		BaseURL string
		APIKey  string
	}
	ScheduleService struct {
		BaseURL string
		APIKey  string
	}
}

// NewExternalServiceContainer crea un nuevo contenedor con todos los adaptadores de servicios externos
func NewExternalServiceContainer(config *ExternalServiceConfig) *ExternalServiceContainer {
	return &ExternalServiceContainer{
		UserService: NewUserServiceAdapter(
			config.UserService.BaseURL,
			config.UserService.APIKey,
		),
		NotificationService: NewNotificationServiceAdapter(
			config.NotificationService.BaseURL,
			config.NotificationService.APIKey,
		),
		ScheduleService: NewScheduleServiceAdapter(
			config.ScheduleService.BaseURL,
			config.ScheduleService.APIKey,
		),
	}
}
