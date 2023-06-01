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


def increase_memory(rds_client, db_instance_identifier, memory_increase_percent):
    try:
        response = rds_client.describe_db_instances(
            DBInstanceIdentifier=db_instance_identifier)
        if 'DBInstances' in response and len(response['DBInstances']) > 0:
            db_instance = response['DBInstances'][0]
            current_memory = db_instance['DBInstanceClass'].split('.')[1]
            new_memory = int(current_memory) + int(current_memory) * \
                memory_increase_percent // 100

            response = rds_client.modify_db_instance(
                DBInstanceIdentifier=db_instance_identifier,
                DBInstanceClass=db_instance['DBInstanceClass'].replace(
                    current_memory, str(new_memory))
            )

            print('RDS instance memory increased successfully!')
            print('New instance class:',
                  response['DBInstance']['DBInstanceClass'])
        else:
            print('RDS instance not found:', db_instance_identifier)
    except Exception as e:
        print('Error increasing RDS instance memory:', str(e))


def create_rds_snapshot(rds_client, db_instance_identifier, snapshot_identifier):
    try:
        response = rds_client.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=db_instance_identifier
        )
        
        print('RDS snapshot created successfully!')
        print('Snapshot ID:', response['DBSnapshot']['DBSnapshotIdentifier'])
    except Exception as e:
        print('Error creating RDS snapshot:', str(e))
