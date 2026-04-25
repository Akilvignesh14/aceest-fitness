pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                // We use double backslashes so Jenkins reads the path correctly
                bat '''
                "C:\\Users\\al037\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv venv
                call venv\\Scripts\\activate.bat
                pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate.bat
                pytest tests/
                '''
            }
        }
    }
}