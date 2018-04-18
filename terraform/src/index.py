import os

import boto3
import certifi
import curator
from curator.exceptions import NoIndices
from elasticsearch import Elasticsearch
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection



# This is the entry point where Lambda will start execution.
def handler(event, context):
    es_host = os.environ.get('endpoint')
    delete_after = int(os.environ.get('delete_after'))

    session = boto3.session.Session()
    credentials = session.get_credentials().get_frozen_credentials()

    awsauth = AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_token=credentials.token,
        aws_host=es_host,
        aws_region=session.region_name,
        aws_service='es'
    )

    es = Elasticsearch(
        hosts="%s:443" % es_host,
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        ca_certs=certifi.where(),
        connection_class=RequestsHttpConnection
    )

    prefix = os.environ.get('prefix')
    print('Checking "%s" indices.' % prefix)

    # fetch index names
    index_list = curator.IndexList(es)
    try:
        # filter out by prefix and age
        index_list.filter_by_regex(kind='prefix', value=prefix)
        index_list.filter_by_age(source='name', direction='older',
                                 timestring=os.environ.get('timestring'), unit='days',
                                 unit_count=delete_after)
        print('Trigger delete %s .' % index_list)
        curator.DeleteIndices(index_list).do_action()
    # If nothing is left in the list, we'll get a NoIndices exception.
    # That's OK.
    except NoIndices:
        pass

    # Record the names of any indices we removed.
    lambda_response = {'deleted': index_list.working_list()}
    return lambda_response
