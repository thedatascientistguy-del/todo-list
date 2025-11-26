pipeline {
  agent any

  environment {
    COMPOSE = "docker-compose -f docker-compose-jenkins.yml"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        sh 'pwd; ls -la'
      }
    }

    stage('Pre-checks') {
      steps {
        sh '''
          echo "Docker version:"
          docker --version || true
          echo "Docker compose version:"
          docker compose version || docker-compose --version || true
        '''
      }
    }

    stage('Build images') {
      steps {
        sh "${COMPOSE} build --pull --parallel"
      }
    }

    stage('Start containers') {
      steps {
        sh "${COMPOSE} up -d"
      }
    }

    stage('Smoke test') {
      steps {
        sh '''
          echo "Waiting for services..."
          sleep 5
          echo "Containers:"
          docker ps --filter "name=jenkins_fastapi" --filter "name=jenkins_mongo"
          # Try basic HTTP GET (adjust path if your app healthcheck endpoint differs)
          if curl --fail --retry 5 --retry-delay 2 http://localhost:9000/ ; then
            echo "Smoke test succeeded"
          else
            echo "Smoke test failed - printing logs"
            ${COMPOSE} ps
            ${COMPOSE} logs --tail=200
            exit 1
          fi
        '''
      }
    }
  }

  post {
    failure {
      sh '''
        echo "Pipeline failed - docker ps and last logs:"
        docker ps -a --filter "name=jenkins_fastapi" --filter "name=jenkins_mongo"
        docker stats --no-stream || true
        ${COMPOSE} logs --tail=400 || true
      '''
    }
    always {
      echo "Pipeline finished."
    }
  }
}

