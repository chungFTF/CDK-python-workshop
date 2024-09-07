from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager
)
from constructs import Construct
from aws_cdk import CfnOutput
import json

class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc_name = 'vpc-workshop5'
        self.vpc_cidr = '10.1.0.0/16'

        self.__create_vpc()
    
    # Create VPC
    def __create_vpc(self):
        vpc_construct_id = 'vpc'
        MY_IP = ""

        vpc = ec2.Vpc(
            self, vpc_construct_id,
            vpc_name=self.vpc_name,
            ip_addresses=ec2.IpAddresses.cidr(self.vpc_cidr),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name='Public',
                    cidr_mask=24
                ), ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    name='Private',
                    cidr_mask=24
                )
            ]
        )


        # Create EC2 Security Group
        ec2_sec_group = ec2.SecurityGroup(
            self, "EC2_sec_group", vpc=vpc, allow_all_outbound=True
        )
        ec2_sec_group.add_ingress_rule(ec2.Peer.ipv4(MY_IP), ec2.Port.tcp(22), "allow SSH access")
        ec2_sec_group.add_ingress_rule(ec2.Peer.ipv4("13.209.1.56/29"), ec2.Port.tcp(22), "allow SSH access from EC2 console")
        ec2_sec_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow HTTP access")


        # Create EC2 instance
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ec2/README.html
        # https://docs.aws.amazon.com/linux/al2023/ug/what-is-amazon-linux.html
        ec2_w5_instance = ec2.Instance(
            self,
            "Public_instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=ec2_sec_group,
            associate_public_ip_address=True
        )

        # Create Secret Manager to store RDS password
        secret_db_creds = secretsmanager.Secret(
            self,
            "secret_db_creds",
            secret_name="w5/db_creds",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "admin"}),
                exclude_punctuation=True,
                generate_string_key="password",
            ),
        )

        # Create RDS Security Group
        db_sec_group = ec2.SecurityGroup(
                                    self,
                                    "db_sec_group",
                                    vpc=vpc,
                                    security_group_name="db_sec_group",
                                    allow_all_outbound=True
                                )

        # Add ingress rule to allow EC2 security group access

        db_sec_group.add_ingress_rule(
            peer=ec2_sec_group,
            connection=ec2.Port.tcp(3306),
            description="Allow access from EC2 security group"
        )

        # Create an RDS Database
        myDB = rds.DatabaseInstance(self, 
            "W5Database",
            engine= rds.DatabaseInstanceEngine.MYSQL,
            vpc= vpc,
            vpc_subnets= ec2.SubnetSelection(
                subnet_type= ec2.SubnetType.PRIVATE_ISOLATED
            ),
            credentials=rds.Credentials.from_secret(secret_db_creds),
            instance_type= ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
            port= 3306,
            allocated_storage= 80,
            multi_az= True,
            deletion_protection= False,
            security_groups=[db_sec_group]
        )

        # Output RDS endpoint
        CfnOutput(self, 
                  "db_endpoint",
                  value= myDB.db_instance_endpoint_address)
        

