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
                sh 'docker compose -f docker-compose.integration.yml build'
            }
        }

        stage('Start Integration Environment') {
            steps {
                echo 'Start KAIRON integration environment'
                sh 'docker compose -f docker-compose.integration.yml up -d'
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'Check KAIRON health endpoint'
                sh 'python - <<PY\nimport urllib.request\nimport json\nresponse = urllib.request.urlopen("http://kairon-app-int:5000/health")\ndata = json.loads(response.read().decode())\nassert data["status"] == "ok"\nprint("KAIRON health check OK")\nPY'
            }
        }

        stage('Regression Tests') {
            steps {
                echo 'Run regression tests'
                sh 'docker compose -f docker-compose.integration.yml exec -T kairon-app pytest tests/regression'
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