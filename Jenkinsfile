
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
            // Ensure containers are down even if build fails
            sh 'docker compose -f docker-compose-ci.yml down'
        }

        success {
            echo 'All tests passed!'
            emailext(
                to: 'qasimalik@gmail.com',
                subject: "SUCCESS: Build ${currentBuild.fullDisplayName}",
                body: """\
Hello,

The Jenkins build has completed successfully.

Build URL: ${env.BUILD_URL}

All Selenium tests passed!

Regards,
Jenkins CI
"""
            )
        }

        failure {
            echo 'Some tests failed.'
            emailext(
                to: 'qasimalik@gmail.com',
                subject: "FAILURE: Build ${currentBuild.fullDisplayName}",
                body: """\
Hello,

The Jenkins build has failed.

Build URL: ${env.BUILD_URL}

Please check the console output for details.

Regards,
Jenkins CI
""",
                attachLog: true
            )
        }
    }
}
