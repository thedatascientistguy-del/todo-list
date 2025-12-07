pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose-jenkins.yml'
        FASTAPI_URL = 'http://127.0.0.1:8000'
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
                // Stop and remove old containers
                sh 'docker compose -f $DOCKER_COMPOSE_FILE down -v'

                // Build and start containers in detached mode
                sh 'docker compose -f $DOCKER_COMPOSE_FILE up -d --build'
            }
        }

        stage('Wait for FastAPI') {
            steps {
                sh '''
                echo "Waiting for FastAPI server..."
                for i in {1..30}; do
                    curl -s $FASTAPI_URL && break
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

                # Run Selenium tests inside the container but ensure FastAPI is backgrounded
                docker exec -i webapp_jenkins bash -c "
                cd /app &&
                uvicorn main:app --host 0.0.0.0 --port 8000 & 
                SERVER_PID=$! &&
                echo 'FastAPI started with PID' $SERVER_PID &&
                sleep 5 &&
                pytest selenium-tests/test_todo_app.py --disable-warnings &&
                kill $SERVER_PID
                "
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                curl -f $FASTAPI_URL || exit 1
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
