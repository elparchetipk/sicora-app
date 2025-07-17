from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class EvaluationScore:
    technical: float
    presentation: float
    documentation: float
    innovation: float
    collaboration: float

    def __post_init__(self):
        # Validate scores are between 0 and 5
        for field, value in self.__dict__.items():
            if not (0.0 <= value <= 5.0):
                raise ValueError(f"Score {field} must be between 0.0 and 5.0")

    @property
    def overall_score(self) -> float:
        """Calculate weighted overall score"""
        weights = {
            "technical": 0.3,
            "presentation": 0.2,
            "documentation": 0.2,
            "innovation": 0.15,
            "collaboration": 0.15,
        }

        return (
            self.technical * weights["technical"]
            + self.presentation * weights["presentation"]
            + self.documentation * weights["documentation"]
            + self.innovation * weights["innovation"]
            + self.collaboration * weights["collaboration"]
        )

    @property
    def is_passing(self) -> bool:
        """Check if score is passing (>= 3.0)"""
        return self.overall_score >= 3.0

    @property
    def grade_letter(self) -> str:
        """Get letter grade based on overall score"""
        score = self.overall_score
        if score >= 4.5:
            return "A"
        elif score >= 4.0:
            return "B"
        elif score >= 3.0:
            return "C"
        elif score >= 2.0:
            return "D"
        else:
            return "F"

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "technical": self.technical,
            "presentation": self.presentation,
            "documentation": self.documentation,
            "innovation": self.innovation,
            "collaboration": self.collaboration,
            "overall": self.overall_score,
        }
