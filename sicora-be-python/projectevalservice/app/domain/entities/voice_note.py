from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from enum import Enum


class VoiceNoteStatus(str, Enum):
    """Estado de una nota de voz."""

    UPLOADED = "uploaded"
    TRANSCRIBING = "transcribing"
    TRANSCRIBED = "transcribed"
    ANALYZED = "analyzed"
    ERROR = "error"


class SentimentType(str, Enum):
    """Tipos de sentimiento en análisis."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


@dataclass(frozen=True)
class VoiceNote:
    """Entidad de dominio para notas de voz."""

    id: UUID
    evaluation_session_id: UUID
    criterion_id: Optional[UUID]
    instructor_id: UUID
    file_path: str
    file_size_bytes: int
    duration_seconds: float
    audio_format: str
    status: VoiceNoteStatus
    created_at: datetime
    updated_at: datetime

    def is_transcribed(self) -> bool:
        """Verifica si la nota ha sido transcrita."""
        return self.status in [VoiceNoteStatus.TRANSCRIBED, VoiceNoteStatus.ANALYZED]

    def is_ready_for_analysis(self) -> bool:
        """Verifica si está lista para análisis de sentimientos."""
        return self.status == VoiceNoteStatus.TRANSCRIBED


@dataclass(frozen=True)
class Transcription:
    """Entidad para transcripciones automáticas."""

    id: UUID
    voice_note_id: UUID
    original_text: str
    edited_text: Optional[str]
    confidence_score: float
    language_detected: str
    processing_time_seconds: float
    transcription_provider: str  # openai, azure, google
    created_at: datetime
    updated_at: Optional[datetime] = None
    edited_by: Optional[UUID] = None

    @property
    def final_text(self) -> str:
        """Retorna el texto final (editado o original)."""
        return self.edited_text if self.edited_text else self.original_text

    def is_high_confidence(self) -> bool:
        """Verifica si la transcripción tiene alta confianza."""
        return self.confidence_score >= 0.85


@dataclass(frozen=True)
class SentimentAnalysis:
    """Entidad para análisis de sentimientos."""

    id: UUID
    transcription_id: UUID
    overall_sentiment: SentimentType
    sentiment_score: float  # -1.0 (muy negativo) a 1.0 (muy positivo)
    confidence: float
    key_phrases: List[str]
    emotion_breakdown: Dict[str, float]  # {"joy": 0.1, "frustration": 0.7, etc.}
    analysis_provider: str
    processing_time_seconds: float
    created_at: datetime

    def is_concerning(self) -> bool:
        """Verifica si el sentimiento indica áreas problemáticas."""
        return (
            self.overall_sentiment == SentimentType.NEGATIVE
            and self.sentiment_score < -0.5
        )

    def requires_attention(self) -> bool:
        """Verifica si requiere atención especial."""
        frustration_level = self.emotion_breakdown.get("frustration", 0.0)
        concern_level = self.emotion_breakdown.get("concern", 0.0)
        return frustration_level > 0.6 or concern_level > 0.6


@dataclass(frozen=True)
class TranscriptionSummary:
    """Resumen de transcripciones por categoría."""

    id: UUID
    evaluation_session_id: UUID
    criterion_category: str
    summary_text: str
    key_observations: List[str]
    common_themes: List[str]
    overall_sentiment: SentimentType
    attention_flags: List[str]
    generated_at: datetime
    total_voice_notes: int
    average_sentiment_score: float
