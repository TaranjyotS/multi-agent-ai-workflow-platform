pipeline {
    agent any

    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Setup') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }
        stage('Lint') { steps { sh '. .venv/bin/activate && ruff check app tests' } }
        stage('Test') { steps { sh '. .venv/bin/activate && pytest -q' } }
        stage('Security') { steps { sh '. .venv/bin/activate && bandit -r app -c pyproject.toml' } }
        stage('Docker Build') { steps { sh 'docker build -t multi-agent-ai-workflow-platform:jenkins .' } }
    }
}
