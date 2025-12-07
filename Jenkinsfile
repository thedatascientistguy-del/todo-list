pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose-jenkins.yml'
    }

    stages {

        stage('Clean Workspace') {
            steps {
                echo "Cleaning workspace..."
                deleteDir()  // wipes the entire Jenkins workspace
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
                
                // Build and start containers
                sh 'docker compose -f $DOCKER_COMPOSE_FILE up -d --build'
            }
        }

        stage('Test') {
            steps {
                // Run tests inside the webapp container
                sh '''
                docker exec -i webapp_jenkins bash -c "pip install --no-cache-dir -r requirements.txt && pytest"
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                // Check if the FastAPI app is up
                sh '''
                curl -f http://localhost:8000 || exit 1
                echo "FastAPI app is running!"
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'

            // Show running containers
            sh 'docker ps -a'

            // Show latest logs from docker-compose services
            sh 'docker compose -f $DOCKER_COMPOSE_FILE logs --tail=100'
        }
    }
}
