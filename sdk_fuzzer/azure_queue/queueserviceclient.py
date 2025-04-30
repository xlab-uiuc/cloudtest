import datetime
from azure.storage.queue import QueueServiceClient, QueueAnalyticsLogging, RetentionPolicy, Metrics, CorsRule
from azure.identity import DefaultAzureCredential
import random, json

# Point to certificates
# os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()
config = json.loads(open('config.json').read())

class MyQueueServiceClient:
    def __init__(self, emulator=True, queue_name=None):

        # randomize seed
        random.seed(datetime.datetime.now())
        
        # queue name
        if queue_name is None:
            self.queue_name = f'queue{random.randint(1, 1000000000)}'
        else:
            self.queue_name = queue_name

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

        try:
            # create a queue
            self.queue_service_client = QueueServiceClient.from_connection_string(self.connection_string, credential=credential)
        except Exception as e:
            print('Queue service client creation failed; error: ', e)
            
        try:
            self.queue_service_client.create_queue(self.queue_name)
        except Exception as e:
            print('Queue creation failed; error: ', e)



    # create queue with try except
    def queue_create(self, args):
        args = list(args)

        queue_name = f'queue{random.randint(1, 1000000000)}'
        
        try:
            res = self.queue_service_client.create_queue(queue_name)
            print(self.service, ': Success -- Queue created')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue creation failed; error: ', e)
            return False, e
        

    # delete queue with try except
    def queue_delete(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.queue_name)
        
        try:
            res = self.queue_service_client.delete_queue(args[0])
            print(self.service, ': Success -- Queue deleted')
            
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue deletion failed; error: ', e)
            return False, e
        

    # get queue client with try except
    def queue_get_client(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.queue_name)
        
        try:
            res = self.queue_service_client.get_queue_client(args[0])
            print(self.service, ': Success -- Queue client retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue client retrieval failed; error: ', e)
            return False, e
        

    # get service properties with try except
    def queue_get_service_properties(self, args):
        args = list(args)
        try:
            res = self.queue_service_client.get_service_properties()
            print(self.service, ': Success -- Service properties retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Service properties retrieval failed; error: ', e)
            return False, e
        

    # get service stats with try except
    def queue_get_service_stats(self, args):
        args = list(args)
        try:
            res = self.queue_service_client.get_service_stats()
            print(self.service, ': Success -- Service stats retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Service stats retrieval failed; error: ', e)
            return False, e
        

    # list queues with try except
    def queue_list(self, args):
        args = list(args)
        try:
            res = self.queue_service_client.list_queues()
            print(self.service, ': Success -- Queues listed')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue listing failed; error: ', e)
            return False, e
        

    # set service properties with try except
    def queue_set_service_properties(self, args):

        analytics_logging = QueueAnalyticsLogging(read=True, write=True, delete=True, retention_policy=RetentionPolicy(enabled=True, days=5))
        hour_metrics = Metrics(version='1.0', enabled=True, include_apis=True, retention_policy=RetentionPolicy(enabled=True, days=5))
        minute_metrics = Metrics(version='1.0', enabled=True, include_apis=True, retention_policy=RetentionPolicy(enabled=True, days=5))
        cors = [CorsRule(allowed_origins=['*'], allowed_methods=['GET', 'PUT'], allowed_headers=['*'], exposed_headers=['*'], max_age_in_seconds=3600)]

        try:
            res = self.queue_service_client.set_service_properties(analytics_logging=analytics_logging, hour_metrics=hour_metrics, minute_metrics=minute_metrics, cors=cors)
            print(self.service, ': Success -- Service properties set')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Service properties setting failed; error: ', e)
            return False, e

    # garbage collection
    def __cleanup__(self):

        try:
            queues = self.queue_service_client.list_queues()
            # list queues 
            for queue in queues:
                try: 
                    # delete queue
                    self.queue_service_client.delete_queue(queue.name)
                    print(f'Queue deleted in GC -- {self.service}')
                except:
                    print(f'Queue deletion failed in GC -- {self.service}')

        except:
            print(f'Queue list failed in GC -- {self.service}')


    