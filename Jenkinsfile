pipeline {
    agent any

    environment {
        DOCKERHUB_IMAGE = "faq4265/todo-list:latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'jenkinsAsg2',
                    url: 'https://github.com/thedatascientistguy-del/todo-list.git'
            }
        }

        stage('Pull Docker Images') {
            steps {
                sh 'docker pull ${DOCKERHUB_IMAGE}'
                sh 'docker pull mongo:latest'
            }
        }

        stage('Build & Run using Docker Compose') {
            steps {
                sh '''
                echo "Stopping old containers..."
                docker compose down || true

                echo "Starting new containers..."
                docker compose up -d --force-recreate
                '''
            }
        }

        stage('Verify Running Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {
        always {
            echo "Build complete. Cleaning unused data..."
            sh 'docker system prune -f'
        }
    }
}
