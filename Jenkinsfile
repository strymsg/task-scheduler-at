pipeline{
    agent{
        label "agent-eg"
    }
    stages{
        stage("Building"){
            steps{
                echo "========executing A========"
                sh 'sudo apt-get install python3.8'
                sh 'sudo apt-get install python3-pip'
                sh 'sudo apt-get install python3-virtualenv'
                sh 'virtualenv -p /usr/bin/python3 /home/ubuntu/jenkins_agent/workspace/first_pipeline_test/venv'
                sh 'source /home/ubuntu/jenkins_agent/workspace/first_pipeline_test/venv/bin/activate'
                sh 'pip3 install -r requirements.dev.txt'
                sh 'pip3 install wheel'
                sh 'sudo apt-get install tox'
                sh 'python3 setup.py sdist bdist_wheel'
            }
            post{
                success{
                    echo "==\"BUILDING\" executed successfully=="
                }
                failure{
                    echo "==\"BUILDING\" executed failed=="
                }
            }
        }
    }
    post{
        success{
            echo "========pipeline executed successfully ========"
            sh 'deactivate'
            sh 'sudo rm -rf /home/ubuntu/jenkins_agent/workspace/first_pipeline_test/venv'
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}
