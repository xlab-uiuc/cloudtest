from azure.data.tables import TableServiceClient, TableAnalyticsLogging, TableMetrics, TableCorsRule, TableRetentionPolicy
from azure.identity import DefaultAzureCredential
import random, json, datetime

# Point to certificates
# os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()
config = json.loads(open('config.json').read())

class MyTableServiceClient():

    def __init__(self, emulator=True, table_name=None):

        # randomize seed
        random.seed(datetime.datetime.now())

        # table name
        if table_name is None:
            self.table_name = f'table{random.randint(1, 1000000000)}'
        else:
            self.table_name = table_name

        global config
        self.account_name = config['cloud_account_name']

        # connection string
        if emulator:
            self.connection_string = config['emulator_connection_string']
            self.service = "**EMULATOR**"
        else:
            self.connection_string = config['cloud_connection_string']
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
        except Exception as e:
            print('Table creation failed; error: ', e)



    # create table if not exists with try except
    def table_create(self, args):
        args = list(args)
        try:
            res = self.table_service_client.create_table_if_not_exists(self.table_name)
            print(self.service, ': Success -- Table created')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Table creation failed; error: ', e)
            return False, e
        

    # delete table with try except
    def table_delete(self, args):
        args = list(args)
        try:
            res = self.table_service_client.delete_table(self.table_name)
            print(self.service, ': Success -- Table deleted')
     
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Table deletion failed; error: ', e)
            return False, e
        

    # get service properties with try except
    def table_get_service_properties(self, args):
        args = list(args)
        try:
            res = self.table_service_client.get_service_properties()
            print(self.service, ': Success -- Service properties retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Service properties retrieval failed; error: ', e)
            return False, e
        
    # will fail on cloud without geo-replication
    # get service stats with try except
    def table_get_service_stats(self, args):
        args = list(args)
        try:
            res = self.table_service_client.get_service_stats()
            print(self.service, ': Success -- Service stats retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Service stats retrieval failed; error: ', e)
            return False, e
        

    # get table client with try except
    def table_get_table_client(self, args):
        args = list(args)
        try:
            res = self.table_service_client.get_table_client(self.table_name)
            print(self.service, ': Success -- Table client retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Table client retrieval failed; error: ', e)
            return False, e
        
    # list tables with try except
    def table_list_tables(self, args):
        args = list(args)
        try:
            res = self.table_service_client.list_tables()
            print(self.service, ': Success -- Tables listed')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Tables listing failed; error: ', e)
            return False, e
        

    # query tables with try except
    def table_query_tables(self, args):
        args = list(args)
        if not len(args) > 0:
            table_name = "mytable1"
            name_filter = "TableName eq '{}'".format(table_name)
            args.append(name_filter)
        try:
            res = self.table_service_client.query_tables(args[0])
            print(self.service, ': Success -- Tables queried')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Tables query failed; error: ', e)
            return False, e
        
    # 500 Internal Server Error
    # set service properties with try except
    def table_set_service_properties(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(TableAnalyticsLogging(read=True, write=True, delete=True, retention_policy=TableRetentionPolicy(enabled=True, days=7)))
        
        if not len(args) > 1:
            args.append(TableMetrics(version='1.0', enabled=True, include_apis=True, retention_policy=TableRetentionPolicy(enabled=True, days=7)))
             
        if not len(args) > 2:
            args.append(TableMetrics(version='1.0', enabled=True, include_apis=True, retention_policy=TableRetentionPolicy(enabled=True, days=7)))

        if not len(args) > 3:
            args.append([TableCorsRule(allowed_origins=['*'], allowed_methods=['GET'], max_age_in_seconds=3600, exposed_headers=['x-ms-request-id'], allowed_headers=['*'])])
            
        try:
            res = self.table_service_client.set_service_properties(analytics_logging=args[0], hour_metrics=args[1], minute_metrics=args[2], cors=args[3])
            print(self.service, ': Success -- Service properties set')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Service properties set failed; error: ', e)
            return False, e
        

    # garbage collection
    def __cleanup__(self):

        try:
            tables = self.table_service_client.list_tables()
            # list tables 
            for table in tables:
                try:
                    self.table_service_client.delete_table(table.name)
                    print(f'Table deleted in GC -- {self.service}')
                except:
                    print(f'Table deletion failed in GC -- {self.service}')

        except Exception as e:

            print(f'Tables could not be listed in GC -- {self.service}')

