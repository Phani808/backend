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
            def qg = waitForQualityGate()
            if (qg.status != 'OK') {
                error "Pipeline aborted due to Quality Gate failure: ${qg.status}"
    }   
 } 
}
}   