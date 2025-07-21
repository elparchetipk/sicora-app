"""
Servicio de templates para NotificationService
"""

from jinja2 import Environment, FileSystemLoader, Template
from typing import Dict, Any, Optional
import os
import logging

logger = logging.getLogger(__name__)

class TemplateService:
    """Servicio para manejo de templates de notificaciones."""

    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "../templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render_email_template(
        self,
        template_name: str,
        variables: Dict[str, Any]
    ) -> Optional[str]:
        """Renderizar template de email."""
        try:
            template = self.env.get_template(f"email/{template_name}")
            return template.render(**variables)
        except Exception as e:
            logger.error(f"Error renderizando template {template_name}: {str(e)}")
            return None

    def render_sms_template(
        self,
        template_name: str,
        variables: Dict[str, Any]
    ) -> Optional[str]:
        """Renderizar template de SMS."""
        try:
            template = self.env.get_template(f"sms/{template_name}")
            return template.render(**variables)
        except Exception as e:
            logger.error(f"Error renderizando template SMS {template_name}: {str(e)}")
            return None
