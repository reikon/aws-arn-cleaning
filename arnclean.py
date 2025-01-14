import boto3
import sys
from collections import defaultdict

def parse_arn(arn):
    parts = arn.split(':')
    if len(parts) >= 6:
        service = parts[2]
        region = parts[3]
        resource_type = parts[5].split('/')[0] if '/' in parts[5] else parts[5]
        resource_id = parts[5].split('/')[1] if '/' in parts[5] else parts[5]
        return service, region, resource_type, resource_id
    return None, None, None, None

def delete_resources(arns):
    # Group resources by region
    resources_by_region = defaultdict(list)
    for arn in arns:
        service, region, resource_type, resource_id = parse_arn(arn)
        if service and region:
            resources_by_region[region].append((resource_type, resource_id))

    for region, resources in resources_by_region.items():
        print(f"Processing region: {region}")
        ec2 = boto3.client('ec2', region_name=region)
        
        # Delete in correct order to handle dependencies
        # 1. Delete Subnets
        for res_type, res_id in resources:
            if res_type == 'subnet':
                try:
                    ec2.delete_subnet(SubnetId=res_id)
                    print(f"Deleted subnet: {res_id}")
                except Exception as e:
                    print(f"Error deleting subnet {res_id}: {str(e)}")

        # 2. Delete Internet Gateways
        for res_type, res_id in resources:
            if res_type == 'internet-gateway':
                try:
                    # First detach from VPC
                    vpcs = ec2.describe_internet_gateways(InternetGatewayIds=[res_id])
                    for igw in vpcs['InternetGateways']:
                        for attachment in igw['Attachments']:
                            ec2.detach_internet_gateway(
                                InternetGatewayId=res_id,
                                VpcId=attachment['VpcId']
                            )
                    # Then delete
                    ec2.delete_internet_gateway(InternetGatewayId=res_id)
                    print(f"Deleted internet gateway: {res_id}")
                except Exception as e:
                    print(f"Error deleting internet gateway {res_id}: {str(e)}")

        # 3. Delete Route Tables (except main)
        for res_type, res_id in resources:
            if res_type == 'route-table':
                try:
                    # Skip if main route table
                    rt = ec2.describe_route_tables(RouteTableIds=[res_id])
                    if not any(assoc.get('Main', False) for assoc in rt['RouteTables'][0]['Associations']):
                        ec2.delete_route_table(RouteTableId=res_id)
                        print(f"Deleted route table: {res_id}")
                except Exception as e:
                    print(f"Error deleting route table {res_id}: {str(e)}")

        # 4. Delete Network ACLs (except default)
        for res_type, res_id in resources:
            if res_type == 'network-acl':
                try:
                    # Skip if default NACL
                    nacl = ec2.describe_network_acls(NetworkAclIds=[res_id])
                    if not nacl['NetworkAcls'][0]['IsDefault']:
                        ec2.delete_network_acl(NetworkAclId=res_id)
                        print(f"Deleted network ACL: {res_id}")
                except Exception as e:
                    print(f"Error deleting network ACL {res_id}: {str(e)}")

        # 5. Delete Security Groups (except default)
        for res_type, res_id in resources:
            if res_type == 'security-group':
                try:
                    # Skip if default security group
                    sg = ec2.describe_security_groups(GroupIds=[res_id])
                    if sg['SecurityGroups'][0]['GroupName'] != 'default':
                        ec2.delete_security_group(GroupId=res_id)
                        print(f"Deleted security group: {res_id}")
                except Exception as e:
                    print(f"Error deleting security group {res_id}: {str(e)}")

        # 6. Delete VPCs
        for res_type, res_id in resources:
            if res_type == 'vpc':
                try:
                    ec2.delete_vpc(VpcId=res_id)
                    print(f"Deleted VPC: {res_id}")
                except Exception as e:
                    print(f"Error deleting VPC {res_id}: {str(e)}")

        # 7. Delete DHCP Options
        for res_type, res_id in resources:
            if res_type == 'dhcp-options':
                try:
                    ec2.delete_dhcp_options(DhcpOptionsId=res_id)
                    print(f"Deleted DHCP options: {res_id}")
                except Exception as e:
                    print(f"Error deleting DHCP options {res_id}: {str(e)}")

if __name__ == "__main__":
    # Read ARNs from a file or pass them as a list
    arns = [line.strip() for line in sys.stdin.readlines()]
    delete_resources(arns)
