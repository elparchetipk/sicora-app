"""
Configuración Swagger mejorada para projectevalservice
Generado automáticamente - vie 04 jul 2025 06:58:14 -05
"""

# Configuración de tags para organización de endpoints
tags_metadata = [
    {
        "name": "Health",
        "description": "Endpoints de estado y salud del servicio",
    },
    {
        "name": "Authentication", 
        "description": "Endpoints de autenticación y autorización",
    },
    {
        "name": "Users",
        "description": "Gestión de usuarios",
    },
    {
        "name": "Admin",
        "description": "Endpoints administrativos",
    },
    {
        "name": "API",
        "description": "Endpoints principales del servicio",
    }
]

# Configuración de servidor para documentación
servers = [
    {
        "url": "http://localhost:9006",
        "description": "Servidor de desarrollo local"
    },
    {
        "url": "http://localhost:9006/api/v1", 
        "description": "API v1"
    }
]

# Configuración de contacto
contact = {
    "name": "Equipo SICORA",
    "email": "dev@sicora.sena.edu.co",
    "url": "https://github.com/sicora-dev"
}

# Configuración de licencia
license_info = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT"
}
