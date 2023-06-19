from azure.storage.blob import BlobServiceClient
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
            
        self.account_name = 'sdkfuzz'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=Kt8fMYDEpeaq/A6TRBU+1+LRMIqd2h9Nv7Hd/qCn4B9DqvbNDXPJWU4BRqu50GVEjFfcocumL1lr+AStfVsaPA==;EndpointSuffix=core.windows.net'
            self.service = "**AZURE**"


        # create container client
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            self.container_client = self.blob_service_client.get_container_client(self.container_name)
        except Exception as e:
            print('Blob service client creation failed; error: ', e)

        try:
            self.container_client.create_container()
        except:
            pass

        # create blob client
        try:
            self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            self.blob_client = self.container_client.get_blob_client(self.blob_name)
        except Exception as e:
            print('Blob client creation failed; error: ', e)


    # create container with default container name as none with try except
    def create_container(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append(f'container{random.randint(1, 1000000000)}')

        try:
            self.container_client = self.blob_service_client.create_container(args[0])
            print(self.service, ': Container created with name: ', args[0])
            return True
        except Exception as e:
            print(self.service, ': Container creation failed with name: ', args[0], ' and error: ', e)
            return False
        

    # delete container with default container name as none with try except
    def delete_container(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.container_name)

        try:
            self.blob_service_client.delete_container(args[0])
            print(self.service, ': Container deleted with name: ', args[0])
            # create container again
            self.container_client.create_container()
            return True
        except Exception as e:
            print(self.service, ': Container deletion failed with name: ', args[0], ' and error: ', e)
            return False
        

    # find blobs by tags
    def find_blobs_by_tags(self, *args):
        args = list(args)
        # tag name
        if not len(args) > 0:
            args.append('hello')
        
        try:
            blobs = self.blob_service_client.find_blobs_by_tags(args[0])
            print(self.service, ': Blobs found with filter expression: ', args[0])
            return True
        except Exception as e:
            print(self.service, ': Blob search failed, error: ', e)
            return False


    # get account info with try except
    def get_account_info(self, *args):
        args = list(args)
        try:
            self.blob_service_client.get_account_information()
            print(self.service, ': Account info retrieved')
            return True
        except Exception as e:
            print(self.service, ': Account info retrieval failed, error: ', e)
            return False
        

    # get blob client with default blob name as none with try except
    def get_blob_client(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.blob_name)

        try:
            self.blob_client = self.container_client.get_blob_client(args[0])
            print(self.service, ': Blob client retrieved with name: ', args[0])
            return True
        except Exception as e:
            print(self.service, ': Blob client retrieval failed with name: ', args[0], ' and error: ', e)
            return False
        

    # get container client with default container name as none with try except
    def get_container_client(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.container_name)

        try:
            self.container_client = self.blob_service_client.get_container_client(args[0])
            print(self.service, ': Container client retrieved with name: ', args[0])
            return True
        except Exception as e:
            print(self.service, ': Container client retrieval failed with name: ', args[0], ' and error: ', e)
            return False
        

    # get service properties with try except
    def get_service_properties(self, *args):
        args = list(args)
        try:
            self.blob_service_client.get_service_properties()
            print(self.service, ': Service properties retrieved')
            return True
        except Exception as e:
            print(self.service, ': Service properties retrieval failed, error: ', e)
            return False
        

    # get service stats with try except
    def get_service_stats(self, *args):
        args = list(args)
        try:
            self.blob_service_client.get_service_stats()
            print(self.service, ': Service stats retrieved')
            return True
        except Exception as e:
            print(self.service, ': Service stats retrieval failed, error: ', e)
            return False
        

    # list containers with try except
    def list_containers(self, *args):
        args = list(args)
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
    def undelete_container(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.container_name)

        if not len(args) > 1:
            args.append('')

        try:
            self.blob_service_client.undelete_container(args[0], args[1])
            print(self.service, ': Container undeleted with name: ', args[0])
            return True
        except Exception as e:
            print(self.service, ': Container undeletion failed with name: ', args[0], ' and error: ', e)
            return False
    
    # garbage collection
    def __cleanup__(self):
        
        try:
            containers = self.blob_service_client.list_containers()
            # delete all containers
            for container in containers:
                try:
                    self.blob_service_client.delete_container(container.name)
                    print("Container is deleted.")
                except Exception as e:
                    print("Container is not deleted. Error: ", e)
        except Exception as e:
            print("Containers could not be listed. Error: ", e)





