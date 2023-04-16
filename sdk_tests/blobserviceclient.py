import datetime
from azure.storage.blob import BlobServiceClient, ContentSettings, ImmutabilityPolicy
import random


class MyBlobServiceClient:
    def __init__(self, emulator=True, container_name=None, blob_name=None):
        
        # container name
        if container_name is None:
            self.container_name = f'container{random.randint(1, 1000000000)}'
        else:
            self.container_name = container_name
        # blob name
        if blob_name is None:
            self.blob_name = f'blob{random.randint(1, 1000000000)}'
        else:
            self.blob_name = blob_name
            
        self.account_name = 'restlertest1'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=restlertest1;AccountKey=En0z7F3kBwgMv8YIlU57bifLmr2Nb71m4sNVndRvtFiOlpWRNhnlOOPsJG5C7uwZgP92rkFFj4rx+AStw5Q7sA==;EndpointSuffix=core.windows.net'
            self.service = "**AZURE**"


        # create container client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        self.container_client.create_container()

        # create blob client
        self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
        self.blob_client = self.container_client.get_blob_client(self.blob_name)


    # create container with default container name as none with try except
    def create_container(self, container_name=None):
        if container_name is None:
            container_name = f'container{random.randint(1, 1000000000)}'

        try:
            self.container_client = self.blob_service_client.create_container(container_name)
            print(self.service, ': Container created with name: ', container_name)
            return True
        except Exception as e:
            print(self.service, ': Container creation failed with name: ', container_name, ' and error: ', e)
            return False
        

    # delete container with default container name as none with try except
    def delete_container(self, container_name=None):
        if container_name is None:
            container_name = self.container_name

        try:
            self.blob_service_client.delete_container(container_name)
            print(self.service, ': Container deleted with name: ', container_name)
            return True
        except Exception as e:
            print(self.service, ': Container deletion failed with name: ', container_name, ' and error: ', e)
            return False
        

    # find blobs by tags
    def find_blobs_by_tags(self, filter_expression=None):
        # tag name
        if filter_expression is None:
            filter_expression = 'test'
        
        try:
            blobs = self.blob_service_client.find_blobs_by_tags(filter_expression)
            print(self.service, ': Blobs found with filter expression: ', filter_expression)
            return True
        except Exception as e:
            print(self.service, ': Blob search failed, error: ', e)
            return False


    # get account info with try except
    def get_account_info(self):
        try:
            self.blob_service_client.get_account_information()
            print(self.service, ': Account info retrieved')
            return True
        except Exception as e:
            print(self.service, ': Account info retrieval failed, error: ', e)
            return False
        

    # get blob client with default blob name as none with try except
    def get_blob_client(self, blob_name=None):
        if blob_name is None:
            blob_name = self.blob_name

        try:
            self.blob_client = self.container_client.get_blob_client(blob_name)
            print(self.service, ': Blob client retrieved with name: ', blob_name)
            return True
        except Exception as e:
            print(self.service, ': Blob client retrieval failed with name: ', blob_name, ' and error: ', e)
            return False
        

    # get container client with default container name as none with try except
    def get_container_client(self, container_name=None):
        if container_name is None:
            container_name = self.container_name

        try:
            self.container_client = self.blob_service_client.get_container_client(container_name)
            print(self.service, ': Container client retrieved with name: ', container_name)
            return True
        except Exception as e:
            print(self.service, ': Container client retrieval failed with name: ', container_name, ' and error: ', e)
            return False
        

    # get service properties with try except
    def get_service_properties(self):
        try:
            self.blob_service_client.get_service_properties()
            print(self.service, ': Service properties retrieved')
            return True
        except Exception as e:
            print(self.service, ': Service properties retrieval failed, error: ', e)
            return False
        

    # get service stats with try except
    # def get_service_stats(self):
    #     try:
    #         self.blob_service_client.get_service_stats()
    #         print(self.service, ': Service stats retrieved')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Service stats retrieval failed, error: ', e)
    #         return False
        

    # list containers with try except
    def list_containers(self):
        try:
            self.blob_service_client.list_containers()
            print(self.service, ': Container list retrieved')
            return True
        except Exception as e:
            print(self.service, ': Container list retrieval failed, error: ', e)
            return False
        

    # skip seet service property
    # skip get user delegation key


    # undelete container with default container name as none with try except
    def undelete_container(self, container_name=None, version_id=None):
        if container_name is None:
            container_name = self.container_name

        if version_id is None:
            version_id = ""

        try:
            self.blob_service_client.undelete_container(container_name, version_id)
            print(self.service, ': Container undeleted with name: ', container_name)
            return True
        except Exception as e:
            print(self.service, ': Container undeletion failed with name: ', container_name, ' and error: ', e)
            return False
    


# if __name__ == '__main__':


#     # create blob client
#     blob_service_client = MyBlobServiceClient(False)
#     # get all methods
#     methods = [getattr(MyBlobServiceClient, attr) for attr in dir(MyBlobServiceClient) if callable(getattr(MyBlobServiceClient, attr)) and not attr.startswith("__")]

#     for i in methods:
#         print(i.__name__)
#         i(blob_service_client)


