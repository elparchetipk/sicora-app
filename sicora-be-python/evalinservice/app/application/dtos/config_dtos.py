"""DTOs for Configuration operations."""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class EvalinConfigurationRequest:
    """DTO para actualizar configuración del módulo EVALIN."""
    min_responses_for_results: Optional[int] = None
    enable_qualitative_comments: Optional[bool] = None
    anonymization_threshold: Optional[int] = None
    auto_close_periods: Optional[bool] = None
    notification_enabled: Optional[bool] = None
    reminder_days_before_end: Optional[int] = None
    max_evaluations_per_period: Optional[int] = None
    allow_multiple_periods_active: Optional[bool] = None


@dataclass
class EvalinConfigurationResponse:
    """DTO de respuesta para configuración del módulo EVALIN."""
    min_responses_for_results: int
    enable_qualitative_comments: bool
    anonymization_threshold: int
    auto_close_periods: bool
    notification_enabled: bool
    reminder_days_before_end: int
    max_evaluations_per_period: int
    allow_multiple_periods_active: bool
    last_updated_by: Optional[str]
    last_updated_at: Optional[str]


@dataclass
class SendNotificationRequest:
    """DTO para enviar notificaciones."""
    ficha_id: Optional[str] = None
    message_template: Optional[str] = None
    force_send: bool = False


@dataclass
class NotificationResponse:
    """DTO de respuesta para notificaciones enviadas."""
    total_recipients: int
    successful_sends: int
    failed_sends: int
    notification_id: str
    sent_at: str
    errors: list


@dataclass
class SendReminderRequest:
    """DTO para enviar recordatorios."""
    ficha_id: str
    custom_message: Optional[str] = None
    include_pending_only: bool = True


@dataclass
class ReminderResponse:
    """DTO de respuesta para recordatorios enviados."""
    ficha_id: str
    total_students: int
    students_notified: int
    pending_evaluations: int
    reminder_id: str
    sent_at: str
    message_preview: str


@dataclass
class SystemConfigResponse:
    """DTO de respuesta para configuración del sistema."""
    min_responses_for_results: int
    enable_qualitative_comments: bool
    anonymization_threshold: int
    auto_close_periods: bool
    notification_enabled: bool
    reminder_days_before_end: int
    max_evaluations_per_period: int
    allow_multiple_periods_active: bool
    version: str
    last_updated_by: Optional[str]
    last_updated_at: str
