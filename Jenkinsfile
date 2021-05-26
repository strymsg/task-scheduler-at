pipeline {

    //agent {label 'agent-eg'}
    agent {label 'jenkins-agent-01'}

    environment {
        STAGING_TAG = "${BUILD_NUMBER}-stg"
        PROD_TAG = "${BUILD_NUMBER}-prod"
        PROJECT_NAME = "app-task-scheduler"
        PACKAGE_MONGO = "mongodb"
        PACKAGE_REDIS = "redis-server"
        //NEXUS_IP_PORT = "10.28.108.180:8123"
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
                    pip3 install coverage
                    pip3 install wheel"""
            }
        }

        stage('UnitTests') {
            steps {
                sh """source \$WORKSPACE/venv/bin/activate
                      tox -vvv 
                      coverage xml
                      """
            }
        }

        //  stage('Static code analysis') {
        //     steps {
        //         script {
        //             def scannerHome = tool 'sonarqube-scanner-at'
        //             withSonarQubeEnv('sonarqube-automation') {
        //                 sh """${scannerHome}/bin/sonar-scanner \
        //                 -Dsonar.projectName=$PROJECT_NAME \
        //                 -Dsonar.projectKey=$PROJECT_NAME \
        //                 -Dsonar.sources=."""
        //             }
        //         }
        //      }
        // }

        stage("Building with Docker") {
            when {branch "devops/Rodrigo-Garcia"}
            environment {
                TAG = "$STAGING_TAG"
            }
            steps {
                sh """
                docker-compose build 
                echo
                docker images --filter dangling=true -q
                """
            }
            post {
                failure {
                    script {
                        sh 'Falied docker-compose build'
                        //sh "sudo docker rmi \$(docker images --filter dangling=true -q)"
                    }
                }
            }
        }

        // stage('Promote Image') {
        //     when {branch "devops/Rodrigo-Garcia"}
        //     environment {
        //         TAG = "$STAGING_TAG"
        //     }
        //     steps{
        //         script {
        //                 withCredentials([usernamePassword(
        //                   credentialsId: 'nexus_eg_credentials',
        //                   usernameVariable: 'USERNAME',
        //                   passwordVariable: 'PASSWORD'
        //                 )]) {

        //                   sh """
        //                     docker login -u $USERNAME -p $PASSWORD \${NEXUS_IP_PORT}
        //                     docker push \${NEXUS_IP_PORT}/\${PROJECT_NAME}:\${TAG}
        //                   """
        //                 }
        //         }
        //     }

        //     post {
        //         always {
        //             script {
        //                 sh "docker rmi -f \${NEXUS_IP_PORT}/\${PROJECT_NAME}:\${TAG}"
        //                 sh "docker logout \${NEXUS_IP_PORT}"
        //             }
        //         }
        //     }
        // }

        stage ('Deploy to Staging') {
            when {branch 'devops/Rodrigo-Garcia'}
            environment {
                TAG = "$STAGING_TAG"
            }
            steps {
               script {
                        withCredentials([usernamePassword(
                          //credentialsId: 'nexus_eg_credentials',
                          credentialsId: 'sonatype-nexus-at-rodrigo',
                          usernameVariable: 'USERNAME',
                          passwordVariable: 'PASSWORD'
                        )]) {
                           // sh "sudo docker pull \${NEXUS_IP_PORT}/\${PROJECT_NAME}:\${TAG}"
                          sh """
                            docker login -u $USERNAME -p $PASSWORD \${NEXUS_IP_PORT}
                            docker-compose up -d
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

        stage ('Acceptance Tests') {
           when {branch 'devops/Rodrigo-Garcia'}
           steps {
               sh "echo OK"
            //    sh "curl http://localhost:8003/hello/ | grep 'Hello World!'"
            //    sh "curl http://localhost:8003/hello/User | grep 'Hello User!'"
            //    sh "curl http://localhost:8004/hello/ | grep 'Hello World!'"
            //    sh "curl http://localhost:8004/hello/User | grep 'Hello User!'"
           }
        }

        stage ('Tag Prod Image') {
           when {branch 'devops/Rodrigo-Garica'}
           environment {
                TAG = "$SPROD_TAG"
            }
           steps {
               sh "docker-compose build"
           }
           post {
               failure {
                   script {
                       sh "echo 'paso fallido'"
                       // sh "sudo docker rmi \$(docker images --filter dangling=true -q)"
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