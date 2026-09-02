from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])
project_list: list[ProjectResponse] = []


@router.get("/", response_model=list[ProjectResponse])
def read_projects(db: Annotated[Session, Depends(get_db)]):
    statement = select(Project)
    projects = db.scalars(statement).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Annotated[Session, Depends(get_db)]):
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.post("/",
             response_model=ProjectResponse,
             status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    db: Annotated[Session, Depends(get_db)]
):
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int,
                   project_data: ProjectCreate,
                   db: Annotated[Session, Depends(get_db)]):
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    project.name = project_data.name
    project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project


@router.delete("/{project_id}")
def delete_project(project_id: int):
    for index, project in enumerate(project_list):
        if project_id == project.id:
            deleted_project = project_list.pop(index)
            return deleted_project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found",
    )
