# Salesforce function mapper
import os
from simple_salesforce import Salesforce


sf_consumer_key = os.environ.get('SF_CONSUMER_KEY')
sf_consumer_secret = os.environ.get('SF_CONSUMER_SECRET')
sf_username = os.environ.get('SF_USERNAME')
sf_password = os.environ.get('SF_PASSWORD')
sf_security_token = os.environ.get('SF_SECURITY_TOKEN')
# Salesforce credentials

sf = Salesforce(
    username=sf_username,
    password=sf_password,
    security_token=sf_security_token,
    consumer_key=sf_consumer_key,
    consumer_secret=sf_consumer_secret
)


def query_salesforce(query):
    response = sf.query(query)
    return response["records"]

def insert_salesforce(object_name, data):
    response = getattr(sf, object_name).create(data)
    return response["id"]

def update_salesforce(object_name, record_id, data):
    response = getattr(sf, object_name).update(record_id, data)
    return response

def delete_salesforce(object_name, record_id):
    response = getattr(sf, object_name).delete(record_id)
    return response

salesforce_function_mapper = {
    "query": query_salesforce,
    "insert": insert_salesforce,
    "update": update_salesforce,
    "delete": delete_salesforce
}