# DeployLite

DeployLite is a small Flask dashboard that demonstrates packaging and running a web application in an isolated Docker container. It includes a live status view, runtime details, a `/health` endpoint, and a short overview of the deployment workflow.

## Objectives

- Build a lightweight Python web application with Flask.
- Package the application and its dependencies into a Docker image.
- Run it consistently with Docker Compose and expose it at `http://localhost:5000`.
- Report application health with an HTTP endpoint and container health check.

## Technologies

Python 3.12, Flask, HTML, CSS, minimal JavaScript, Docker, and Docker Compose.

## Project structure

```text
DeployLite/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── tests/
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## Run locally

Use Python 3.10 or newer. From the project directory, create and activate a virtual environment, then install Flask and start the server.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`. Stop the local server with `Ctrl+C`.

## Build a Docker image

Run from the project directory:

```bash
docker build -t deploylite:1.0.0 .
```

## Run with Docker Compose

```bash
docker compose up --build -d
```

Compose maps host port `5000` to container port `5000`. Open `http://localhost:5000` to view the dashboard.

To view container status and health:

```bash
docker compose ps
docker inspect --format='{{.State.Health.Status}}' deploylite
```

Stop and remove the container:

```bash
docker compose down
```

## Verify the application

Open `http://localhost:5000/health` or run:

```bash
curl http://localhost:5000/health
```

The endpoint returns HTTP 200 and a JSON response similar to:

```json
{"application":"DeployLite","status":"healthy","version":"1.0.0"}
```

Docker and Compose also run a health check against this endpoint. The container becomes healthy after the application responds successfully.

## CI/CD with GitHub Actions

The workflow in `.github/workflows/ci.yml` runs automatically for each push to `main` and each pull request targeting `main`. It checks out the repository, sets up Python, installs Flask and pytest, runs the route tests, and builds the Docker image from the existing `Dockerfile`. It does not publish the image, so Docker Hub credentials are not needed.

### Run the same checks locally

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -v
docker build --tag deploylite:ci .
```

### Trigger and inspect the workflow

1. Push a commit to the GitHub repository's `main` branch, or open a pull request with `main` as its target. For example:

   ```bash
   git add .
   git commit -m "Add DeployLite CI workflow"
   git push origin main
   ```

   To use a pull request instead, push a feature branch and open a pull request targeting `main`.
2. In GitHub, open the repository's **Actions** tab and select **DeployLite CI** to view the run and its test and image-build logs.
3. A green check mark means both pytest and the Docker image build passed. A failed step is marked in red and includes logs to help locate the issue.

The workflow only needs read access to repository contents. GitHub-hosted runners provide Docker, and no registry login or secrets are configured in this phase.
