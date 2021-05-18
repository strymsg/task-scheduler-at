pipeline{
    agent{
        label "agent-eg"
    }
    stages{
        stage("Building"){
            steps{
                echo "========executing A========"
                // sh 'virtualenv -p /usr/bin/python3 ../venv'
                // sh 'source /home/ubuntu/jenkins_agent/workspace/'
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
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}
