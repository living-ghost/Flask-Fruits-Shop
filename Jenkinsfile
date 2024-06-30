pipeline {
    agent any

    environment {
        VIRTUALENV = 'venv'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/living-ghost/Flask-Fruits-Shop.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
                    // Check if virtual environment exists, if not create one
                    if (!fileExists("${env.WORKSPACE}\\${env.VIRTUALENV}\\Scripts\\activate")) {
                        bat 'python -m venv venv'
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Run Flask App') {
            steps {
                bat 'venv\\Scripts\\activate && python run.py'
            }
        }
    }
}
