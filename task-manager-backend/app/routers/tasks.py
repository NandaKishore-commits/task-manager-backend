"""Task endpoints."""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def _get_or_404(db: Session, task_id: int):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Task {task_id} not found")
    return task


@router.post("", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data)


@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(
    status_filter: Literal["all", "completed", "pending"] = Query("all", alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.get_tasks(db, status_filter, skip, limit)


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, task_id)


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db, _get_or_404(db, task_id), data)


@router.patch("/{task_id}/toggle", response_model=schemas.TaskOut)
def toggle_completed(task_id: int, db: Session = Depends(get_db)):
    task = _get_or_404(db, task_id)
    return crud.update_task(db, task, schemas.TaskUpdate(completed=not task.completed))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    crud.delete_task(db, _get_or_404(db, task_id))
