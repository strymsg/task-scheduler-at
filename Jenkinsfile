pipeline {

    agent {label 'agent-eg'}
    //agent {label 'jenkins-agent-01'}

    environment {
        STAGING_TAG = "${BUILD_NUMBER}-stg"
        PROD_TAG = "${BUILD_NUMBER}-prod"
        PROJECT_NAME = "app-task-scheduler"
        PACKAGE_MONGO = "mongodb"
        PACKAGE_REDIS = "redis-server"
        NEXUS_IP_PORT = "10.28.108.180:8123"
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
                    def scannerHome = tool 'sonarqube-scanner-at'
                    withSonarQubeEnv('sonarqube-automation') {
                        sh """${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectName=$PROJECT_NAME \
                        -Dsonar.python.coverage.reportPaths=coverage.xml \
                        -Dsonar.projectKey=$PROJECT_NAME \
                        -Dsonar.sources=."""
                    }
                }
             }
        }

        stage ("Quality Gate") {
            steps {
                timeout(time: 1, unit:"HOURS"){
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage("Building Staging Image") {
            when {branch "develop"}
            environment {
                TAG = "$STAGING_TAG"
            }
            steps {
                sh """
                docker-compose build """
            }
            post {
                failure {
                    script {
                        sh "docker rmi \$(docker images --filter dangling=true -q)"
                    }
                }
            }
        }

        stage('Promote Staging Image') {
            when {branch "develop"}
            environment {
                TAG = "$STAGING_TAG"
            }
            steps{
                script {
                        withCredentials([usernamePassword(
                          credentialsId: 'nexus_eg_credentials',
                          usernameVariable: 'USERNAME',
                          passwordVariable: 'PASSWORD'
                        )]) {

                          sh """
                            docker login -u $USERNAME -p $PASSWORD \${NEXUS_IP_PORT}
                            docker push \${NEXUS_IP_PORT}/\${PROJECT_NAME}:\${TAG}
                          """
                        }
                    }
                }

            post {
                always {
                    script {
                        sh "docker logout \${NEXUS_IP_PORT}"
                    }
                }
            }
        }

        stage ('Deploy to Staging') {
            when {branch 'develop'}
            environment {
                TAG = "$STAGING_TAG"
            }
            steps {
               script {
                        sh "docker rm -f \$(docker ps --filter name=$PROJECT_NAME* -q)"
                        sh "docker-compose up -d"
                    }
                }

            post {
                success {
                    script {
                        sh "docker image prune -a -f"
                    }
                }
            }
        }

        stage ('Acceptance Tests') {
           when {branch 'develop'}
           steps {
               sh """
               curl -I http://10.28.108.180:5000/api/v1/task/api-task/all | grep 200
               curl -I http://10.28.108.180:5000/api/v1/task/api-task/task_Db | grep 200
               """
           }
        }

        stage ('Building Prod Image') {
           when {branch 'main'}
           environment {
                TAG = "$PROD_TAG"
            }
           steps {
               sh "docker-compose build"
           }
           post {
               failure {
                   script {
                       sh "docker rmi \$(docker images --filter dangling=true -q)"
                   }
               }
           }
        }

        stage('Promote Prod Image') {
            when {branch "main"}
            environment {
                TAG = "$PROD_TAG"
            }
            steps{
                script {
                        withCredentials([usernamePassword(
                          credentialsId: 'nexus_eg_credentials',
                          usernameVariable: 'USERNAME',
                          passwordVariable: 'PASSWORD'
                        )]) {

                          sh """
                            docker login -u $USERNAME -p $PASSWORD \${NEXUS_IP_PORT}
                            docker push \${NEXUS_IP_PORT}/\${PROJECT_NAME}:\${TAG}
                          """
                        }
                    }
                }

            post {
                always {
                    script {
                        sh "docker logout \${NEXUS_IP_PORT}"
                    }
                }
            }
        }

        stage ('Deploy to Prod') {
            when {branch 'main'}
            environment {
                TAG = "$PROD_TAG"
            }
            steps {
               script {
                    sh "docker rm -f \$(docker ps --filter name=$PROJECT_NAME* -q)"
                    sh "docker-compose up -d"
               }
            }
            post {
                success {
                    script {
                        sh "docker image prune -a -f"
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
