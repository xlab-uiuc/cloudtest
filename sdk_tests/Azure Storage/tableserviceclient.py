from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential
import random, os, datetime

# Point to certificates
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()


class MyTableServiceClient():

    def __init__(self, emulator=True, table_name=None):

        # randomize seed
        random.seed(datetime.datetime.now())

        print("****************************************************************************")

        # table name
        if table_name is None:
            self.table_name = f'table{random.randint(1, 1000000000)}'
        else:
            self.table_name = table_name

        self.account_name = 'sdkfuzz'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=https://127.0.0.1:10002/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=LGHPh+f0PHvNw8PVYtEkN0fWsqWO9ZsY3DrQox0veta/Ii+aW3m/E7VLVFna/qDMqm/CCg4lou9N+AStwMBcgA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'

        # credential
        global credential

        # create table service client
        try:
            self.table_service_client = TableServiceClient.from_connection_string(self.connection_string)
        except Exception as e:
            print('Table service client creation failed; error: ', e)

        try:
            self.table_service_client.create_table(self.table_name)
        except:
            pass



    # create table if not exists with try except
    def table_create(self, *args):
        args = list(args)
        try:
            self.table_service_client.create_table_if_not_exists(self.table_name)
            print(self.service, ': Table created')
            return True
        except Exception as e:
            print(self.service, ': Table creation failed; error: ', e)
            return False
        

    # delete table with try except
    def table_delete(self, *args):
        args = list(args)
        try:
            self.table_service_client.delete_table(self.table_name)
            print(self.service, ': Table deleted')
            # create table again
            self.table_service_client.create_table_if_not_exists(self.table_name)
            return True
        except Exception as e:
            print(self.service, ': Table deletion failed; error: ', e)
            return False
        

    # get service properties with try except
    def table_get_service_properties(self, *args):
        args = list(args)
        try:
            self.table_service_client.get_service_properties()
            print(self.service, ': Service properties retrieved')
            return True
        except Exception as e:
            print(self.service, ': Service properties retrieval failed; error: ', e)
            return False
        

    # get service stats with try except
    def table_get_service_stats(self, *args):
        args = list(args)
        try:
            self.table_service_client.get_service_stats()
            print(self.service, ': Service stats retrieved')
            return True
        except Exception as e:
            print(self.service, ': Service stats retrieval failed; error: ', e)
            return False
        

    # get table client with try except
    def table_get_table_client(self, *args):
        args = list(args)
        try:
            self.table_service_client.get_table_client(self.table_name)
            print(self.service, ': Table client retrieved')
            return True
        except Exception as e:
            print(self.service, ': Table client retrieval failed; error: ', e)
            return False
        
    # list tables with try except
    def table_list_tables(self, *args):
        args = list(args)
        try:
            self.table_service_client.list_tables()
            print(self.service, ': Tables listed')
            return True
        except Exception as e:
            print(self.service, ': Tables listing failed; error: ', e)
            return False
        

    # query tables with try except
    def table_query_tables(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append("TableName eq 'table1'")
        try:
            self.table_service_client.query_tables(args[0])
            print(self.service, ': Tables queried')
            return True
        except Exception as e:
            print(self.service, ': Tables query failed; error: ', e)
            return False
        
    # 500 Internal Server Error
    # set service properties with try except
    def table_set_service_properties(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append({
                'analytics_logging': {
                    'version': '1.0',
                    'delete': True,
                    'read': True,
                    'write': True,
                    'retention_policy': {
                        'enabled': True,
                        'days': 7
                    }
                }
            })
        
        if not len(args) > 1:
            args.append({
                'hour_metrics': {
                    'version': '1.0',
                    'enabled': True,
                    'include_apis': True,
                    'retention_policy': {
                        'enabled': True,
                        'days': 7
                    }
                }
            })
        if not len(args) > 2:
            args.append({
                'minute_metrics': {
                    'version': '1.0',
                    'enabled': True,
                    'include_apis': True,
                    'retention_policy': {
                        'enabled': True,
                        'days': 7
                    }
                }
            })
        if not len(args) > 3:
            args.append({
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
            })
            
        try:
            self.table_service_client.set_service_properties(analytics_logging=args[0], hour_metrics=args[1], minute_metrics=args[2], cors=args[3])
            print(self.service, ': Service properties set')
            return True
        except Exception as e:
            print(self.service, ': Service properties set failed; error: ', e)
            return False
        

    # garbage collection
    def __cleanup__(self):

        try:
            tables = self.table_service_client.list_tables()
            # list tables 
            for table in tables:
                try:
                    self.table_service_client.delete_table(table.name)
                    print('Table deleted: ', table.name)
                except:
                    print('Table deletion failed: ', table.name)

        except Exception as e:

            print('Tables could not be listed: ', e)

