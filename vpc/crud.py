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
