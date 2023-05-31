# AWS BTU
# S3 CLI + host static

That's S3 CLI tool, created for educational purposes. Don't forget to check `.env.example` file to see all the required credentials to allow CLI script work correctly.

## Install
First install:
```
https://github.com/ahupp/python-magic
```

```
poetry install
```

## Usage

First run in shell help command, to see the message about avaliable CLI functions, it can listen for passed `-h`, or `--help`:

```shell
python main.py -h
```

## Bucket
Commands works without  `""` too.

### Create bucket

```shell
python main.py bucket "any-name-for-s3" -cb
```

### Create bucket and Enable Versining

```shell
python main.py bucket "bucket-with-vers-2" -cb -vers True
```

### Organize bucket per extensions

```shell
python main.py bucket "bucket-with-vers" -o_b
```
```

### Show bucket's objects tree

```shell
python main.py bucket "bucket-with-vers" --show_bucket_tree
```


## Object

Upload local object from /static folder.
```shell
python main.py object "bucket-with-vers" --local_object "important.txt" --upload_type "upload_file"
```

Upload object link.
```shell
python main.py object bucket_name "new-bucket-btu-7" -ol "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4" -du
```
List object versions

```shell
python main.py object "important.txt" "bucket-with-vers" -l_v 
```

Rollback to version

```shell
python main.py object "important.txt" "bucket-with-vers" -r_b_t "En8tj6pxH3nduvOzGpEs5RP5QN6M5UQ6"
```
## List Buckets


```shell
python main.py list_buckets
```

## Host
Enable public read permission on Bucket

```shell
python main.py bucket "your-bucket-name" --assign_read_policy
```

Set "WebsiteConfiguration"

```shell
python main.py host "your-bucket-name" --website_configuration True
```

Host static file

```shell
python main.py host "your-bucket-name" --host_static "index.html"
```


Host static file with folders

```shell
python main.py host "your-bucket-name" --host_static "separate_project"
```

Upload static web page to s3 

```shell
python main.py host nztest11111 --source "html_demo_site"
```
Result
```
website configuration assigned
public read policy assigned!
text/html text/html
text/plain text/plain
text/html text/html
image/jpeg image/jpeg
image/jpeg image/jpeg
image/jpeg image/jpeg
```
http://nztest11111.s3-website-us-west-2.amazonaws.com


If inspire flag empty Get a random quote.

```shell
python main.py quote "your-bucket-name" --inspire
```

If inspire flag has parameter Get quote by author.

```shell
python main.py quote "nztest1111" --inspire "Yoda"
```

Save quote as json file to an S3 bucket.

```shell
python main.py quote "nztest1111" --inspire "Yoda" --save
```

Create VPC add tag name and create and attach IGW to VPC

```shell
python main.py vpc --vpc_name nikavpctestbtu1 --subnet_id '10.0.0.0/20'
```

Create Security Group and Launch EC2 Instance
```shell
python main.py vpc --vpc_id vpc-12345678 --subnet_id 10.0.0.0/24
```

## RDS

create RDS
```shell
python main.py rds --db_instance_identifier db-instance-name --security_group_id sg-123456789
```
