import datetime
from azure.data.tables import TableClient, TableServiceClient, TableEntity, UpdateMode
import random


class MyTableServiceClient():

    def __init__(self, emulator=True, table_name=None):
        # table name
        if table_name is None:
            self.table_name = f'table{random.randint(1, 1000000000)}'
        else:
            self.table_name = table_name

        self.account_name = 'restlertest1'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=restlertest1;AccountKey=En0z7F3kBwgMv8YIlU57bifLmr2Nb71m4sNVndRvtFiOlpWRNhnlOOPsJG5C7uwZgP92rkFFj4rx+AStw5Q7sA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'


        # create table service client
        self.table_service_client = TableServiceClient.from_connection_string(self.connection_string)
        self.table_service_client.create_table(self.table_name)



    # create table if not exists with try except
    def table_create(self):
        try:
            self.table_service_client.create_table_if_not_exists(self.table_name)
            print(self.service, ': Table created')
            return True
        except Exception as e:
            print(self.service, ': Table creation failed; error: ', e)
            return False
        

    # delete table with try except
    def table_delete(self):
        try:
            self.table_service_client.delete_table(self.table_name)
            print(self.service, ': Table deleted')
            return True
        except Exception as e:
            print(self.service, ': Table deletion failed; error: ', e)
            return False
        

    # get service properties with try except
    def table_get_service_properties(self):
        try:
            self.table_service_client.get_service_properties()
            print(self.service, ': Service properties retrieved')
            return True
        except Exception as e:
            print(self.service, ': Service properties retrieval failed; error: ', e)
            return False
        

    # get service stats with try except
    def table_get_service_stats(self):
        try:
            self.table_service_client.get_service_stats()
            print(self.service, ': Service stats retrieved')
            return True
        except Exception as e:
            print(self.service, ': Service stats retrieval failed; error: ', e)
            return False
        

    # get table client with try except
    def table_get_table_client(self):
        try:
            self.table_service_client.get_table_client(self.table_name)
            print(self.service, ': Table client retrieved')
            return True
        except Exception as e:
            print(self.service, ': Table client retrieval failed; error: ', e)
            return False
        
    # list tables with try except
    def table_list_tables(self):
        try:
            self.table_service_client.list_tables()
            print(self.service, ': Tables listed')
            return True
        except Exception as e:
            print(self.service, ': Tables listing failed; error: ', e)
            return False
        

    # query tables with try except
    def table_query_tables(self, query=None):
        if query is None:
            query = "TableName eq 'table1'"
        try:
            self.table_service_client.query_tables(query)
            print(self.service, ': Tables queried')
            return True
        except Exception as e:
            print(self.service, ': Tables query failed; error: ', e)
            return False
        
    # 500 Internal Server Error
    # set service properties with try except
    def table_set_service_properties(self, properties=None):
        if properties is None:
            properties = {
                'analytics_logging': {
                    'version': '1.0',
                    'delete': True,
                    'read': True,
                    'write': True,
                    'retention_policy': {
                        'enabled': True,
                        'days': 7
                    }
                },
                'hour_metrics': {
                    'version': '1.0',
                    'enabled': True,
                    'include_apis': True,
                    'retention_policy': {
                        'enabled': True,
                        'days': 7
                    }
                },
                'minute_metrics': {
                    'version': '1.0',
                    'enabled': True,
                    'include_apis': True,
                    'retention_policy': {
                        'enabled': True,
                        'days': 7
                    }
                },
                'cors': {
                    'cors_rules': [
                        {
                            'allowed_origins': ['*'],
                            'allowed_methods': ['GET'],
                            'max_age_in_seconds': 3600,
                            'exposed_headers': ['x-ms-request-id'],
                            'allowed_headers': ['*']
                        }
                    ]
                }
            }
        try:
            self.table_service_client.set_service_properties(analytics_logging=properties['analytics_logging'],)
            print(self.service, ': Service properties set')
            return True
        except Exception as e:
            print(self.service, ': Service properties set failed; error: ', e)
            return False
        


if __name__ == '__main__':


    # create blob client
    table_client = MyTableServiceClient(False)
    # get all methods
    methods = [getattr(MyTableServiceClient, attr) for attr in dir(MyTableServiceClient) if callable(getattr(MyTableServiceClient, attr)) and not attr.startswith("__")]

    for i in methods:
        print(i.__name__)
        i(table_client)