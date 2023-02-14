This Repository is for demonstrating how CI/CD works. 

The Flow at a high level:
Developer makes code changes -> push the changes to the "development" branch ->Jenkins Job trigger->  in the Jenkins pipeline job; we build a new docker image based on the latest changes in the multi-stage build; we make some tests which include Lint testing -> new docker image created ->running the docker file on Jenkins to give the developer instant view on the app output ->if all previous steps finished successfully -> push the image to DockerHub -> Updade the chart image -> Merge the commit to "master" branch ->ArgoCD (which listen to master) run a deployment and deploy the new changes. 


Hello
This is my workshop files

in order to docker the app please use the Docker file added and run this commands (tune it for your docker Hub repo)
docker build -t mydocker2 .
docker tag mydocker2 virtuall4u/workshop3_boto3_ip:1.0.X
docker push virtuall4u/workshop3_boto3_ip:1.0.X
to run the docker :
edit environment file aws_credentials:
AWS_ACCESS_KEY_ID=YOURKEY
AWS_SECRET_ACCESS_KEY=YOUR-SECRET
AWS_DEFAULT_REGION=eu-west-1

run:
docker run --env-file aws_credentials virtuall4u/workshop3_boto3_ip:1.0.X

(same instructions here: https://hub.docker.com/repository/docker/virtuall4u/workshop3_boto3_ip/general)

because I didn't have time to implement steps 5 and the next sections
(which was on the workshop instruction "not mandatory") I was unable to make it run every 5 min
(since I need a cronTab or Jenkins server) sorry for that :)

Thank you, Eliran Turgeman