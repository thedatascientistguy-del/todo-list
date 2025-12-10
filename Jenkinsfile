pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:$PATH" // ensures docker compose is found
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'jenkinsAsg3', url: 'https://github.com/thedatascientistguy-del/todo-list.git'
            }
        }

        stage('Build & Start App') {
            steps {
                // Use a separate CI docker-compose to avoid port conflicts
                sh 'docker compose -f docker-compose-ci.yml build'
                sh 'docker compose -f docker-compose-ci.yml up -d web mongodb'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                // Runs the selenium_tests service defined in docker-compose-ci.yml
                sh 'docker compose -f docker-compose-ci.yml run --rm selenium_tests'
            }
        }

        stage('Teardown') {
            steps {
                // Tear down CI containers, networks, and volumes
                sh 'docker compose -f docker-compose-ci.yml down'
            }
        }
    }

    post {
        always {
            sh 'docker compose -f docker-compose-ci.yml down'
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Some tests failed.'
        }
    }
}
