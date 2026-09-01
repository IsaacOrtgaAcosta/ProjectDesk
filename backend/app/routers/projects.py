from fastapi import APIRouter, HTTPException, status

from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])
project_list: list[ProjectResponse] = []


@router.get("/", response_model=list[ProjectResponse])
def read_projects():
    return project_list


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int):
    for project in project_list:
        if project_id == project.id:
            return project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found",
    )


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


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectCreate):
    for index, project in enumerate(project_list):
        if project_id == project.id:
            updated_project = ProjectResponse(
                id=project.id,
                name=project_data.name,
                description=project_data.description,
            )

            project_list[index] = updated_project
            return updated_project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found",
    )
