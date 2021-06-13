# pollinate

Heavily adapted from Hashicorp's publicly available EKS demo workspace.
In order to provision the infrastructure, clone the repository and then run a terraform apply.

This will provision the following resources:

- EKS cluster
- VPC
- Subnets
- IGW
- NAT Gateway
- Host Instances with k8s AMI
- EC2 Autoscaling Group
- Classic ELB
- DynamoDB table for logging of connections

Once provisioning is complete, you can run a `aws eks --region ap-southeast-2 update-kubeconfig --name <resultant EKS name>`  (with correctly configured local AWS profile) in order to update your local `~/.kube/config` file. With this you can then interact with the provisioned EKS cluster. 

To deploy the app, run a `kubectl apply -f deploy/deployment.yaml`  to provision the load balancing service as well as the actual pod deployment of the application. This creates a basic load balancer service on port 80 within the cluster's virtual network and pulls the most recent image from Docker Hub to run the application. The image pulled has been pre-published as part of the development but can be recreated using the provided Dockerfile and Python script using `docker build --tag python-docker deploy/docker` then pushing to Docker hub. Note that the deployment.yaml file will need to be updated to use whatever Docker image you may republish.
  
The default configuration for this is 2 hosts provisioned, with 4 deployed pods for the service total. This can be updated using `kubectl`.
  
Each instance of the app will serve requests. The provisioned DynamoDB instance acts as the NOSQL database of connection times.
