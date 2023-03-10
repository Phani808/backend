pipeline {
    agent any
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '3')
    }
    
    environment {
        APP_NAME = "backend"
        IMAGE_TAG = "${BUILD_NUMBER}"
        

    }
    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/Phani808/backend.git'
                ignore: commit([$class: 'org.jenkinsci.plugins.gitclient.IgnoreNotifyCommit', excludedUsers: 'phani'])
                         
            } 
            post {
                success {
                    slackSend (color: 'good', message: "Checkout SCM stage: Success: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
                failure {
                    slackSend (color: 'danger', message: "Checkout SCM stage: Failed: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
            }      
        }
        stage('increment version') {
            steps {
                script {
                    echo 'incrementing app version...'
                    sh 'mvn build-helper:parse-version versions:set \
                        -DnewVersion=\\\${parsedVersion.majorVersion}.\\\${parsedVersion.minorVersion}.\\\${parsedVersion.incrementalVersion} \
                        versions:commit'
                    def matcher = readFile('pom.xml') =~ '<version>(.+)</version>'
                    def version = matcher[0][1]
                    env.IMAGE_NAME = "$version-$BUILD_NUMBER"
                }
            }
            post {
                success {
                    slackSend (color: 'good', message: "Increment version stage: Success: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
                failure {
                    slackSend (color: 'danger', message: "Increment version stage: Failed: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
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
            post {
                success {
                    slackSend (color: 'good', message: "UNIT TEST stage: Success: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
                failure {
                    slackSend (color: 'danger', message: "UNIT TEST stage: Failed: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
            }
        }
        stage('INTEGRATION TEST'){
            steps {
                sh 'mvn verify'
            }
            post {
                success {
                    slackSend (color: 'good', message: "INTEGRATION TEST stage: Success: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
                failure {
                    slackSend (color: 'danger', message: "INTEGRATION TEST stage: Failed: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
            }
        }
        stage ('CODE ANALYSIS WITH CHECKSTYLE'){
            steps {
                sh 'mvn checkstyle:checkstyle'
            }
            
            post {
                success {
                    slackSend (color: 'good', message: "CODE ANALYSIS WITH CHECKSTYLE: Success: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
                failure {
                    slackSend (color: 'danger', message: "CODE ANALYSIS WITH CHECKSTYLE: Failed: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
            }
        }
        stage('Build docker image and push') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'nexus_passwd', variable: 'nexus_creds')]) {
                        sh "docker build -t 34.125.175.151:8083/backend:$IMAGE_NAME ."
                        sh "echo $nexus_creds | docker login -u admin --password-stdin 34.125.175.151:8083"
                        sh "docker push 34.125.175.151:8083/backend:$IMAGE_NAME"
                        sh "docker rmi 34.125.175.151:8083/backend:$IMAGE_NAME"
                    }
                }
            }
            post {
                success {
                    slackSend (color: 'good', message: "Build docker image and push: Success: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
                failure {
                    slackSend (color: 'danger', message: "Build docker image and push: Failed: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
                }
            }
        }
      //  stage('Commit Version Update') {
         //   steps {
         //       script {
         //           withCredentials([gitUsernamePassword(credentialsId: 'git', gitToolName: 'Default')]) {
         //               sh 'git config --global user.email "mpvarma997@gmail.com"'
          //              sh 'git config --global user.name "phani"'
          //              sh "git remote set-url origin https://github.com/Phani808/backend.git"
           //             sh 'git add .'
           //             sh 'git commit -m "Ci: Version Bump"'
           //             sh 'git push origin HEAD:main'
              //      }
         //     //  }
         //   }
          //  post {
          //      success {
          //          slackSend (color: 'good', message: "commit version update: Success: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
          //      }
          //      failure {
          //          slackSend (color: 'danger', message: "commit version update: Failed: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
             //   }
         //   }
     //   }
        stage('Trigger Update K8s') {
            steps{
            script {
                echo "triggering Update manifest Job"
                sh "curl -v -k -user Phani: 1128130815aa05948951b1606d49480525 -X POST -H 'cache-control: no-cache' -H 'content-type: application/x-www-form-urlencoded' -d \"IMAGE_NAME=${IMAGE_NAME}\" 'http://34.125.172.13:8080/job/Project/job/backend-update-k8s/buildWithParameters?token=phani'"

              
            }
            }
        }
    }
}

