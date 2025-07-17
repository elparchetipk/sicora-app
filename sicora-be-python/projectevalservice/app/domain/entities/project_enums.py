from enum import Enum


class ProjectStatus(Enum):
    IDEA_PROPOSAL = "idea_proposal"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectType(Enum):
    FORMATIVE = "formative"
    PRODUCTIVE = "productive"
    RESEARCH = "research"
    INNOVATION = "innovation"
