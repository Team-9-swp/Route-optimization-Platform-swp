# Route Optimization Platform

A logistics optimization system that generates vehicle and loader routes for the BIA CVRPTW problem variant. The project provides an asynchronous REST solver service and a React web interface.

## Quick start

Run the whole stack with Docker Compose:

```bash
docker compose up --build
```

Then open:

- Swagger UI: `http://localhost:8000/docs`
- Web interface: `http://localhost:3000`

## Deployment

### Production (Docker Compose)

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

The `docker-compose.prod.yml` override adds `restart: unless-stopped` policies and production environment settings.

### Remote access via ngrok

Share the running stack with the customer or TA over the internet:

```bash
ngrok http 3000
```

Then share the generated `https://*.ngrok-free.app` URL. The nginx proxy forwards `/api/` requests to the backend automatically.

### Stopping

```bash
docker compose down
```

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
   curl -X POST "http://localhost:8000/solve?seed=42&time_limit=2&max_restarts=3" \
        -H "Content-Type: application/json" \
        -d @test_cases/t1.json
   ```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite dev server proxies `/api` to `http://localhost:8000`.

## Assignment reports

- [Week 2 report index](./reports/week2/README.md)
- [MVP v0 report](./reports/week2/mvp-v0-report.md)
- [MVP v1 report](./reports/week3/README.md)
- [User-stories](docs/user-stories.md)

## License

[MIT](./LICENSE)
