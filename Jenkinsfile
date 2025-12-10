pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'jenkinsAsg3', url: 'https://github.com/thedatascientistguy-del/todo-list.git'
            }
        }

        stage('Build & Start App') {
            steps {
                sh 'docker-compose -f docker-compose-tests.yml build'
                sh 'docker-compose -f docker-compose-tests.yml up -d web mongodb'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh 'docker-compose -f docker-compose-tests.yml run --rm selenium_tests'
            }
        }

        stage('Teardown') {
            steps {
                sh 'docker-compose -f docker-compose-tests.yml down'
            }
        }
    }

    post {
        always {
            sh 'docker-compose -f docker-compose-tests.yml down'
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Some tests failed.'
        }
    }
}
