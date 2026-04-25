pipeline {
    agent any
    
    environment {
        // Your Docker Hub username and the application name
        DOCKER_IMAGE = 'akilvignesh14/aceest-fitness'
        // Using the Jenkins BUILD_NUMBER as our image tag for easy versioning (e.g., v1.4, v1.5)
        DOCKER_TAG = "v1.${env.BUILD_NUMBER}" 
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies & Test') {
            steps {
                bat '''
                "C:\\Users\\al037\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv venv
                call venv\\Scripts\\activate.bat
                pip install -r requirements.txt
                pytest tests/
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Build the image and tag it with both the specific version and 'latest'
                bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest ."
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                // Securely load the credentials we just created in Jenkins
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    // Log in to Docker Hub via the terminal
                    bat '''
                    docker login -u "%DOCKER_USER%" -p "%DOCKER_PASS%"
                    '''
                    // Push both the specific version and the 'latest' tag
                    bat "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    bat "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }
    }
}