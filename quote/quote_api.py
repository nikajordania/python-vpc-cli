from datetime import datetime
import json
from os import getenv
import random
import requests


def get_quotes():
    response = requests.get("https://type.fit/api/quotes")
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_random_quote(quotes):
    return random.choice(quotes)


def get_random_quote_by_author(author, quotes):
    filter_by_authors = [q for q in quotes if q['author'] == author]
    return random.choice(filter_by_authors)


def save_to_s3(s3_client, bucket_name, quote):
    now = datetime.now()
    filename = f'quote_{now.strftime("%Y-%m-%d_%H-%M-%S")}.json'

    s3_client.put_object(
        Body=json.dumps(quote, indent=4),
        Bucket=bucket_name,
        Key=filename
    )

    # public URL
    return "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        getenv("aws_s3_region_name", "us-west-2"),
        bucket_name,
        filename
    )
