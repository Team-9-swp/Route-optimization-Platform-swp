import threading

import pytest

from app.schemas import JobStatus
from app.store import JobStore


def test_create_job_stores_record():
    store = JobStore()
    record = store.create_job(instance={}, seed=1)
    assert record.status == JobStatus.PENDING
    assert record.job_id in store._jobs


def test_get_job_returns_record():
    store = JobStore()
    created = store.create_job(instance={}, seed=1)
    fetched = store.get_job(created.job_id)
    assert fetched is not None
    assert fetched.job_id == created.job_id


def test_get_missing_job_returns_none():
    store = JobStore()
    assert store.get_job("missing") is None


def test_update_job():
    store = JobStore()
    record = store.create_job(instance={}, seed=1)
    store.update_job(
        record.job_id,
        status=JobStatus.COMPLETED,
        result={"vehicles": []},
    )
    updated = store.get_job(record.job_id)
    assert updated.status == JobStatus.COMPLETED
    assert updated.result == {"vehicles": []}


def test_update_missing_job_does_not_raise():
    store = JobStore()
    store.update_job("missing", status=JobStatus.COMPLETED)
    assert store.get_job("missing") is None


def test_concurrent_create():
    store = JobStore()
    ids = set()
    ids_lock = threading.Lock()
    errors = []

    def worker():
        try:
            record = store.create_job(instance={}, seed=1)
            with ids_lock:
                ids.add(record.job_id)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(ids) == 100
