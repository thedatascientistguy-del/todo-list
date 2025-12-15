pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKERHUB_IMAGE = "faq4265/todo-list:latest"
    }

    stages {

        stage('Checkout Latest Code') {
            steps {
                echo "📥 Pulling latest code from GitHub..."
                git branch: 'jenkinsAsg2',
                    url: 'https://github.com/thedatascientistguy-del/todo-list.git'
            }
        }

        stage('Stop Existing Environment') {
            steps {
                echo "🛑 Bringing environment DOWN..."
                sh '''
                    docker compose down || true
                '''
            }
        }

        stage('Pull Latest Images') {
            steps {
                echo "⬇️ Pulling latest Docker images..."
                sh '''
                    docker compose pull
                '''
            }
        }

        stage('Start Environment') {
            steps {
                echo "🚀 Bringing environment UP..."
                sh '''
                    docker compose up -d --force-recreate
                '''
            }
        }

        stage('Verify Containers') {
            steps {
                echo "🔍 Verifying running containers..."
                sh 'docker ps'
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful — environment is LIVE"
        }
        failure {
            echo "❌ Deployment failed — check logs"
        }
    }
}
