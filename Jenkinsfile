pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout SCM') {
            steps {
                checkout scm
                sh 'git rev-parse --abbrev-ref HEAD || true'
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Docker Version') {
            steps {
                sh 'docker version'
            }
        }

        stage('Build Pipeline Environment') {
            steps {
                sh 'docker compose -f docker-compose.pipeline.yml build'
            }
        }

        stage('Start Pipeline Environment') {
            steps {
                sh 'docker compose -f docker-compose.pipeline.yml up -d'
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'docker compose -f docker-compose.pipeline.yml exec -T kairon-app python -c "import urllib.request, json; r=urllib.request.urlopen(\"http://localhost:5000/health\"); d=json.loads(r.read().decode()); assert d[\"status\"] == \"ok\"; print(\"KAIRON health check OK\")"'
            }
        }

        stage('Regression Tests') {
            steps {
                sh 'docker compose -f docker-compose.pipeline.yml exec -T kairon-app pytest tests/regression'
            }
        }
    }

    post {
        always {
            sh 'docker compose -f docker-compose.pipeline.yml down -v || true'
        }

        success {
            echo 'Pipeline succeeded - checked-out SCM branch is valid'
        }

        failure {
            echo 'Pipeline failed - deployment must not continue'
        }
    }
}
