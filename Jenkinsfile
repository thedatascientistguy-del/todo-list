pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose-jenkins.yml'
        FASTAPI_URL = 'http://127.0.0.1:8000'
        SELENIUM_CONTAINER = 'webapp_jenkins'
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
                echo "Checking Docker versions..."
                sh 'docker --version'
                sh 'docker compose version'
            }
        }

        stage('Build and Run Docker Containers') {
            steps {
                echo "Stopping and removing old containers..."
                sh 'docker compose -f $DOCKER_COMPOSE_FILE down -v || true'

                echo "Building and starting containers..."
                sh 'docker compose -f $DOCKER_COMPOSE_FILE up -d --build'
            }
        }

        stage('Wait for FastAPI') {
            steps {
                echo "Waiting for FastAPI to be ready..."
                sh '''
                for i in $(seq 1 30); do
                    if curl -s $FASTAPI_URL > /dev/null; then
                        echo "FastAPI is ready!"
                        break
                    fi
                    echo "Server not ready, retrying..."
                    sleep 2
                done
                if ! curl -s $FASTAPI_URL > /dev/null; then
                    echo "FastAPI did not start in time!"
                    exit 1
                fi
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium tests inside container..."
                sh """
                docker exec -i $SELENIUM_CONTAINER bash -c '
                    cd /app &&
                    # Ensure Chrome runs in headless mode
                    pytest selenium-tests/test_todo_app.py --disable-warnings
                '
                """
            }
        }

        stage('Smoke Test') {
            steps {
                echo "Checking FastAPI endpoint..."
                sh '''
                curl -f $FASTAPI_URL || exit 1
                echo "FastAPI app is running!"
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished! Checking container statuses and logs...'
            sh 'docker ps -a'
            sh 'docker compose -f $DOCKER_COMPOSE_FILE logs --tail=100'
        }
    }
}
