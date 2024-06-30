pipeline {
    agent any
    
    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials-id'
        DOCKER_IMAGE = 'living9host/fruits-app'
        CONTAINER_NAME = 'fruits-container'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/living-ghost/Flask-Fruits-Shop.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS_ID) {
                        try {
                            dockerImage.push()
                            echo 'Image pushed successfully'
                        } catch (Exception e) {
                            echo "Failed to push image: ${e.getMessage()}"
                        }
                    }
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    // Define the container name and image variables
                    def containerName = "${env.CONTAINER_NAME}"
                    def imageName = "${DOCKER_IMAGE}:${env.BUILD_ID}"

                    bat """
                    // Stop and remove any existing container with the same name
                    docker stop ${containerName} || true
                    docker rm ${containerName} || true

                    // Run the new container
                    docker run -d --name ${containerName} -p 80:80 ${imageName}
                    """
                }
            }
        }
    }
}