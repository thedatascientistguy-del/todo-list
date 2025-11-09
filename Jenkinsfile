pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = 'docker-hub-creds'
        IMAGE_NAME = "faq4265/todo-list"
        IMAGE_TAG = "latest"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/thedatascientistguy-del/todo-list.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Standard Docker build without BuildKit
                    sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_HUB_CREDENTIALS) {
                        sh "docker push $IMAGE_NAME:$IMAGE_TAG"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Docker image $IMAGE_NAME:$IMAGE_TAG pushed successfully!"
        }
        failure {
            echo "❌ Build or push failed!"
        }
    }
}
