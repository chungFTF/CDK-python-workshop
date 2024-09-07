# CDK-python-workshop 

## Install Node.js & CDK
AWS CDK prerequisites - https://docs.aws.amazon.com/cdk/v2/guide/prerequisites.html

What is AWS CloudFormation? - https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html

## Init CDK folder
Getting started with the AWS CDK - https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html


Run the commands
```
$ cdk synth
```
Upon executing the command, the resulting CloudFormation template outlining the resource definitions for the deployment can be found in the cdk.out directory.
```
$ cdk deploy
```
This command retrieves your generated CloudFormation template and deploys it through AWS CloudFormation, which provisions your resources as part of a CloudFormation stack.



> You can go to CloudFormation console to check the deployment process and view your resource after deployment is finished.
> 
> During the execution of the cdk deploy command, you can navigate to the CloudFormation console to monitor the deployment progress, and once completed, visit the respective service consoles to inspect the provisioned resources.

