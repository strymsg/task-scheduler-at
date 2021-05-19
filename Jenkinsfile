pipeline {
    
    agent {label 'agent-eg'}
    
    environment {
        BUILD_NUMBER = "0.9"
        PROJECT_PREFIX = "TASK-SCHED"
        PROJECT_IMAGE = "${env.PROJECT_PREFIX}:${env.BUILD_NUMBER}"
        PROJECT_CONTAINER = "${env.PROJECT_PREFIX}-${env.BUILD_NUMBER}"
        PACKAGE_MONGO = "mongodb"
        PACKAGE_REDIS = "redis-server"
    }
    
    stages {
        stage("Prepare Environment") {
            steps {
                sh """sudo apt-get update
                    sudo apt-get -y install python3.8
                    sudo apt-get -y install python3-pip
                    sudo apt-get -y install python3-virtualenv
                    python3 -m venv \$WORKSPACE/venv
                    source \$WORKSPACE/venv/bin/activate
                    pip3 install -r requirements.dev.txt
                    pip3 install tox
                    pip3 install wheel
                    sudo apt-get -y install tox
                        
                    PKG_OK=\$(dpkg-query -W --showformat='\${Status}\\n' \${PACKAGE_MONGO}|grep "install ok installed")
                    echo Checking for \${PACKAGE_MONGO}: \${PKG_OK}
                    if [ "" = "\${PKG_OK}" ]; then
                        echo "Not found: \${PACKAGE_MONGO}... Setting up \${PACKAGE_MONGO}."
                        sudo apt-get --y install \${PACKAGE_MONGO} 
                    fi 

                    PKG_OK=\$(dpkg-query -W --showformat='\${Status}\\n' \${PACKAGE_REDIS}|grep "install ok installed")
                    echo Checking for \${PACKAGE_REDIS}: \${PKG_OK}
                    if [ "" = "\${PKG_OK}" ]; then
                        echo "Not found: \${PACKAGE_REDIS}... Setting up \${PACKAGE_REDIS}."
                        sudo apt-get --y install \${PACKAGE_REDIS} 
                    fi  """
            }
        }
        stage('UnitTests') {
            steps {
                sh """source \$WORKSPACE/venv/bin/activate
                      tox -vvv """
            }
        }
        
        stage('Static code analysis') {
            steps{
                echo "Here will be Sonar..."
            }
        }
        
        stage("Building with Docker") {
            steps {
                // sh 'docker build -t test_test_test .'
                sh """
                docker-compose build """
                // sh "docker-compose up -d"
            }
        }
        stage('Promote Image') {
            steps {
                echo 'Here will be NEXUS...'
            }
        }
    
    }
    
    post {
        always {
            echo "DONE!!!"
            // sh "docker-compose down || true"
            }
        }
}
