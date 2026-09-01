from fastapi import APIRouter, status

from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])
project_list: list[ProjectResponse] = []


@router.get("/", response_model=list[ProjectResponse])
def read_projects():
    return project_list


@router.post("/",
             response_model=ProjectResponse,
             status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate):
    project_id = len(project_list) + 1
    created_project = ProjectResponse(
        id=project_id,
        name=project.name,
        description=project.description,
    )
    project_list.append(created_project)
    return created_project
