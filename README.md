# DeploySphere

## An Integrated DevOps Platform for Automated Software Delivery, Containerisation and Deployment Orchestration

DeploySphere is a lightweight Flask dashboard project that introduces core DevOps practices through an approachable example. It demonstrates application development, Docker containerisation, automated testing, and a GitHub Actions CI pipeline that checks the application and builds its container image.

The project provides a simple, locally runnable application and independent CI pipelines in GitHub Actions and Jenkins. The pipelines run tests and build a local Docker image; they do not publish images or configure cloud deployment.

## Objectives

- Build a small Python web application with Flask.
- Package the application and dependencies into a portable Docker image.
- Run the application using Docker Compose at `http://localhost:5000`.
- Report application health through `/health` and a container health check.
- Automatically test the Flask routes and build the Docker image with GitHub Actions and Jenkins.

## Technologies

Python 3.12, Flask, HTML, CSS, minimal JavaScript, Docker, Docker Compose, pytest, GitHub Actions, and Jenkins.

## Project structure

```text
DEPLOYSPHERE/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docker-compose.jenkins.yml
├── Dockerfile.jenkins-agent
├── Jenkinsfile
├── .dockerignore
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── tests/
│   └── test_app.py
└── README.md
```

## Run locally

Use Python 3.10 or newer. From the project directory, create and activate a virtual environment, install the Flask dependency, and start the server.

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
docker build -t deploysphere:1.0.0 .
```

## Run with Docker Compose

```bash
docker compose up --build -d
```

Compose maps host port `5000` to container port `5000`. Open `http://localhost:5000` to view the dashboard.

To view container status and health:

```bash
docker compose ps
docker inspect --format='{{.State.Health.Status}}' deploysphere
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
{"application":"DeploySphere","status":"healthy","version":"1.0.0"}
```

Docker and Compose also run a health check against this endpoint. The container becomes healthy after the application responds successfully. The Docker Compose project and service are named `deploysphere`, and the standard application image is tagged `deploysphere:latest`.

## CI/CD with GitHub Actions

The workflow in `.github/workflows/ci.yml` runs automatically for each push to `main` and each pull request targeting `main`. It checks out the repository, sets up Python, installs Flask and pytest, runs the route tests, and builds a Docker image from the existing `Dockerfile`. It does not publish the image, so Docker Hub credentials are not needed.

### Run the same checks locally

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -v
docker build --tag deploysphere:ci .
```

### Trigger and inspect the workflow

Push a commit to the GitHub repository's `main` branch, or open a pull request targeting `main`. For example:

```bash
git add .
git commit -m "Add DeploySphere CI workflow"
git push origin main
```

For a pull request, push a feature branch and open a pull request with `main` as its target. In GitHub, open the repository's **Actions** tab and select **DeploySphere CI** to view the run and its test and image-build logs. A green check mark means pytest and the Docker image build passed. A failed step is marked in red and includes logs to help identify the issue.

The workflow only needs read access to repository contents. GitHub-hosted runners provide Docker; no registry login or secrets are configured in this phase.

## CI/CD with Jenkins

Jenkins provides an independent pipeline beside GitHub Actions. A Jenkins Pipeline job checks out the configured Git revision, creates a Python virtual environment on its agent, installs the existing Flask dependency and pytest, runs the existing tests, then builds the existing Dockerfile as `deploysphere:latest`. The pipeline reports each stage in the Jenkins console and marks the build successful or failed. It does not push the image and needs no Docker Hub credentials.

### Windows 11, Docker Desktop, and WSL2 Jenkins setup

The `docker-compose.jenkins.yml` starts a Jenkins controller and a separate Linux inbound build agent. Jenkins data persists in the named `jenkins_home` volume. The web UI binds to `127.0.0.1:8080` only. `Dockerfile.jenkins-agent` installs Python 3, pip, venv support, and Docker CLI on the agent; the Jenkins controller does not run builds.

The agent does **not** mount a Windows path as `/var/run/docker.sock`. Docker Desktop's daemon is in its Linux VM and Windows named-pipe paths are not Linux socket files. Instead, the agent uses Docker Desktop's host gateway (`host.docker.internal`) to reach the Linux daemon's optional TCP endpoint at port 2375. This avoids an incorrect socket bind mount, but the unauthenticated TCP endpoint gives clients powerful Docker host access. It must only be enabled for a trusted local demo; do not expose port 2375 to a network. If you do not accept that local risk, use a dedicated Linux VM/WSL distribution with Docker Engine and a protected socket, and connect a Jenkins agent there.

#### Configure Docker Desktop

1. In Docker Desktop, open **Settings → General** and enable **Expose daemon on tcp://localhost:2375 without TLS**. Docker Desktop describes this as an insecure option. Use it only on this trusted workstation and disable it after the demo if it is not otherwise needed.
2. Confirm Docker Desktop is using the **WSL 2 based engine** and that `docker info` works in PowerShell.
3. Do not publish, forward, or firewall-open port 2375. The Jenkins agent reaches it through the Docker Desktop host gateway from the local Compose network.

#### Configure Jenkins controller and agent

1. Start the controller first from PowerShell in the repository directory:

   ```powershell
   docker compose -f docker-compose.jenkins.yml up -d jenkins
   docker compose -f docker-compose.jenkins.yml logs -f jenkins
   ```

2. Open `http://127.0.0.1:8080`, complete the setup wizard, and install the suggested plugins. Minimum plugins are **Pipeline** (including Declarative Pipeline support) and **Git**. The built-in inbound agent/WebSocket support is part of Jenkins core; no Docker Pipeline plugin is needed because the Jenkinsfile invokes the Docker CLI. Webhook integration is optional and may use **GitHub** plugin support.
3. In **Manage Jenkins → Nodes → New Node**, create a permanent node named exactly `deploysphere-agent`. Set **Number of executors** to `1`, **Remote root directory** to `/home/jenkins/agent`, and **Labels** to `deploysphere-agent`. Choose **Launch method: Launch agent by connecting it to the controller** (inbound) and enable WebSocket if that option is shown. Save the node and copy its generated secret from the node page.
4. Create a local, Git-ignored `.env.jenkins-agent` file in the repository root and put the secret copied from the Jenkins node page there. Do not paste it into Compose, the Jenkinsfile, or a committed file. For example, create it with PowerShell (the prompt keeps the value out of shell history):

   ```powershell
   $secret = Read-Host 'Paste deploysphere-agent secret'
   Set-Content -Path .env.jenkins-agent -Value "JENKINS_SECRET=$secret"
   Remove-Variable secret
   docker compose -f docker-compose.jenkins.yml up -d --build agent
   docker compose -f docker-compose.jenkins.yml logs -f agent
   ```

5. Wait until the node is online in Jenkins. The agent image is built locally from `Dockerfile.jenkins-agent`; it contains the tools used by the pipeline.

#### Verify agent tools and Docker connection

After it is online, run these read-only checks from PowerShell:

```powershell
docker compose -f docker-compose.jenkins.yml exec agent python3 --version
docker compose -f docker-compose.jenkins.yml exec agent python3 -m pip --version
docker compose -f docker-compose.jenkins.yml exec agent python3 -m venv --help
docker compose -f docker-compose.jenkins.yml exec agent docker --version
docker compose -f docker-compose.jenkins.yml exec agent sh -lc 'DOCKER_HOST=tcp://host.docker.internal:2375 docker info --format "{{.OSType}}"'
```

The last command must print `linux`. The Docker CLI is configured in the Jenkinsfile with `DOCKER_HOST=tcp://host.docker.internal:2375` for the image build, so the image is built by Docker Desktop's daemon and stored in its image store. No Docker socket is mounted and no world-writable socket permissions are used.

### Create and run a Pipeline job

1. In Jenkins, choose **New Item**, enter a job name, select **Pipeline**, then choose **OK**.
2. In the job configuration, under **Pipeline**, set **Definition** to **Pipeline script from SCM** and **SCM** to **Git**. Ensure the job is configured to run on the `deploysphere-agent` label; the Jenkinsfile itself requests that label.
3. Set the repository URL to `https://github.com/meghana-dscse/DEPLOYLITE` (the current repository URL). Set **Branch Specifier** to `*/main` (or the branch you want to build) and **Script Path** to `Jenkinsfile`.
4. Save the job and click **Build Now** to start a manual run. No GitHub credentials are needed for a public repository. If it is private, add a read-only credential in Jenkins and select it in the job; never put a token in the Jenkinsfile or README.
5. Open the build number and select **Console Output** to inspect checkout, setup, test, and Docker build logs. The stage view shows success or failure for each stage. A green result means the image was built in Docker Desktop's daemon through the local TCP endpoint.

### Optional automatic triggers

To poll for changes, enable **Poll SCM** in the job's **Build Triggers** (for example, schedule `H/5 * * * *`). For webhook triggering, configure a GitHub webhook to the Jenkins endpoint and enable the corresponding GitHub hook trigger in Jenkins. A public GitHub webhook requires a reachable Jenkins endpoint; do not expose this local Jenkins instance publicly for a classroom demo. Prefer manual builds or polling for local use. Webhook setup may require additional Jenkins plugins and network configuration.

### Troubleshooting Jenkins

- **`docker: not found`:** Install Docker CLI on the pipeline agent and ensure it is on `PATH`.
- **Cannot connect to Docker daemon:** Confirm Docker Desktop's insecure localhost TCP setting is enabled, the agent can resolve `host.docker.internal`, and the agent-side `docker info` check succeeds. Do not expose port 2375 externally.
- **`python3: not found` or venv creation fails:** Install Python 3, pip, and the venv package on the agent, then ensure `python3` is on `PATH`.
- **Git checkout fails:** Confirm the repository URL and branch. For private repositories, configure a Jenkins SCM credential with read access.
- **Tests fail:** Open **Console Output** and reproduce with `python -m pytest -v` in a local virtual environment.
- **Docker build fails:** Inspect the build output and verify the agent's Docker daemon is running and can access the checkout workspace.
- **Compose port conflict:** Stop the conflicting service or choose another loopback-only host port in the Jenkins Compose file.

Stop the controller and agent while retaining Jenkins data:

```bash
docker compose -f docker-compose.jenkins.yml down
```

The `jenkins_home` volume persists through shutdown. Removing it with `docker compose -f docker-compose.jenkins.yml down -v` permanently deletes Jenkins jobs and configuration; use that only when intentionally resetting the demo.

## Rename the existing GitHub repository

The project files do not contain a hard-coded GitHub repository URL. Rename the existing GitHub repository to `DEPLOYSPHERE`; no new repository is needed.

Rename the existing repository (do not create another one) in GitHub:

1. Open the current repository and select **Settings**.
2. In **General**, change the repository name to `DEPLOYSPHERE` and save the change.
3. Update the local remote from the project directory:

   ```bash
   git remote set-url origin https://github.com/meghana-dscse/DEPLOYSPHERE.git
   git remote -v
   ```

GitHub normally redirects requests to the old repository URL, but update local remotes and any external bookmarks or integrations to use the new URL.
