from fastapi import APIRouter
from app.schemas.project import ProjectCreate, ProjectResponse


project_list: list[ProjectResponse] = []
router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/")
def read_projects():
    return project_list
