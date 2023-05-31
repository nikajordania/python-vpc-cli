def create_rds_instance(rds_client, args):
    try:
        response = rds_client.create_db_instance(
            DBInstanceIdentifier=args.db_instance_identifier,
            AllocatedStorage=args.allocated_storage,
            Engine=args.engine,
            DBInstanceClass=args.db_instance_class,
            VpcSecurityGroupIds=[args.security_group_id],
            PubliclyAccessible=True,
            MasterUsername='admin',
            MasterUserPassword='password123'
        )

        print('RDS instance created successfully!')
        print('Instance ID:', response['DBInstance']['DBInstanceIdentifier'])

        return response

    except Exception as e:
        print('Error creating RDS instance:', str(e))
