from datetime import date
from fastapi import APIRouter, Depends, HTTPException

from app.domain.exceptions import (
    DomainError,
    NotFoundError,
    InvalidStatusTransition,
    ValidationError,
)
from app.repositories.memory import InMemoryProjectRepo, InMemoryTaskRepo
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.schemas.dto import ProjectCreate, ProjectOut, TaskCreate, TaskOut, TaskUpdate

router = APIRouter()

project_repo = InMemoryProjectRepo()
task_repo = InMemoryTaskRepo()


def get_project_service() -> ProjectService:
    return ProjectService(project_repo)


def get_task_service() -> TaskService:
    return TaskService(project_repo, task_repo)


def to_http(e: Exception) -> HTTPException:
    if isinstance(e, NotFoundError):
        return HTTPException(status_code=404, detail=str(e))
    if isinstance(e, (InvalidStatusTransition, ValidationError, ValueError)):
        return HTTPException(status_code=400, detail=str(e))
    if isinstance(e, DomainError):
        return HTTPException(status_code=500, detail="Internal Server Error")
    return HTTPException(status_code=500, detail="Unexpected error")


@router.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(
    body: ProjectCreate, service: ProjectService = Depends(get_project_service)
):
    try:
        project = service.create(body.name)
        return ProjectOut(id=project.id, name=project.name)
    except Exception as e:
        raise to_http(e)


@router.get("/projects", response_model=list[ProjectOut])
def get_projects(service: ProjectService):
    try:
        projects = service.list()
        return [ProjectOut(id=p.id, name=p.name) for p in projects]
    except Exception as e:
        raise to_http(e)


@router.get("/projects/{project_id}", response_model=ProjectOut)
def get_project_by_id(service: ProjectService, project_id: str):
    try:
        project = service.get(project_id=project_id)
        return ProjectOut(id=project.id, name=project.name)
    except Exception as e:
        raise to_http(e)


@router.post("/projects/{project_id}/tasks", status_code=201, response_model=TaskOut)
def create_task(body: TaskCreate, service: TaskService, project_id: str):
    try:
        task = service.create_task(
            project_id=project_id,
            title=body.title,
            task_type=body.task_type,
            due_date=body.due_date,
        )
        return TaskOut(
            id=task.id,
            project_id=task.project_id,
            title=task.title,
            status=task.status,
            due_date=task.due_date,
            priority_score=task.priority_score,
        )
    except Exception as e:
        raise to_http(e)


@router.get("/projects/{project_id}/tasks", response_model=list[TaskOut])
def get_tasks(service: TaskService, project_id: str):
    try:
        tasks = service.list_tasks(project_id)
        return [
            TaskOut(
                id=t.id,
                project_id=t.project_id,
                title=t.title,
                status=t.status,
                due_date=t.due_date,
                priority_score=t.priority_score,
            )
            for t in tasks
        ]
    except Exception as e:
        raise to_http(e)


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task_by_id(service: TaskService, task_id: str):
    try:
        service.delete_task(task_id)
    except Exception as e:
        raise to_http(e)
