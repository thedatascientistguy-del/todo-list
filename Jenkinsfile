pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose-jenkins.yml'
    }

    stages {
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
                sh 'docker compose -f $DOCKER_COMPOSE_FILE down -v'  // stop and remove old containers
                sh 'docker compose -f $DOCKER_COMPOSE_FILE up -d --build'
            }
        }

        stage('Test') {
            steps {
                sh '''
                docker run --rm \
                -v $PWD:/tests \
                -w /tests \
                selenium/standalone-chrome:115.0 \
                bash -c "pip install -r requirements.txt && pytest"
                '''
            }
        }


        stage('Smoke Test') {
            steps {
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
            sh 'docker ps -a'
            sh 'docker compose -f $DOCKER_COMPOSE_FILE logs --tail=100'
        }
    }
}
