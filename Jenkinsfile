pipeline {
    // This label is provided by the dedicated agent in docker-compose.jenkins.yml.
    agent { label 'deploysphere-agent' }

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    environment {
        // Docker Desktop's local TCP endpoint; enable it in Docker Desktop settings.
        DOCKER_HOST = 'tcp://host.docker.internal:2375'
    }

    stages {
        stage('Checkout') {
            steps {
                // In a Pipeline-from-SCM job, this retrieves the configured repository revision.
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    set -eu
                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt pytest
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    set -eu
                    . .venv/bin/activate
                    python -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --tag deploysphere:latest .'
            }
        }
    }

    post {
        success {
            echo 'All stages succeeded: tests passed and deploysphere:latest was built.'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above to locate the failed step.'
        }
        always {
            echo "Pipeline result: ${currentBuild.currentResult}"
        }
    }
}
