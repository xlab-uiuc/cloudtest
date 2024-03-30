import datetime
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import random, time, json

# Point to certificates
# os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()
config = json.loads(open('config.json').read())

class MyBlobServiceClient:
    def __init__(self, emulator=True, container_name=None, blob_name=None):

        # randomize seed
        random.seed(datetime.datetime.now())
        
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
            
        global config
        self.account_name = config['cloud_account_name']

        # connection string
        if emulator:
            self.connection_string = config['emulator_connection_string']
            self.service = "**EMULATOR**"
        else:
            self.connection_string = config['cloud_connection_string']
            self.service = "**AZURE**"

        # credential
        global credential

        # create container client
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            self.container_client = self.blob_service_client.get_container_client(self.container_name)
        except Exception as e:
            print('Blob service client creation failed; error: ', e)

        try:
            self.container_client.create_container()
        except Exception as e:
            print('Container creation failed; error: ', e)

        # create blob client
        try:
            self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            self.blob_client = self.container_client.get_blob_client(self.blob_name)
        except Exception as e:
            print('Blob client creation failed; error: ', e)


    # create container with default container name as none with try except
    def create_container(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(f'container{random.randint(1, 1000000000)}')

        try:
            res = self.blob_service_client.create_container(args[0])
            print(self.service, ': Success -- Container created with name: ', args[0])
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Container creation failed with name: ', args[0], ' and error: ', e)
            return False, e
        

    # delete container with default container name as none with try except
    def delete_container(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.container_name)

        try:
            res = self.blob_service_client.delete_container(args[0])
            print(self.service, ': Success -- Container deleted with name: ', args[0])

            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Container deletion failed with name: ', args[0], ' and error: ', e)
            return False, e
        

    # find blobs by tags
    def find_blobs_by_tags(self, args):
        args = list(args)
        # tag name
        if not len(args) > 0:
            args.append('hello')
        
        try:
            res = self.blob_service_client.find_blobs_by_tags(args[0])
            print(self.service, ': Success -- Blobs found with filter expression: ', args[0])
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Blob search failed, error: ', e)
            return False, e


    # get account info with try except
    def get_account_info(self, args):
        args = list(args)
        try:
            res = self.blob_service_client.get_account_information()
            print(self.service, ': Success -- Account info retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Account info retrieval failed, error: ', e)
            return False, e
        

    # get blob client with default blob name as none with try except
    def get_blob_client(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.blob_name)

        try:
            res = self.container_client.get_blob_client(args[0])
            print(self.service, ': Success -- Blob client retrieved with name: ', args[0])
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Blob client retrieval failed with name: ', args[0], ' and error: ', e)
            return False, e
        

    # get container client with default container name as none with try except
    def get_container_client(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.container_name)

        try:
            res = self.blob_service_client.get_container_client(args[0])
            print(self.service, ': Success -- Container client retrieved with name: ', args[0])
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Container client retrieval failed with name: ', args[0], ' and error: ', e)
            return False, e
        

    # get service properties with try except
    def get_service_properties(self, args):
        args = list(args)
        try:
            res = self.blob_service_client.get_service_properties()
            print(self.service, ': Success -- Service properties retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Service properties retrieval failed, error: ', e)
            return False, e
        
    # will get "Failed to establish a connection" error if geo replication is disabled in cloud
    # get service stats with try except
    def get_service_stats(self, args):
        args = list(args)
        try:
            res = self.blob_service_client.get_service_stats()
            print(self.service, ': Success -- Service stats retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Service stats retrieval failed, error: ', e)
            return False, e
        

    # list containers with try except
    def list_containers(self, args):
        args = list(args)
        # name_starts_with
        if not len(args) > 0:
            args.append('container')
        # include_metadata
        if not len(args) > 1:
            args.append(True)
        # include_deleted
        if not len(args) > 2:
            args.append(True)
        try:
            res = self.blob_service_client.list_containers(name_starts_with=args[0], include_metadata=args[1], include_deleted=args[2])
            print(self.service, ': Success -- Container list retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Container list retrieval failed, error: ', e)
            return False, e


    # undelete container with default container name as none with try except
    def undelete_container(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.container_name)

        if not len(args) > 1:
            args.append('0x8DB74AF1E107D84')

        try:
            # delete the container first
            if args[0] == self.container_name:
                self.blob_service_client.delete_container(self.container_name)

                # list container to get version id
                containers = self.blob_service_client.list_containers(include_deleted=True)
                for container in containers:
                    if container.name == self.container_name:
                        args[1] = container.version
                        # max time for resource deletion is 30 seconds
                        time.sleep(30)

            res = self.blob_service_client.undelete_container(deleted_container_name=args[0], deleted_container_version=args[1])
            print(self.service, ': Success -- Container undeleted with name: ', args[0])
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Container undeletion failed with name: ', args[0], ' and error: ', e)
            return False, e
    
    # garbage collection
    def __cleanup__(self):
        
        try:
            containers = self.blob_service_client.list_containers()
            # delete all containers
            for container in containers:
                try:
                    self.blob_service_client.delete_container(container.name)
                    print(f"Container is deleted in GC -- {self.service}")
                except Exception as e:
                    print(f"Container is not deleted in GC -- {self.service}. Error: ", e)
        except Exception as e:
            print(f"Containers could not be listed in GC -- {self.service}. Error: ", e)





