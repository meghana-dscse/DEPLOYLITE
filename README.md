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
