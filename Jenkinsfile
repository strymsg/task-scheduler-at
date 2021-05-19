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
                sh """
                
                sudo apt-get update
                sudo apt-get -y install python3.8
                sudo apt-get -y install python3-pip
                sudo apt-get -y install python3-virtualenv
                python3 -m venv \$WORKSPACE/venv
                source \$WORKSPACE/venv/bin/activate
                pip3 install -r requirements.dev.txt'
                pip3 install wheel'
                sudo apt-get -y install tox
                              
                PKG_OK=$(dpkg-query -W --showformat=\'${Status}\\n\' $PACKAGE_MONGO|grep "install ok installed")
                echo Checking for $PACKAGE_MONGO: $PKG_OK
                if [ "" = "$PKG_OK" ]; then
                  echo "No $PACKAGE_MONGO. Setting up $PACKAGE_MONGO."
                  sudo apt-get --yes install $PACKAGE_MONGO 
                fi
                      
                PKG_OK=\$(dpkg-query -W --showformat='\${Status}\n' \$REQUIRED_REDIS|grep "install ok installed")
                echo Checking for \$REQUIRED_REDIS: \$PKG_OK
                if [ "" = "\$PKG_OK" ]; then
                  echo "Not found: \$REQUIRED_REDIS... Setting up \$REQUIRED_REDIS."
                  sudo apt-get --y install \$REQUIRED_REDIS 
                fi

                """
            }
        }
        stage('UnitTests') {
            steps {
                sh "tox -vvv"
            }
        }
        
        /*
        
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
    */
    }
    
    post {
        always {
            echo "DONE!!!"
            // sh "docker-compose down || true"
            }
        }
}
