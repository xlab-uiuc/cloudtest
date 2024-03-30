import datetime
from azure.storage.queue import QueueClient, QueueServiceClient, AccessPolicy
from azure.identity import DefaultAzureCredential
import random, json

# Point to certificates
# os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()
config = json.loads(open('config.json').read())

class MyQueueClient:
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
            self.queue_service_client = QueueServiceClient.from_connection_string(self.connection_string)
        except Exception as e:
            print('Queue service client creation failed; error: ', e)

        try:
            self.queue_service_client.create_queue(self.queue_name)
        except Exception as e:
            print('Queue creation failed; error: ', e)

        try:
            self.queue_client = self.queue_service_client.get_queue_client(self.queue_name)
        except Exception as e:
            print('Queue client creation failed; error: ', e)



    # clear messages with params none try except
    def queue_clear_messages(self, args):
        args = list(args)
        try:
            res = self.queue_client.clear_messages()
            print(self.service, ': Success -- Queue cleared')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue clear failed; error: ', e)
            return False, e


    # create queue if not exists with try except
    def queue_create(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(f'queue{random.randint(1, 1000000000)}')
        
        try:
            self.queue_client = self.queue_client.from_connection_string(self.connection_string, args[0])
            res = self.queue_client.create_queue()
            print(self.service, ': Success -- Queue created')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue creation failed; error: ', e)
            return False, e


    # delete message with arguments as none try except
    def queue_delete_message(self, args):
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
            res = self.queue_client.delete_message(message_id, pop_receipt)
            print(self.service, ': Success -- Message deleted')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Message deletion failed; error: ', e)
            return False, e
        


    # delete queue with arguments as none try except
    def queue_delete(self, args):
        args = list(args)
        
        try:
            res = self.queue_client.delete_queue()
            print(self.service, ': Success -- Queue deleted')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue deletion failed; error: ', e)
            return False, e
        


    # get queue access policy with arguments as none try except
    def queue_get_access_policy(self, args):
        args = list(args)
        
        try:
            res = self.queue_client.get_queue_access_policy()
            print(self.service, ': Success -- Queue access policy retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': FAIL : Queue access policy retrieval failed; error: ', e)
            return False, e
        

    # get queue properties with arguments as none try except
    def queue_get_properties(self, args):
        args = list(args)
            
        try:
            res = self.queue_client.get_queue_properties()
            print(self.service, ': Success -- Queue properties retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue properties retrieval failed; error: ', e)
            return False, e
        
    # peek messages with arguments as none try except
    def queue_peek_messages(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(5)
        
        try:
            res = self.queue_client.peek_messages(args[0])
            print(self.service, ': Success -- Queue messages peeked')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue messages peek failed; error: ', e)
            return False, e
        
    # receive message with arguments as none try except
    def queue_receive_message(self, args):
            
        try:
            res = self.queue_client.receive_message()
            print(self.service, ': Success -- Queue messages received')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue messages receive failed; error: ', e)
            return False, e
        

    # receive messages with arguments as none try except
    def queue_receive_messages(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(5)
                
        try:
            res = self.queue_client.receive_messages(max_messages=args[0])
            print(self.service, ': Success -- Queue messages received')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue messages receive failed; error: ', e)
            return False, e
    

    # send message with arguments as none try except
    def queue_send_message(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append('Hello World')
                        
        try:
            res = self.queue_client.send_message(args[0])
            print(self.service, ': Success -- Message sent')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Message send failed; error: ', e)
            return False, e
        

    # set queue access policy with arguments as none try except
    def queue_set_access_policy(self, args):
        args = list(args)
               
        try:
            # get access policy
            resp = self.queue_client.get_queue_access_policy()
            print(self.service, ': Success -- Queue access policy retrieved')
            # set access policy
            res = self.queue_client.set_queue_access_policy(resp)
            print(self.service, ': Success -- Queue access policy set')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue access policy set failed; error: ', e)
            return False, e


    # set queue metadata with arguments as none try except
    def queue_set_metadata(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append({'key':'value'})
        try:
            res = self.queue_client.set_queue_metadata(args[0])
            print(self.service, ': Success -- Queue metadata set')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Queue metadata set failed; error: ', e)
            return False, e
        

    # update message with arguments as none try except
    def queue_update_message(self, args):
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
            res = self.queue_client.update_message(message_id, pop_receipt, args[1])
            print(self.service, ': Success -- Message updated')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Message update failed; error: ', e)
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

        

