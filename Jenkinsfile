pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose-jenkins.yml'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'jenkins',
                    url: 'https://github.com/thedatascientistguy-del/https://github.com/thedatascientistguy-del/todo-list.git'
            }
        }

        stage('Build and Run Docker Containers') {
            steps {
                sh 'docker-compose -f $DOCKER_COMPOSE_FILE down'  // stop old containers
                sh 'docker-compose -f $DOCKER_COMPOSE_FILE up -d --build'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
    }
}
