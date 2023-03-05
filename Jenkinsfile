pipeline {
    agent any
    options {
         buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '3')
         }
         stages {
            stage('Checkout SCM') {
                git branch: 'main', url: 'https://github.com/Phani808/backend.git'
      }
    }   
 }    