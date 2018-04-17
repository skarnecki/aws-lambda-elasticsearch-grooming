import os

import certifi
import curator
from curator.exceptions import NoIndices
from elasticsearch import Elasticsearch


# This is the entry point where Lambda will start execution.
def handler(event, context):
    # Create a place to track any indices that are deleted.
    deleted_indices = {}
    print('xx %s' % os.environ.get('endpoint', 'x'))
    es = Elasticsearch(os.environ.get('endpoint', 'x'), use_ssl=True,
                       verify_certs=True, ca_certs=certifi.where())

    prefix = os.environ.get('prefix')
    print('Checking "%s" indices.' % prefix)

    # fetch index names
    index_list = curator.IndexList(es)
    try:
        # filter out by prefix and age
        index_list.filter_by_regex(kind='prefix', value=prefix)
        index_list.filter_by_age(source='name', direction='older',
                                 timestring=os.environ.get('timestring'), unit='days',
                                 unit_count=int(os.environ.get('delete_after')))
        print('Trigger delete %s .' % index_list)
        curator.DeleteIndices(index_list).do_action()
    # If nothing is left in the list, we'll get a NoIndices exception.
    # That's OK.
    except NoIndices:
        pass

    # Record the names of any indices we removed.
    lambda_response = {'deleted': index_list.working_list()}
    return lambda_response
