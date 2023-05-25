from datetime import datetime
from common.common_functions import get_ip_address


def list_vpcs(ec2_client):
    result = ec2_client.describe_vpcs()
    vpcs = result.get("Vpcs")
    print(vpcs)


def create_vpc(ec2_client):
    result = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
    vpc = result.get("Vpc")
    print(vpc)

    return result


def add_name_tag(ec2_client, vpc_id, vpc_name):
    ec2_client.create_tags(Resources=[vpc_id],
                           Tags=[{
                               "Key": "Name",
                               "Value": vpc_name
                           }])


def create_igw(ec2_client):
    result = ec2_client.create_internet_gateway()
    return result.get("InternetGateway").get("InternetGatewayId")


def attach_igw_to_vpc(ec2_client, vpc_id, igw_id):
    ec2_client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

def create_subnet(ec2_client, vpc_id, subnet_cidr):
    response = ec2_client.create_subnet(
        VpcId=vpc_id,
        CidrBlock=subnet_cidr
    )
    
    return response['Subnet']['CidrBlock']


def create_security_group(ec2_client, vpc_id, subnet_id):
    response = ec2_client.create_security_group(
        Description='Allow HTTP and SSH access',
        GroupName='my-security-group' + str(datetime.now()),
        VpcId=vpc_id
    )
    
    security_group_id = response['GroupId']
    
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': get_ip_address()}]
            }
        ]
    )
    
    return security_group_id


def create_key_pair(ec2_client):
    now = datetime.now()
    key_name = f'key_{now.strftime("%Y-%m-%d_%H-%M-%S")}'

    response = ec2_client.create_key_pair(KeyName=key_name)

    with open(f'{key_name}.pem', 'w') as f:
        f.write(response['KeyMaterial'])

    return response['KeyPairId'], key_name


def launch_ec2_instance(ec2_client, image_id, instance_type, subnet_id, security_group_id, key_pair_name):
    response = ec2_client.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        SubnetId=subnet_id,
        SecurityGroupIds=[security_group_id],
        KeyName=key_pair_name,
        MinCount=1,
        MaxCount=1,
        UserData='',
        InstanceInitiatedShutdownBehavior='terminate',
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'VolumeSize': 10,
                    'VolumeType': 'gp2'
                }
            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'MyInstance'}
                ]
            }
        ]
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    
    return instance_id, public_ip
