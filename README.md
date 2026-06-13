# Route Optimization Platform

A logistics optimization system that generates vehicle and loader routes for the BIA CVRPTW problem variant. The project provides an asynchronous REST solver service and a planned React web interface.

## Quick start

A hosted instance is available at `http://10.93.26.188:8000` from the university network (Swagger UI at `/docs`).

To run locally, use Docker Compose:

```bash
docker compose up --build
```

Then open Swagger UI at `http://localhost:8000/docs`.

## Local development

### Backend

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the API:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

4. Submit a test instance:

   ```bash
   curl -X POST "http://localhost:8000/solve?seed=42" \
        -H "Content-Type: application/json" \
        -d @test_cases/t1.json
   ```

### Frontend (planned)

A React + TypeScript SPA is planned for MVP v1.

## Assignment reports

- [Week 2 report index](./reports/week2/README.md)
- [MVP v0 report](./reports/week2/mvp-v0-report.md)
- [User stories](./reports/week2/user-stories.md)

## License

[MIT](./LICENSE)
