# pollinate

Heavily adapted from Hashicorp's publicly available EKS demo workspace.
In order to provision the infrastructure, clone the repository and then run a terraform apply.

This will provision the following resources:

- EKS cluster
- VPC
- Subnets
- IGW
- NAT Gateway
- Instances
- Classic ELB
- DynamoDB table for logging of connections

Once provisioning is complete, you can run a aws eks --region us-east-2 update-kubeconfig --name <resultant EKS name>  in order to update your local ~/.kube/config file. With this you can then interact with the provisioned EKS cluster. To deploy the app, run a kubectl apply -f ./deployment.yaml  to provision the load balancing service as well as the actual pod deployment of the application.
  
The default configuration for this is 3 hosts provisioned, with 4 deployed pods on each.
  
Each instance of the app will serve requests. The provisioned DynamoDB instance acts as the NOSQL database of connection times.
