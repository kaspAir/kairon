pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checkout source code'
                checkout scm
            }
        }

        stage('Build Docker Environment') {
            steps {
                echo 'Build KAIRON integration environment'
                bat 'docker compose -f docker-compose.integration.yml build'
            }
        }

        stage('Start Integration Environment') {
            steps {
                echo 'Start KAIRON integration environment'
                bat 'docker compose -f docker-compose.integration.yml up -d'
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'Check KAIRON health endpoint'
                bat 'powershell -Command "Invoke-RestMethod http://localhost:5000/health"'
            }
        }

        stage('Regression Tests') {
            steps {
                echo 'Run regression tests'
                bat 'docker compose -f docker-compose.integration.yml exec -T kairon-app pytest tests/regression'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }

        failure {
            echo 'Pipeline failed - deployment must not continue'
        }

        success {
            echo 'Pipeline succeeded - integration environment is valid'
        }
    }
}