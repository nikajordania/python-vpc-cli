def print_dynamodb_tables(dynamodb_client):
    try:
        response = dynamodb_client.list_tables()

        print('DynamoDB tables:')
        for table_name in response['TableNames']:
            print(table_name)
    except Exception as e:
        print('Error listing DynamoDB tables:', str(e))
