pipeline {
    agent any
  ///  environment {
    //    NEXUS_VERSION = "nexus3"
     //   NEXUS_PROTOCOL = "http"
     //   NEXUS_URL = "34.125.12.138:8081"
     //   NEXUS_REPOSITORY = "backend-release"
     //   NEXUS_REPO_ID    = "backend-release"
     //   NEXUS_CREDENTIAL_ID = "nexus"
  //  }
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '3')
    }
    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/Phani808/backend.git'
            }       
        }
      
        stage('increment version') {
            steps {
                script {
                    echo 'incrementing app version...'
                    sh 'mvn build-helper:parse-version versions:set \
                        -DnewVersion=\\\${parsedVersion.majorVersion}.\\\${parsedVersion.minorVersion}.\\\${parsedVersion.nextIncrementalVersion} \
                        versions:commit'
                    def matcher = readFile('pom.xml') =~ '<version>(.+)</version>'
                    def version = matcher[0][1]
                    env.IMAGE_NAME = "$version-$BUILD_NUMBER"
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
        }
          //  post {
            //    success {
                  //  echo 'Generated Analysis Result'
            //    }
          // }
        
       
      //  stage("Publish to Nexus Repository Manager") {
         //   steps {
          //      nexusArtifactUploader(
           //         nexusVersion: NEXUS_VERSION,
           //         protocol: NEXUS_PROTOCOL,
          //          nexusUrl: NEXUS_URL,
           ////         groupId: pom.groupId,
            //        repository: NEXUS_REPOSITORY,
            //        credentialsId: NEXUS_CREDENTIAL_ID,
            //        artifacts: [
            //            [artifactId: pom.artifactId,
             //            classifier: '',
             //            file: artifactPath,
              //           type: pom.packaging],
              //          [artifactId: pom.artifactId,
              //           classifier: '',
             //            file: "pom.xml",
             //            type: "pom"]
            //        ]
            //    )
          //  }
     ///   }
               
        stage('Build docker image and push') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'nexus_passwd', variable: 'nexus_creds')]) {
                        sh "docker build -t 34.125.12.138:8083/backend:$IMAGE_NAME ."
                        sh "echo $nexus_creds | docker login -u admin --password-stdin 34.125.12.138:8083"
                        sh "docker push 34.125.12.138:8083/backend:$IMAGE_NAME"
                        sh "docker rmi 34.125.12.138:8083/backend:$IMAGE_NAME"
                    }
                }
            }
        }
        stage('commit version update') {
            steps {
                script {
                    withCredentials([gitUsernamePassword(credentialsId: 'git', gitToolName: 'Default')]) {
                        sh 'git config --global user.email "mpvarma997@gmail.com"'
                        sh 'git config --global user.name "phani"'

                        sh "git remote set-url origin https://github.com/Phani808/backend.git"
                        sh 'git add .'
                        sh 'git commit -m "ci: version bump"'
                        sh 'git push origin HEAD:main'
                    }
                }
            }
        }

    }
} 
         
          
   
