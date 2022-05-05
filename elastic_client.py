import json
from pprint import pprint

from elasticsearch import Elasticsearch

from elastic_set import elastic_settings


def connect_elasticsearch():
    """Connect."""
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Elasticsearch connection established')
    else:
        print('Elasticsearch connection failed!')
        
    return _es


def create_index(es_object, index_name):
    """Create index."""
    created = False
    settings = elastic_settings

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def delete_index(elastic_object, index_name,):
    """Delete index."""
    elastic_object.indices.delete(index=index_name)
    print('Index deleted')



def store_record(elastic_object, index_name, record):
    """Save record."""
    is_stored = True
    try:
        outcome = elastic_object.index(index=index_name, body=record)
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def search(es_object, index_name, search):
    """Find records."""
    res = es_object.search(index=index_name, body=search)
    pprint(res)



def record():
    """Create record."""
    hashtag = "Дед Мороз любит ёлка и песни"
    description = "История о том, как Деда мороз ходил на пасику"

    rec = {
        "hashtags": hashtag,
        "description": description


    }
    return json.dumps(rec)


if __name__ == '__main__':
    index_name = 'recipes'
    es = connect_elasticsearch()

    # out = create_index(es, 'index_name')
    # print(out)

    # del_in = delete_index(es, index_name)
    
    result = record()
    if es is not None:
        if create_index(es, 'recipes'):
            out = store_record(es, 'recipes', result)
            print(out)
            print('Data indexed successfully')

    if es is not None:
        # search_object = {'query': {'match': {'calories': '102'}}}
        # search_object = {'_source': ['title'], 'query': {'match': {'calories': '102'}}}
        search_object = {'query': {'match': {'hashtags': "История"}}}
        search(es, 'recipes', json.dumps(search_object))
