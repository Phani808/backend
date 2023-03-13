pipeline {
    agent any
     environment {
        NEXUS_VERSION = "nexus3"
        NEXUS_PROTOCOL = "http"
        NEXUS_URL = "34.125.12.138:8081"
        NEXUS_REPOSITORY = "backend-release"
	NEXUS_REPO_ID    = "backend-release"
        NEXUS_CREDENTIAL_ID = "nexus"
    //    ARTVERSION = "${env.BUILD_ID}"
  //      VERSION = "${env.BUILD_ID}"
    }
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
                echo 'incrementing app version ..'
                sh 'mvn build-helper:parse-version versions:set \
                -DnewVersion=\\\${parsedVersion.majorVersion}.\\\$(parsedVersion.minorVersion).\\\$(parsedVersion.nextIncrementalVersion) versions:commit'
               def matcher = readFile('pom.xml') =~ '<version>(.+)</version>'
              def version = matcher[0][1]
             env.IMAGE_NAME = "$version-$BUILD_NUMBER"
            }
        }
      }
    //    stage('Sonar Quality status')
   // steps{
   
     //   withSonarQubeEnv('sonarqube') {
   // sh 'mvn clean package sonar:sonar'
      
    //  }
  //  } 
//}
     // stage('SonarQube Quality Gate') {
  //  steps {
    //    script {
      //      waitForQualityGate abortPipeline: false, credentialsId: 'sonar'
  //  }   
 //} 
//}
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
        //            pom = readMavenPom file: "pom.xml";
            //        filesByGlob = findFiles(glob: "target/*.${pom.packaging}");
            //        echo "${filesByGlob[0].name} ${filesByGlob[0].path} ${filesByGlob[0].directory} ${filesByGlob[0].length} ${filesByGlob[0].lastModified}"
             //       artifactPath = filesByGlob[0].path;
            //        artifactExists = fileExists artifactPath;
                //    if(artifactExists) {
                //        echo "*** File: ${artifactPath}, group: ${pom.groupId}, packaging: ${pom.packaging}, version ${pom.version} ARTVERSION";
                       nexusArtifactUploader(
                            nexusVersion: NEXUS_VERSION,
                           protocol: NEXUS_PROTOCOL,
                            nexusUrl: NEXUS_URL,
                            groupId: pom.groupId,
                            version: ARTVERSION,
                            repository: NEXUS_REPOSITORY,
                            credentialsId: NEXUS_CREDENTIAL_ID,
                           artifacts: [
                               [artifactId: pom.artifactId,
                              classifier: '',
                               file: artifactPath,
                                type: pom.packaging],
                                [artifactId: pom.artifactId,
                                classifier: '',
                                file: "pom.xml",
                                type: "pom"]
                            ]
                        );
                    } 
		
               }
       //     }
      //  }
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
     //   stage('Trigger Update K8s') {
      //      steps{
      //      script {
       //         echo "triggering Update manifest Job"
      //          build job: 'backend-update-k8s', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
         //   }
       // }
   // }             

       }
         }  
}     
