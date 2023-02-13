pipeline {
//None parameter in the agent section means that no global agent will be allocated for the entire Pipeline’s
//execution and that each stage directive must specify its own agent section.
    agent any
    parameters {
        string defaultValue: '300', name: 'INTERVAL'
    }
    environment {
        AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
        DOCKER = credentials('jenkins-dockerhub')
    }
    stages {
        stage('Init') {
            steps {
                //cleanWs()
                echo "Init stage"
                echo "Running BUILD_ID: ${env.BUILD_ID} on ${env.JENKINS_URL}"
                echo "INTERVAL in sec: ${params.INTERVAL}"
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
                    sh "pwd"
                    sh "ls"
                    sh "docker rm -f boto3_ip_finder"                
                    sh "docker build -t boto3_ip_finder ."                    
                }
                sh"""
                docker login -u ${DOCKER_USR} -p ${DOCKER_PSW}
                docker image tag boto3_ip_finder virtuall4u/workshop_ci_cd:${env.BUILD_ID}
                docker push virtuall4u/workshop_ci_cd:${env.BUILD_ID}

                docker image tag boto3_ip_finder virtuall4u/workshop_ci_cd:latest
                docker push virtuall4u/workshop_ci_cd:latest
                """
            }
        }

        stage('Deploy') {
            steps {
                sh "docker run -itd --name boto3_ip_finder --env INTERVAL=${params.INTERVAL}  --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}  --env AWS_DEFAULT_REGION=eu-west-1 boto3_ip_finder"
                sleep 10
                sh "docker logs boto3_ip_finder"                
            }
        }      
    }
    post {
        success {
            echo "This pipeline BUILD_ID: ${env.BUILD_ID} on ${env.JENKINS_URL} finshed successfully"
        }
        failure {
            echo "This pipeline BUILD_ID: ${env.BUILD_ID} on ${env.JENKINS_URL} failed!"
        }
    }
}