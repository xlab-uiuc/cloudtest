import datetime
from azure.storage.queue import QueueClient, QueueServiceClient, AccessPolicy
import random

class MyQueueClient:
    def __init__(self, emulator=True, queue_name=None):
        # queue name
        if queue_name is None:
            self.queue_name = f'queue{random.randint(1, 1000000000)}'
        else:
            self.queue_name = queue_name

        self.account_name = 'restlertest1'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=restlertest1;AccountKey=En0z7F3kBwgMv8YIlU57bifLmr2Nb71m4sNVndRvtFiOlpWRNhnlOOPsJG5C7uwZgP92rkFFj4rx+AStw5Q7sA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'

        # create a queue
        self.queue_service_client = QueueServiceClient.from_connection_string(self.connection_string)
        self.queue_service_client.create_queue(self.queue_name)
        self.queue_client = self.queue_service_client.get_queue_client(self.queue_name)



    # clear messages with params none try except
    def queue_clear_messages(self):
        try:
            self.queue_client.clear_messages()
            print(self.service, ': Success -- Queue cleared')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue clear failed; error: ', e)
            return False


    # create queue if not exists with try except
    def queue_create(self, queue_name=None):
        if queue_name is None:
            queue_name = f'queue{random.randint(1, 1000000000)}'
        
        try:
            self.queue_client = self.queue_client.from_connection_string(self.connection_string, queue_name)
            self.queue_client.create_queue()
            print(self.service, ': Success -- Queue created')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue creation failed; error: ', e)
            return False


    # delete message with arguments as none try except
    def queue_delete_message(self, message_id=None, pop_receipt=None):
        if message_id is None:
            message_id = 'message_id'
        if pop_receipt is None:
            pop_receipt = 'pop_receipt'
        try:
            # send message
            resp = self.queue_client.send_message('Hello World')
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
    def queue_delete(self):
        
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
    def queue_get_access_policy(self):
        
        try:
            self.queue_client.get_queue_access_policy()
            print(self.service, ': Success -- Queue access policy retrieved')
            return True
        except Exception as e:
            print(self.service, ': FAILED : Queue access policy retrieval failed; error: ', e)
            return False
        

    # get queue properties with arguments as none try except
    def queue_get_properties(self):
            
        try:
            self.queue_client.get_queue_properties()
            print(self.service, ': Success -- Queue properties retrieved')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue properties retrieval failed; error: ', e)
            return False
        
    # peek messages with arguments as none try except
    def queue_peek_messages(self, number_of_messages=5):
        
        try:
            self.queue_client.peek_messages(number_of_messages)
            print(self.service, ': Success -- Queue messages peeked')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue messages peek failed; error: ', e)
            return False
        
    # receive message with arguments as none try except
    def queue_receive_message(self):
            
        try:
            self.queue_client.receive_message()
            print(self.service, ': Success -- Queue messages received')
            return True
        except Exception as e:
            print(self.service, ': Queue messages receive failed; error: ', e)
            return False
        

    # receive messages with arguments as none try except
    def queue_receive_messages(self, number_of_messages=None):

        if number_of_messages is None:
            number_of_messages = 5
                
        try:
            kwargs = {'max_messages':number_of_messages}
            self.queue_client.receive_messages(**kwargs)
            print(self.service, ': Success -- Queue messages received')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue messages receive failed; error: ', e)
            return False
    

    # send message with arguments as none try except
    def queue_send_message(self, content='Hello World'):
                        
        try:
            self.queue_client.send_message(content)
            print(self.service, ': Success -- Message sent')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Message send failed; error: ', e)
            return False
        

    # set queue access policy with arguments as none try except
    def queue_set_access_policy(self, signed_identifiers=None):
               
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
    def queue_set_metadata(self, metadata=None):
        if metadata is None:
            metadata = {'val': 'test'}
        try:
            self.queue_client.set_queue_metadata(metadata)
            print(self.service, ': Success -- Queue metadata set')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Queue metadata set failed; error: ', e)
            return False
        

    # update message with arguments as none try except
    def queue_update_message(self, message_id=None, pop_receipt=None, content=None):
        if message_id is None:
            message_id = 'message_id'
        if pop_receipt is None:
            pop_receipt = 'pop_receipt'
        if content is None:
            content = 'New Hello World'
        try:
            # send message
            resp = self.queue_client.send_message('Hello World')
            print(self.service, ': Success -- Message sent')
            # msg id and pop receipt
            message_id = resp['id']
            pop_receipt = resp['pop_receipt']
            self.queue_client.update_message(message_id, pop_receipt, content)
            print(self.service, ': Success -- Message updated')
            return True
        except Exception as e:
            print(self.service, ': Failed -- Message update failed; error: ', e)
            return False
        

# if __name__ == '__main__':


#     # create blob client
#     table_client = MyQueueClient(True)
#     # get all methods
#     methods = [getattr(MyQueueClient, attr) for attr in dir(MyQueueClient) if callable(getattr(MyQueueClient, attr)) and not attr.startswith("__")]
#     print(len(methods))
#     for i in methods:
#         print(i.__name__)
#         i(table_client)