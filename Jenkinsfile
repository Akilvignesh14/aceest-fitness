pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'akilvignesh14/aceest-fitness'
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

        // --- NEW STAGE FOR TASK 7 ---
        stage('SonarQube Analysis') {
            steps {
                // This 'sonar-server' name must match what you saved in Jenkins System settings
                withSonarQubeEnv('sonar-server') {
                    // This command runs the static code analysis [cite: 65]
                    bat 'sonar-scanner -Dsonar.projectKey=aceest-fitness -Dsonar.sources=.'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest ."
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    bat '''
                    docker login -u "%DOCKER_USER%" -p "%DOCKER_PASS%"
                    '''
                    bat "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    bat "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }
    }
}