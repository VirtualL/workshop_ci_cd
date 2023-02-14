pipeline {
//None parameter in the agent section means that no global agent will be allocated for the entire Pipeline’s
//execution and that each stage directive must specify its own agent section.
    agent any
    environment {
        AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
        DOCKER                = credentials('jenkins-dockerhub')
        GITHUB                = credentials('myGitHubToken')
    }
    stages {
        stage('Init') {
            steps {
                //cleanWs()
                echo "Init stage"
                echo "Running BUILD_ID: ${env.BUILD_ID} on ${env.JENKINS_URL}"
            } 
    }
        stage('Get SCM') {
            steps {
                git branch: 'development', url: 'https://github.com/VirtualL/workshop_ci_cd.git'
            }
        }
        
        stage('Build') {
            steps {
                dir('application') {
                    sh "pwd && ls -la" 
                    sh "docker rm -f boto3_ip_finder"                
                    sh "docker build -t boto3_ip_finder ."
                }
                sh """
                docker login -u ${DOCKER_USR} -p ${DOCKER_PSW}
                docker image tag boto3_ip_finder virtuall4u/workshop_ci_cd:${env.BUILD_ID}
                docker push virtuall4u/workshop_ci_cd:${env.BUILD_ID}
                """
            }
        }

        stage('Test') {
            steps {
                sh "docker run -itd --name boto3_ip_finder --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}  --env AWS_DEFAULT_REGION=eu-west-1 boto3_ip_finder"
                sleep 5
                sh "docker logs boto3_ip_finder"                
            }
        }      
    }
    post {
        success {
            echo "This pipeline BUILD_ID: ${env.BUILD_ID} on ${env.JENKINS_URL} finshed successfully!"
            
            sh """
            echo "Uploading new docker image:" 
            docker login -u ${DOCKER_USR} -p ${DOCKER_PSW}
            docker image tag boto3_ip_finder virtuall4u/workshop_ci_cd:latest
            docker push virtuall4u/workshop_ci_cd:latest
            """
            dir('helm-Chart') {
                sh "pwd && ls -la"                  
                sh """#!/bin/bash
                echo "Updating helm-chart image tag:" 
                # Use sed to find the line with the key name "tag" and update its value to "BUILD_ID" in file "values.yaml"
                sed -i 's|tag: .*|tag: "${env.BUILD_ID}"|' values.yaml
                git diff values.yaml
                """              
                sh """
                git add values.yaml 
                git commit -m "Updating image tag to:${env.BUILD_ID} in helm-chart values file"
                git push https://${GITHUB_USR}:${GITHUB_PSW}@github.com/VirtualL/workshop_ci_cd.git
                """
            }                
            echo "Marging 'development' branch to 'master'"  
            sh "git pull origin development"           
            sh "git push https://${GITHUB_USR}:${GITHUB_PSW}@github.com/VirtualL/workshop_ci_cd.git development:master"              

        }
        failure {
            echo "This pipeline BUILD_ID: ${env.BUILD_ID} on ${env.JENKINS_URL} failed!"
        }
    }
}