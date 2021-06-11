# pollinate

Build Process:
In order to access DynamoDB, the Python runtime in the Docker image needs access to an AWS IAM user keypair. 
To embed these secrets (I don't have the time to create a proper secrets management framework over a weekend!), export them as environment variables and pass them to the docker build command as follows:

$ export aws_id="NOT_A_REAL_ID"
$ export aws_key="NOT_A_REAL_SECRET_KEY"
$ docker build --tag python-docker --secret id=aws_id --secret id=aws_key .