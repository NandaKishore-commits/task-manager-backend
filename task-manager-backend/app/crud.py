"""Database operations, kept separate from the API layer."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_tasks(db: Session, status: str = "all", skip: int = 0, limit: int = 100):
    stmt = select(models.Task).order_by(models.Task.id.desc())
    if status == "completed":
        stmt = stmt.where(models.Task.completed.is_(True))
    elif status == "pending":
        stmt = stmt.where(models.Task.completed.is_(False))
    return db.scalars(stmt.offset(skip).limit(limit)).all()


def get_task(db: Session, task_id: int):
    return db.get(models.Task, task_id)


def create_task(db: Session, data: schemas.TaskCreate):
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: models.Task, data: schemas.TaskUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()
