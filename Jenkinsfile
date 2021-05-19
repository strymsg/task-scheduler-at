pipeline {
    agent {label 'agent-eg'}
    stages {
        stage("Prepare") {
            steps {
                bitbucketStatusNotify buildState: "INPROGRESS"
            }
        }
        stage('Building') {
            steps {
                // sh 'docker build -t test_test_test .'
                sh """
                docker-compose build
                docker-compose up -d
                """
            }
        }
        stage('Example Test') {
            steps {
                echo 'Hello, Here will be tests and they will run with tox'
            }
        }
    }
      post {
      always {
          sh "docker-compose down || true"
      }
      success {
          bitbucketStatusNotify buildState: "SUCCESSFUL"
      }
      failure {
          bitbucketStatusNotify buildState: "FAILED"
      }
}
