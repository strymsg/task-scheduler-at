pipeline {
    agent none
    stages {
        stage('App'){
            agent {
                dockerfile {
                    filename 'Dockerfile'
                }
            }
            steps {
                echo "APP - created"
            }
        }
        stage('Redis') {
            agent {
                docker {
                    image 'redis:latest'
                    args """
                    --name redisdbat
                    -v /docker/redisdb/datadir:/data
                    """
                }
            }
            steps {
                echo "REDIS - created"
            }
        }
        stage('Mongo') {
            agent {
                docker {
                    image 'mongo:latest'
                    args """
                    --name mongodbat
                    -e MONGO_INITDB_ROOT_USERNAME= \
                    -e MONGO_INITDB_ROOT_PASSWORD= \
                    -v /docker/mongodb/datadir:/data/db
                    """
                }
            }
            steps {
                echo "MONGO - created"
            }
        }
    }
}
