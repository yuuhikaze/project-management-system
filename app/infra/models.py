from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.db import Base


class ProjectModel(Base):
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # a project has multiple tasks
    tasks: Mapped[list["TaskModel"]] = relationship(
        # fill with table project
        back_populates="project",
        # on project deletion, delete all related takss and orphans
        cascade="all,delete-orphan",
    )


class TaskModel(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(
        String, ForeignKey("projects.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)

    tasks_type: Mapped[str] = mapped_column(String, nullable=False)
    # a task has a single project
    project: Mapped["ProjectModel"] = relationship(
        # fill with table tasks
        back_populates='tasks'
    )
