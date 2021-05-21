pipeline {

    agent {label 'agent-eg'}
    //agent {label 'jenkins-agent-01'}

    environment {
        IMAGE_NAME = "app-task-scheduler:${BUILD_NUMBER}"
        PROM_IMAGE_NAME = "app-task-scheduler"
        PROJECT_PREFIX = "APP-TASK-SCHEDULER"
        PROJECT_CONTAINER = "${env.PROJECT_PREFIX}-${BUILD_NUMBER}"
        PACKAGE_MONGO = "mongodb"
        PACKAGE_REDIS = "redis-server"
        NEXUS_IP_PORT = "10.28.108.154:8083"
    }

    stages {
        stage("Prepare Environment") {
            steps {
                sh """
                    sudo apt-get update &&  sudo apt-get -y install python3.7 && sudo apt-get -y install python3-pip \
                        && sudo apt-get -y install python3-venv && sudo apt-get -y install \${PACKAGE_MONGO} \
                        && sudo apt-get -y install \${PACKAGE_REDIS} && sudo apt-get -y install tox

                    sudo service mongodb start && sudo service redis-server start
                    
                    python3 -m venv \$WORKSPACE/venv
                    source \$WORKSPACE/venv/bin/activate
                    pip3 install -r requirements.dev.txt
                    pip3 install tox
                    pip3 install wheel"""
            }
        }
        
        stage('UnitTests') {
            steps {
                sh """source \$WORKSPACE/venv/bin/activate
                      tox -vvv """
            }
        }

         stage('Static code analysis') {
            steps {
                script {
                    // SonarQube Scanner Installation name = sonarqube-scanner-at
                    // Get the directory path where SonarQube Scanner
                    def scannerHome = tool 'sonarqube-scanner-at'
                    // SonarQube Server name = sonarqube-automation
                    withSonarQubeEnv('sonarqube-automation') {
                    // Set parameters to the sonar-scanner binary and run it
                        sh """${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectName=$PROJECT_PREFIX \
                        -Dsonar.projectKey=$PROJECT_PREFIX \
                        -Dsonar.sources=."""
                    }
                }
             }
        }

        stage("Building with Docker") {
            steps {
                sh """
                docker-compose build """
                // sh "docker-compose up -d"
            }
            post {
                failure {
                    script {
                        sh "docker rmi \$(docker images --filter dangling=true -q)"
                    }
                }
            }
        }
        
        stage('Promote Image') {
            steps{
                script {
                        withCredentials([usernamePassword(
                          credentialsId: 'sonatype-nexus-at-rodrigo',
                          usernameVariable: 'USERNAME',
                          passwordVariable: 'PASSWORD'
                        )]) {

                          sh """
                            docker login -u $USERNAME -p $PASSWORD \${NEXUS_IP_PORT}
                            docker push \${NEXUS_IP_PORT}/\${PROM_IMAGE_NAME}:\${BUILD_NUMBER}
                          """
                        }
                    }
                }
    
            post {
                always {
                    script {
                        sh "docker rmi -f \${NEXUS_IP_PORT}/\${PROM_IMAGE_NAME}:\${BUILD_NUMBER}"
                        sh "docker logout \${NEXUS_IP_PORT}"
                    }
                }
            }
        }
    }

    post {
        always {
            emailext body: """Hi Devs!\n\nJenkins reporting: Pipeline execution finished\n\nStatus: \"${currentBuild.currentResult}\"\nJob: ${env.JOB_NAME}\nBuild: ${env.BUILD_NUMBER}\nURL to more info at: ${env.BUILD_URL}""",
            recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], 
            subject: "${currentBuild.currentResult}: Jenkins Build (${env.BUILD_NUMBER}) Notification for Job: ${env.JOB_NAME}",
            to: '$DEFAULT_RECIPIENTS'
        }
    }
}
