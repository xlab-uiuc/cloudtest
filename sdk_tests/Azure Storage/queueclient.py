import datetime
from azure.storage.queue import QueueClient, QueueServiceClient, AccessPolicy
from azure.identity import DefaultAzureCredential
import random, os

# Point to certificates
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()

class MyQueueClient:
    def __init__(self, emulator=True, queue_name=None):

        # randomize seed
        random.seed(datetime.datetime.now())

        print("****************************************************************************")
        
        # queue name
        if queue_name is None:
            self.queue_name = f'queue{random.randint(1, 1000000000)}'
        else:
            self.queue_name = queue_name

        self.account_name = 'sdkfuzz'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;QueueEndpoint=https://127.0.0.1:10001/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=LGHPh+f0PHvNw8PVYtEkN0fWsqWO9ZsY3DrQox0veta/Ii+aW3m/E7VLVFna/qDMqm/CCg4lou9N+AStwMBcgA==;EndpointSuffix=core.windows.net'
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
        except:
            pass

        try:
            self.queue_client = self.queue_service_client.get_queue_client(self.queue_name)
        except Exception as e:
            print('Queue client creation failed; error: ', e)



    # clear messages with params none try except
    def queue_clear_messages(self, *args):
        args = list(args)
        try:
            self.queue_client.clear_messages()
            print(self.service, ': Success -- Queue cleared')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue clear failed; error: ', e)
            return False


    # create queue if not exists with try except
    def queue_create(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append(f'queue{random.randint(1, 1000000000)}')
        
        try:
            self.queue_client = self.queue_client.from_connection_string(self.connection_string, args[0])
            self.queue_client.create_queue()
            print(self.service, ': Success -- Queue created')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue creation failed; error: ', e)
            return False


    # delete message with arguments as none try except
    def queue_delete_message(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append('message content')

        try:
            # send message
            resp = self.queue_client.send_message(args[0])
            print(self.service, ': Success -- Message sent')
            # msg id and pop receipt
            message_id = resp['id']
            pop_receipt = resp['pop_receipt']
            self.queue_client.delete_message(message_id, pop_receipt)
            print(self.service, ': Success -- Message deleted')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Message deletion failed; error: ', e)
            return False
        


    # delete queue with arguments as none try except
    def queue_delete(self, *args):
        args = list(args)
        
        try:
            self.queue_client.delete_queue()
            print(self.service, ': Success -- Queue deleted')
            # create queue again
            self.queue_create()
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue deletion failed; error: ', e)
            return False
        


    # get queue access policy with arguments as none try except
    def queue_get_access_policy(self, *args):
        args = list(args)
        
        try:
            self.queue_client.get_queue_access_policy()
            print(self.service, ': Success -- Queue access policy retrieved')
            return True
        except Exception as e:
            print(self.service, ': FAILED : Queue access policy retrieval failed; error: ', e)
            return False
        

    # get queue properties with arguments as none try except
    def queue_get_properties(self, *args):
        args = list(args)
            
        try:
            self.queue_client.get_queue_properties()
            print(self.service, ': Success -- Queue properties retrieved')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue properties retrieval failed; error: ', e)
            return False
        
    # peek messages with arguments as none try except
    def queue_peek_messages(self, *args):
        args = list(args)

        if not len(args) > 0:
            args.append(5)
        
        try:
            self.queue_client.peek_messages(args[0])
            print(self.service, ': Success -- Queue messages peeked')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue messages peek failed; error: ', e)
            return False
        
    # receive message with arguments as none try except
    def queue_receive_message(self, *args):
            
        try:
            self.queue_client.receive_message()
            print(self.service, ': Success -- Queue messages received')
            return True
        except Exception as e:
            print(self.service, ': Queue messages receive failed; error: ', e)
            return False
        

    # receive messages with arguments as none try except
    def queue_receive_messages(self, *args):
        args = list(args)

        if not len(args) > 0:
            args.append(5)
                
        try:
            self.queue_client.receive_messages(max_messages=args[0])
            print(self.service, ': Success -- Queue messages received')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue messages receive failed; error: ', e)
            return False
    

    # send message with arguments as none try except
    def queue_send_message(self, *args):
        args = list(args)

        if not len(args) > 0:
            args.append('Hello World')
                        
        try:
            self.queue_client.send_message(args[0])
            print(self.service, ': Success -- Message sent')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Message send failed; error: ', e)
            return False
        

    # set queue access policy with arguments as none try except
    def queue_set_access_policy(self, *args):
        args = list(args)
               
        try:
            # get access policy
            resp = self.queue_client.get_queue_access_policy()
            print(self.service, ': Success -- Queue access policy retrieved')
            # set access policy
            self.queue_client.set_queue_access_policy(resp)
            print(self.service, ': Success -- Queue access policy set')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue access policy set failed; error: ', e)
            return False


    # set queue metadata with arguments as none try except
    def queue_set_metadata(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append({'key':'value'})
        try:
            self.queue_client.set_queue_metadata(args[0])
            print(self.service, ': Success -- Queue metadata set')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue metadata set failed; error: ', e)
            return False
        

    # update message with arguments as none try except
    def queue_update_message(self, *args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('Hello World')
        if not len(args) > 1:
            args.append('updated message content')
        try:
            # send message
            resp = self.queue_client.send_message(args[0])
            print(self.service, ': Success -- Message sent')
            # msg id and pop receipt
            message_id = resp['id']
            pop_receipt = resp['pop_receipt']
            self.queue_client.update_message(message_id, pop_receipt, args[1])
            print(self.service, ': Success -- Message updated')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Message update failed; error: ', e)
            return False
        
    # garbage collection
    def __cleanup__(self):

        try:
            queues = self.queue_service_client.list_queues()
            # list queues 
            for queue in queues:
                try: 
                    # delete queue
                    self.queue_service_client.delete_queue(queue.name)
                    print('Success -- Queue deleted')
                except:
                    print('Failed -- Queue deletion failed')

        except:
            print('Failed -- Queue list failed')

        

