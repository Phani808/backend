pipeline {
    agent any
    
    options {
         buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '3')
         }
         stages {
            stage('Checkout SCM') {
                steps {
                git branch: 'main', url: 'https://github.com/Phani808/backend.git'
        }       
      }
       stage('Sonar Quality status'){
    steps{
   
        withSonarQubeEnv('sonarqube') {
    sh 'mvn clean package sonar:sonar'
      
      }
    } 
}
      stage('SonarQube Quality Gate') {
    steps {
        script {
            waitForQualityGate abortPipeline: false, credentialsId: 'sonar'
    }   
 } 
}
    stage('BUILD'){
            steps {
                sh 'mvn clean install'
            }
            post {
                success {
                    echo 'Now Archiving...'
                    archiveArtifacts artifacts: '**/target/*.war'
                }
            }
        }

	stage('UNIT TEST'){
            steps {
                sh 'mvn test'
            }
        }

	stage('INTEGRATION TEST'){
            steps {
                sh 'mvn verify'
            }
        }
		
        stage ('CODE ANALYSIS WITH CHECKSTYLE'){
            steps {
                sh 'mvn checkstyle:checkstyle'
            }
            post {
                success {
                    echo 'Generated Analysis Result'
                }
            }
        }
        stage("Publish to Nexus Repository Manager") {
            steps {
                script {
                 nexusArtifactUploader artifacts: [[artifactId: 'devopsodia', classifier: '', file: 'target/devopsodia.war', type: 'war']], credentialsId: 'nexus', groupId: 'com.devopsodia', nexusUrl: '34.16.136.33:8081', nexusVersion: 'nexus3', protocol: 'http', repository: 'backend-release', version: '0.0.1'
}
 }
 
 }
}
}
