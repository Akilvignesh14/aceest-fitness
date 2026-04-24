pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // This step automatically pulls the latest code from GitHub
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                // Setting up a virtual environment and installing packages
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate.bat
                pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                // Running the Pytest framework to validate application logic
                bat '''
                call venv\\Scripts\\activate.bat
                pytest tests/
                '''
            }
        }
    }
}