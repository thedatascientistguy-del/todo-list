pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose-jenkins.yml'
    }

    stages {

        stage('Clean Workspace') {
            steps {
                echo "Cleaning workspace..."
                deleteDir()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'jenkins',
                    url: 'https://github.com/thedatascientistguy-del/todo-list.git'
            }
        }

        stage('Pre-checks') {
            steps {
                sh 'docker --version'
                sh 'docker compose version'
            }
        }

        stage('Build and Run Docker Containers') {
            steps {
                sh 'docker compose -f $DOCKER_COMPOSE_FILE down -v'
                sh 'docker compose -f $DOCKER_COMPOSE_FILE up -d --build'
            }
        }

        stage('Wait for FastAPI') {
            steps {
                sh '''
                echo "Waiting for FastAPI server..."
                for i in {1..30}; do
                    curl -s http://127.0.0.1:8000/ && break
                    echo "Server not ready, retrying..."
                    sleep 2
                done
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                echo "Running Selenium tests..."
                docker exec -i webapp_jenkins bash -c "
                cd /app &&
                pytest selenium-tests/test_todo_app.py --disable-warnings
                "
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                curl -f http://127.0.0.1:8000 || exit 1
                echo "FastAPI app is running!"
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
            sh 'docker ps -a'
            sh 'docker compose -f $DOCKER_COMPOSE_FILE logs --tail=100'
        }
    }
}
