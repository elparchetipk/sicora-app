from fastapi import APIRouter

from ....presentation.controllers.project_controller import router as project_router
from ....presentation.controllers.evaluation_controller import router as evaluation_router

api_router = APIRouter()

# Include all routers
api_router.include_router(project_router)
api_router.include_router(evaluation_router)

# TODO: Include additional routers for criteria, groups, and voice notes
# api_router.include_router(criteria_router)
# api_router.include_router(group_router)
# api_router.include_router(voice_note_router)
