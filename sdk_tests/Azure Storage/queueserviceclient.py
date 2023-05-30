import datetime
from azure.storage.queue import QueueServiceClient, QueueAnalyticsLogging, RetentionPolicy, Metrics, CorsRule
import random


class MyQueueServiceClient:
    def __init__(self, emulator=True, queue_name=None):
        # queue name
        if queue_name is None:
            self.queue_name = f'queue{random.randint(1, 1000000000)}'
        else:
            self.queue_name = queue_name

        self.account_name = 'sdkfuzz'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=Kt8fMYDEpeaq/A6TRBU+1+LRMIqd2h9Nv7Hd/qCn4B9DqvbNDXPJWU4BRqu50GVEjFfcocumL1lr+AStfVsaPA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'

        # create a queue
        self.queue_service_client = QueueServiceClient.from_connection_string(self.connection_string)
        self.queue_service_client.create_queue(self.queue_name)



    # create queue with try except
    def queue_create(self, *args):
        args = list(args)

        queue_name = f'queue{random.randint(1, 1000000000)}'
        
        try:
            self.queue_service_client.create_queue(queue_name)
            print(self.service, ': Success -- Queue created')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue creation failed; error: ', e)
            return False
        

    # delete queue with try except
    def queue_delete(self, *args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.queue_name)
        
        try:
            self.queue_service_client.delete_queue(args[0])
            print(self.service, ': Success -- Queue deleted')
            # create another queue in its place
            self.queue_service_client.create_queue(f'queue{random.randint(1, 1000000000)}')
            print(self.service, ': Success -- Queue created')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue deletion failed; error: ', e)
            return False
        

    # get queue client with try except
    def queue_get_client(self, *args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.queue_name)
        
        try:
            queue_client = self.queue_service_client.get_queue_client(args[0])
            print(self.service, ': Success -- Queue client retrieved')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue client retrieval failed; error: ', e)
            return False
        

    # get service properties with try except
    def queue_get_service_properties(self, *args):
        args = list(args)
        try:
            self.queue_service_client.get_service_properties()
            print(self.service, ': Success -- Service properties retrieved')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Service properties retrieval failed; error: ', e)
            return False
        

    # get service stats with try except
    def queue_get_service_stats(self, *args):
        args = list(args)
        try:
            self.queue_service_client.get_service_stats()
            print(self.service, ': Success -- Service stats retrieved')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Service stats retrieval failed; error: ', e)
            return False
        

    # list queues with try except
    def queue_list(self, *args):
        args = list(args)
        try:
            self.queue_service_client.list_queues()
            print(self.service, ': Success -- Queues listed')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue listing failed; error: ', e)
            return False
        

    # set service properties with try except
    def queue_set_service_properties(self, *args):

        analytics_logging = QueueAnalyticsLogging(read=True, write=True, delete=True, retention_policy=RetentionPolicy(enabled=True, days=5))
        hour_metrics = Metrics(version='1.0', enabled=True, include_apis=True, retention_policy=RetentionPolicy(enabled=True, days=5))
        minute_metrics = Metrics(version='1.0', enabled=True, include_apis=True, retention_policy=RetentionPolicy(enabled=True, days=5))
        cors = [CorsRule(allowed_origins=['*'], allowed_methods=['GET', 'PUT'], allowed_headers=['*'], exposed_headers=['*'], max_age_in_seconds=3600)]

        try:
            self.queue_service_client.set_service_properties(analytics_logging=analytics_logging, hour_metrics=hour_metrics, minute_metrics=minute_metrics, cors=cors)
            print(self.service, ': Success -- Service properties set')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Service properties setting failed; error: ', e)
            return False


# if __name__ == '__main__':


#     # create a queue
#     qc = MyQueueServiceClient(emulator=False)
#     # list all queues
#     queues = qc.queue_service_client.list_queues()
#     # delete all queues
#     for queue in queues:
#         qc.queue_service_client.delete_queue(queue.name)
    