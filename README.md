# DeploySphere
### An Integrated DevOps Platform for Automated Software Delivery, Containerisation and Deployment Orchestration

DeploySphere is a lightweight DevOps project that demonstrates how a Python web application can move from source code to a tested, containerised and running application through an automated software delivery workflow.

The project integrates Git, GitHub, GitHub Actions, Jenkins, pytest, Docker and Docker Compose to demonstrate version control, Continuous Integration (CI), automated testing, container image creation and local application deployment.

---

## 1. Project Overview

Traditional software delivery involves several manual activities, including maintaining source code, testing applications, building deployment packages and configuring runtime environments.

DeploySphere demonstrates how these activities can be organised into a repeatable workflow using DevOps tools.

A Flask-based web application serves as the application being deployed. GitHub maintains the source code, GitHub Actions and Jenkins define separate CI pipelines, pytest validates application functionality, and Docker packages the application into a portable container.

Docker Compose simplifies running and managing the application.

### Project Objectives

- Implement version control using Git and GitHub.
- Automate code validation and testing through CI pipelines.
- Integrate Jenkins for pipeline execution.
- Perform application testing using pytest.
- Containerise the Flask application using Docker.
- Manage local application startup using Docker Compose.
- Provide a health-check endpoint to monitor application availability.

---

## 2. Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| Programming Language | Python | Application development |
| Web Framework | Flask | Backend application |
| Version Control | Git | Source code management |
| Repository Hosting | GitHub | Remote repository |
| Continuous Integration | GitHub Actions | Automated CI workflow |
| Continuous Integration | Jenkins | Independent pipeline automation |
| Testing | pytest | Automated application testing |
| Containerisation | Docker | Application packaging |
| Container Management | Docker Compose | Local container startup and management |
| Frontend | HTML, CSS, JavaScript | Dashboard interface |

---

## 3. System Architecture

The project follows a source-to-container workflow. GitHub Actions and Jenkins are independent CI pipelines; each checks out the source, runs tests, and builds an image. Docker Compose runs the application locally.

```text
                 Developer
                     |
                     v
                Git / GitHub
                     |
          +----------+----------+
          |                     |
          v                     v
    GitHub Actions           Jenkins
          |                     |
          |              Jenkins Controller
          |                     |
          |                Jenkins Agent
          |                     |
          +----------+----------+
                     |
                     v
              Automated Testing
                  (pytest)
                     |
                     v
              Docker Image Build
                     |
                     v
             Docker Container
                     |
                     v
             Docker Compose
                     |
                     v
            Flask Web Application
                     |
             +-------+-------+
             |               |
             v               v
          Dashboard       /health
```

The Jenkins agent requires a local Docker daemon connection to build the image. Jenkins controller and agent setup is documented below; successful connection depends on the local Jenkins node and Docker Desktop configuration.

---

## 4. Features and Implementation

### 4.1 Flask Web Application

A lightweight Flask application acts as the main application being deployed.

It includes:
- A responsive deployment dashboard.
- Application status information.
- Application version and runtime details.
- A health-check endpoint.
- A simple interface explaining the deployment workflow.

**Application endpoints:**

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Displays the DeploySphere dashboard |
| `/health` | GET | Returns the application health status in JSON format |

### 4.2 Version Control Using Git and GitHub

Git is used to maintain the application's source code and track changes.

GitHub hosts the project repository and acts as the central source-code repository for the CI workflows. The primary workflow targets the `main` branch.

### 4.3 Continuous Integration Using GitHub Actions

GitHub Actions automates the CI process. The workflow is defined in `.github/workflows/ci.yml` and runs on pushes to `main` and pull requests targeting `main`.

The workflow performs the following activities:

1. Checks out the source code.
2. Sets up Python.
3. Installs Flask from `requirements.txt` and pytest.
4. Executes automated tests.
5. Builds the Docker image tagged `deploysphere:ci`.

The workflow does not publish the image to a registry and requires no Docker Hub credentials.

### 4.4 Continuous Integration Using Jenkins

Jenkins provides an additional CI pipeline. The pipeline configuration is maintained in the root-level `Jenkinsfile`.

**Pipeline stages:**

| Stage | Description |
|---|---|
| Checkout | Retrieves the project source code from the configured Git SCM job |
| Setup Python | Creates a virtual environment and installs dependencies and pytest |
| Test | Executes the pytest test cases |
| Build Docker Image | Builds the application image tagged `deploysphere:latest` |

The Jenkins setup consists of a controller, a dedicated inbound agent, the Jenkinsfile, and Docker CLI access from the agent to the local Docker daemon. The controller and agent are configured separately from the application using `docker-compose.jenkins.yml` and `Dockerfile.jenkins-agent`. No image is pushed to Docker Hub.

### 4.5 Automated Testing Using pytest

pytest validates the Flask application's functionality. The tests cover homepage rendering and the health endpoint.

Install the application dependency and pytest, then run:

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -v
```

### 4.6 Containerisation Using Docker

Docker packages the Flask application and its runtime dependency into an image. The `Dockerfile` defines the application environment, dependency installation and startup configuration.

Build the standard image using:

```bash
docker build --tag deploysphere:latest .
```

GitHub Actions uses the CI tag `deploysphere:ci`; Jenkins uses `deploysphere:latest`.

### 4.7 Container Deployment Using Docker Compose

The application configuration is maintained in `docker-compose.yml`. It builds from the existing Dockerfile, names the service and container `deploysphere`, maps port `5000`, sets the application port, and configures a health check against `/health`.

Start the application with:

```bash
docker compose up --build -d
```

The application is available at `http://localhost:5000`. Compose periodically checks the container health endpoint.

---

## 5. Project Structure

```text
DeploySphere/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── templates/
│   └── index.html
│
├── tests/
│   └── test_app.py
│
├── app.py
├── requirements.txt
├── Dockerfile
├── Dockerfile.jenkins-agent
├── docker-compose.yml
├── docker-compose.jenkins.yml
├── Jenkinsfile
├── .dockerignore
├── .gitignore
└── README.md
```

**Important configuration files:**

| File | Responsibility |
|---|---|
| `app.py` | Flask application and routes |
| `requirements.txt` | Application Python dependencies |
| `Dockerfile` | Application Docker image configuration |
| `docker-compose.yml` | Application container configuration |
| `Jenkinsfile` | Jenkins CI pipeline |
| `docker-compose.jenkins.yml` | Jenkins controller and agent setup |
| `Dockerfile.jenkins-agent` | Custom Jenkins agent image with Python and Docker CLI |
| `.github/workflows/ci.yml` | GitHub Actions CI workflow |
| `tests/test_app.py` | Automated test cases |

The local `.env.jenkins-agent` file is intentionally not included in the repository structure because it contains the Jenkins agent secret and is ignored by Git.

---

## 6. Installation and Execution

### Prerequisites

- Python 3
- Git
- Docker Desktop with its Linux engine
- Docker Compose v2

Jenkins is optional when running only the Flask application. Jenkins setup is covered in Section 7.

### Step 1: Clone the Repository

The current repository URL remains:

```bash
git clone https://github.com/meghana-dscse/DEPLOYLITE.git
```

Navigate into the cloned directory:

```bash
cd DEPLOYLITE
```

### Step 2: Install Python Dependencies

```bash
python -m venv venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies and pytest:

```powershell
python -m pip install -r requirements.txt pytest
```

### Step 3: Run the Application Locally

```bash
python app.py
```

Open `http://localhost:5000` and check `http://localhost:5000/health`.

### Step 4: Run Automated Tests

```bash
python -m pytest -v
```

### Step 5: Build and Run Using Docker Compose

Build and start the application:

```bash
docker compose up --build -d
```

Check the running container and health:

```bash
docker compose ps
docker inspect --format='{{.State.Health.Status}}' deploysphere
```

The dashboard is available at `http://localhost:5000` and the health endpoint at `http://localhost:5000/health`.

Stop the application:

```bash
docker compose down
```

---

## 7. Jenkins Setup

Jenkins is configured separately from the application. On Windows 11 with Docker Desktop and WSL2, the Compose file starts the controller and a dedicated agent. The controller UI binds to localhost port `8080`; controller data persists in the `jenkins_home` volume.

The Jenkinsfile uses Docker Desktop's TCP endpoint at `tcp://host.docker.internal:2375`. On Windows 11 with Docker Desktop, enable **Expose daemon on tcp://localhost:2375 without TLS** in Docker Desktop settings for this local demonstration. This endpoint provides powerful Docker host control; keep it on a trusted workstation, never expose it to an untrusted network, and disable it when no longer needed.

Start the controller first from PowerShell in the project directory:

```powershell
docker compose -f docker-compose.jenkins.yml up -d jenkins
```

Open `http://localhost:8080`, complete the setup wizard, and install at least the Jenkins **Pipeline** and **Git** plugins (the suggested plugins include these capabilities). Create a permanent inbound node named `deploysphere-agent`, with one executor, remote root `/home/jenkins/agent`, and label `deploysphere-agent`. Use the inbound TCP launch method and configure the agent port as `50000` in Jenkins. The current `docker-compose.jenkins.yml` does not publish port `50000`; for standard inbound TCP from the Compose agent, add a controller port mapping for `50000:50000` and ensure Jenkins is configured to use that fixed agent port before starting the agent.

Copy the generated secret for that node into the Git-ignored local file `.env.jenkins-agent`. Do not commit the file or place the secret in source code. Then build and start the agent:

```powershell
docker compose -f docker-compose.jenkins.yml up -d --build agent
docker compose -f docker-compose.jenkins.yml logs -f agent
```

Wait for `deploysphere-agent` to show as online in Jenkins. The agent contacts the controller at `http://jenkins:8080` and uses the configured inbound tunnel `jenkins:50000`.

Create a Jenkins Pipeline job with:

- Pipeline definition: **Pipeline script from SCM**.
- SCM: **Git**.
- Repository URL: `https://github.com/meghana-dscse/DEPLOYLITE.git`.
- Branch: `*/main`.
- Script path: `Jenkinsfile`.

Save the job and select **Build Now**. Inspect each stage and logs in the build page and **Console Output**. Jenkins execution requires the agent to be online and its Docker CLI to reach the configured Docker Desktop daemon.

---

## 8. Verification and Testing

The repository contains two pytest tests. To perform the checks locally, use the commands in Sections 6 and 7. A test or build result depends on the current local environment; this README does not assert that a Jenkins agent connection or a Jenkins pipeline run has succeeded.

| Verification | How to check |
|---|---|
| Flask homepage | `http://localhost:5000` returns the dashboard |
| Flask health endpoint | `http://localhost:5000/health` returns HTTP 200 JSON |
| pytest tests | `python -m pytest -v` |
| Docker image build | `docker build --tag deploysphere:latest .` |
| Application Compose configuration | `docker compose config` |
| Jenkins Compose configuration | `docker compose -f docker-compose.jenkins.yml config` (requires local `.env.jenkins-agent`) |
| GitHub Actions workflow | Inspect `.github/workflows/ci.yml` and the repository Actions tab after a push or pull request |
| Jenkins agent and pipeline | Confirm the node is online, then run the Pipeline job and inspect its stage results |

---

## 9. Security and Configuration

- `.gitignore` excludes `.env`, `.env.jenkins-agent`, credentials and secret-like files, Python caches, and virtual environments.
- Keep the Jenkins agent secret in the local ignored `.env.jenkins-agent` file. Never commit or share its value.
- Jenkins is bound to localhost for local use. Do not expose the Jenkins UI or Docker daemon endpoint to an untrusted network.
- Docker daemon access can grant broad host control; use the Jenkins agent only with trusted pipeline code.

---

## 10. Current Scope and Future Enhancements

### Implemented

- Flask dashboard and `/health` endpoint.
- pytest route tests.
- Docker image build and local Docker Compose application configuration.
- GitHub Actions workflow that runs tests and builds an image on pushes and pull requests targeting `main`.
- Jenkinsfile stages for checkout, Python setup, testing, and local Docker image build.
- Separate Jenkins controller and build-agent configuration files.

The Jenkins files are provided, but a Jenkins pipeline run succeeds only after Jenkins plugins, the inbound node, its secret, and Docker daemon connectivity are configured locally.

### Future enhancements (not implemented)

- Deployment to Azure Container Instances (ACI).
- Kubernetes-based container orchestration.
- Docker Swarm.
- Infrastructure and configuration management using Ansible.
- Puppet-based configuration management.
- SaltStack-based automation.
- Automated cloud deployment and release management.

---

## 11. Conclusion

DeploySphere demonstrates an approachable DevOps workflow that combines source-code management, CI pipelines, automated testing, containerisation, and local application deployment.

GitHub Actions and Jenkins provide separate paths for testing and building the Docker image. Docker and Docker Compose package and run the Flask application locally. The project can be extended later with cloud deployment, infrastructure automation, or advanced container orchestration.

---

**Project:** DeploySphere

**Project Category:** DevOps and Software Delivery Automation

**Primary Technologies:** Python, Flask, Git, GitHub, GitHub Actions, Jenkins, pytest, Docker and Docker Compose.
