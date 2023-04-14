from bucket.policy import assign_policy
from host_static.host_web_page_files import static_web_page_file
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-static-web-host.html
def set_bucket_website_policy(aws_s3_client, bucket_name, switch):
    website_configuration = {
        # 'ErrorDocument': {'Key': 'error.html'},
        "IndexDocument": {"Suffix": "index.html"},
    }

    response = None

    if switch:
        response = aws_s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration=website_configuration)
    else:
        response = aws_s3_client.delete_bucket_website(Bucket=bucket_name)

    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True
    return False


def source_to_web_host(s3_client, args):
        if set_bucket_website_policy(s3_client, args.bucket_name, True):
            print("website configuration assigned")
        else:
            print("website configuration unassigned")
        
        assign_policy(s3_client, "public_read_policy", args.bucket_name)
        print(static_web_page_file(s3_client, args.bucket_name, args.source))
