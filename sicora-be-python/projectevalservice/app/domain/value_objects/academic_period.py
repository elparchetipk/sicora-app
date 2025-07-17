from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class AcademicPeriod:
    academic_year: int
    trimester: int

    def __post_init__(self):
        if not (1 <= self.trimester <= 7):
            raise ValueError("Trimester must be between 1 and 7")
        if self.academic_year < 2020:
            raise ValueError("Academic year must be 2020 or later")

    @property
    def period_code(self) -> str:
        """Get period code like '2025-T3'"""
        return f"{self.academic_year}-T{self.trimester}"

    @property
    def is_final_trimester(self) -> bool:
        """Check if this is the final trimester (7th)"""
        return self.trimester == 7

    @property
    def is_initial_trimester(self) -> bool:
        """Check if this is the initial trimester (1st or 2nd)"""
        return self.trimester in [1, 2]

    @property
    def is_development_period(self) -> bool:
        """Check if this is a development period (3rd to 7th)"""
        return 3 <= self.trimester <= 7

    def next_trimester(self) -> "AcademicPeriod":
        """Get next trimester"""
        if self.trimester < 7:
            return AcademicPeriod(self.academic_year, self.trimester + 1)
        else:
            # Assuming new year starts after 7th trimester
            return AcademicPeriod(self.academic_year + 1, 1)

    def previous_trimester(self) -> Optional["AcademicPeriod"]:
        """Get previous trimester"""
        if self.trimester > 1:
            return AcademicPeriod(self.academic_year, self.trimester - 1)
        elif self.academic_year > 2020:
            return AcademicPeriod(self.academic_year - 1, 7)
        else:
            return None

    @classmethod
    def current_period(cls) -> "AcademicPeriod":
        """Get current academic period based on current date"""
        now = datetime.now()
        year = now.year

        # Simple logic to determine trimester based on month
        # This should be adjusted based on actual SENA calendar
        month = now.month
        if month <= 2:
            trimester = 1
        elif month <= 4:
            trimester = 2
        elif month <= 6:
            trimester = 3
        elif month <= 8:
            trimester = 4
        elif month <= 10:
            trimester = 5
        elif month <= 12:
            trimester = 6
        else:
            trimester = 7

        return cls(year, trimester)

    def __str__(self) -> str:
        return self.period_code
