import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import delete, select, update

from app.db import JobModel, async_session_maker
from app.schemas import JobRecord, JobStatus, ValidationStatus


class JobRepository:
    async def create_job(
        self,
        instance: dict,
        seed: int,
        name: str | None = None,
        time_limit: float | None = None,
    ) -> JobRecord:
        job_id = str(uuid.uuid4())
        record = JobRecord(
            job_id=job_id,
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
            name=name,
            input_data=instance,
            seed=seed,
            time_limit=time_limit,
        )
        async with async_session_maker() as session:
            session.add(JobRepository._to_model(record))
            await session.commit()
        return record

    async def get_job(self, job_id: str) -> JobRecord | None:
        async with async_session_maker() as session:
            result = await session.execute(select(JobModel).where(JobModel.job_id == job_id))
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return JobRepository._from_model(row)

    async def list_jobs(
        self,
        *,
        page: int = 1,
        page_size: int = 25,
        sort_desc: bool = True,
    ) -> tuple[list[JobRecord], int]:
        async with async_session_maker() as session:
            total_result = await session.execute(select(JobModel.job_id))
            total = len(total_result.scalars().all())

            order = JobModel.created_at.desc() if sort_desc else JobModel.created_at.asc()
            offset = (page - 1) * page_size
            result = await session.execute(
                select(JobModel)
                .order_by(order)
                .offset(offset)
                .limit(page_size)
            )
            rows = result.scalars().all()
            return [JobRepository._from_model(row) for row in rows], total

    async def update_job(
        self,
        job_id: str,
        *,
        status: JobStatus | None = None,
        name: str | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        result: dict | None = None,
        error: str | None = None,
        objective_value: float | None = None,
        validation_status: ValidationStatus | None = None,
        validation_report: dict | None = None,
    ) -> None:
        values: dict[str, Any] = {}
        if status is not None:
            values["status"] = status.value
        if name is not None:
            values["name"] = name
        if started_at is not None:
            values["started_at"] = started_at
        if finished_at is not None:
            values["finished_at"] = finished_at
        if result is not None:
            values["result"] = result
        if error is not None:
            values["error"] = error
        if objective_value is not None:
            values["objective_value"] = objective_value
        if validation_status is not None:
            values["validation_status"] = validation_status.value
        if validation_report is not None:
            values["validation_report"] = validation_report

        if not values:
            return

        async with async_session_maker() as session:
            await session.execute(
                update(JobModel).where(JobModel.job_id == job_id).values(**values)
            )
            await session.commit()

    @staticmethod
    def _to_model(record: JobRecord) -> JobModel:
        return JobModel(
            job_id=record.job_id,
            status=record.status.value,
            name=record.name,
            created_at=record.created_at,
            started_at=record.started_at,
            finished_at=record.finished_at,
            seed=record.seed,
            time_limit=record.time_limit,
            input_data=record.input_data,
            result=record.result,
            error=record.error,
            objective_value=record.objective_value,
            validation_status=record.validation_status.value if record.validation_status else None,
            validation_report=record.validation_report,
        )

    @staticmethod
    def _from_model(row: JobModel) -> JobRecord:
        return JobRecord(
            job_id=row.job_id,
            status=JobStatus(row.status),
            name=row.name,
            created_at=row.created_at,
            started_at=row.started_at,
            finished_at=row.finished_at,
            seed=row.seed,
            time_limit=row.time_limit,
            input_data=row.input_data or {},
            result=row.result,
            error=row.error,
            objective_value=row.objective_value,
            validation_status=ValidationStatus(row.validation_status) if row.validation_status else None,
            validation_report=row.validation_report,
        )

    async def clear_all(self) -> None:
        """Test helper to empty the jobs table."""
        async with async_session_maker() as session:
            await session.execute(delete(JobModel))
            await session.commit()
