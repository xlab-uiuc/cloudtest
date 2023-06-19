from azure.storage.blob import BlobServiceClient, PublicAccess, AccessPolicy, PremiumPageBlobTier, StandardBlobTier
import random

# all functions are individually tested cloud service

class ContainerClient:
    def __init__(self, emulator=True, container_name=None, blob_name=None):
        
        # container name
        if container_name is None:
            self.container_name = f'container{random.randint(1, 1000000000)}'
        else :
            self.container_name = container_name
        # blob name
        if blob_name is None:
            self.blob_name = f'blob{random.randint(1, 1000000000)}'
        else:
            self.blob_name = blob_name

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
            self.service = '**EMULATOR**'
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=Kt8fMYDEpeaq/A6TRBU+1+LRMIqd2h9Nv7Hd/qCn4B9DqvbNDXPJWU4BRqu50GVEjFfcocumL1lr+AStfVsaPA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'

        # use blob service client to create a container client
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            self.container_client = self.blob_service_client.get_container_client(self.container_name)
        except Exception as e:
            print('Container creation failed; error: ', e)

        try:
            self.container_client.create_container()
        except:
            pass

        try:
            self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
        except:
            pass

    # acquire lease with try except block
    def acquire_lease(self, *args):
        args = list(args)
        # lease id
        if not len(args) > 0:
            args.append('ashg-jaha-jhds0a-23sds-23423')
        # lease duration
        if not len(args) > 1:
            args.append(10)

        try:
            self.container_client.acquire_lease(lease_duration=args[1], lease_id=args[0])
            print(self.service + ": Lease is acquired")
            return True
        except Exception as e:
            print(self.service + ": Lease is not acquired. Error: ", e)
            return False
        

      # create a container with random name with try except block
    def create_container(self, *args):
        args = list(args)
        # container name
        if not len(args) > 0:
            args.append(f'container{random.randint(1, 1000000000)}')

        try:
            self.blob_service_client.get_container_client(args[0]).create_container()
            print(self.service + ": Container is created")
            return True
        except Exception as e:
            print(self.service + ": Container is not created. Error: ", e)
            return False


    # delete a given blob with try except block
    def delete_blob(self, *args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            self.container_client.delete_blob(args[0])
            print(self.service + ": Blob is deleted")
            # create blob again
            self.container_client.upload_blob(data=b'Second one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            return True
        except Exception as e:
            print(self.service + ": Blob is not deleted. Error: ", e)
            return False


    # delete given list of blobs (delete_blobs operation) with try except block
    def delete_blobs(self, *args):
        args = list(args)
        # blob list
        if not len(args) > 0:
            args.append({'name':'blob1', 'name':'blob2', 'name':'blob3'})

        try:
            self.container_client.delete_blobs(args[0])
            print(self.service + ": Blobs are deleted successfully.")
            # create blob again
            self.container_client.upload_blob(data=b'Third one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            return True
        except Exception as e:
            print(self.service + ": Blobs are not deleted. Error: ", e)
            return False


    # delete container with try except block
    def delete_container(self, *args):
        args = list(args)
        try:
            self.container_client.delete_container()
            print(self.service + ": Container deleted successfully.")
            # create container again
            self.container_client.create_container()
            return True
        except Exception as e:
            print(self.service + ": Container is not deleted. Error: ", e)
            return False


    # download a blob (download_blob operation) with try except block
    def download_blob(self, *args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            self.container_client.download_blob(args[0])
            print(self.service + ": Blob is downloaded")
            return True
        except Exception as e:
            print(self.service + ": Blob is not downloaded. Error: ", e)
            return False
    

    # check if a container exists
    def exists(self, *args):
        args = list(args)
        print(self.service + ": " + 'Checking if container exists: ')
        
        try:
            resp = self.container_client.exists()
            print(self.service + ": Container exists:", resp)
            return True
        except Exception as e:
            print(self.service + ": Container existence check failed. Error: ", e)
            return False


    # find blobs by tags with try except block
    def find_blobs_by_tags(self, *args):
        args = list(args)
        # tags
        if not len(args) > 0:
            args.append({'tag1': 'value1', 'tag2': 'value2'})
        try:
            self.container_client.find_blobs_by_tags(args[0])
            print(self.service + ": Blobs are found.")
            return True
        except Exception as e:
            print(self.service + ": Blobs are not found. Error: ", e)
            return False


    # get account information with try except block
    def get_account_information(self, *args):
        args = list(args)
        try:
            self.container_client.get_account_information()
            print(self.service + ": Account information found")
            return True
        except Exception as e:
            print(self.service + ": Account information is not found. Error: ", e)
            return False


    # get blob client with try except block
    def get_blob_client(self, *args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            self.container_client.get_blob_client(args[0])
            print(self.service + ": Blob client accessed")
            return True
        except Exception as e:
            print(self.service + ": Blob client is not found. Error: ", e)
            return False


    # get container access policy with try except block
    def get_container_access_policy(self, *args):
        args = list(args)
        try:
            self.container_client.get_container_access_policy()
            print(self.service + ": Container access policy accessed")
            return True
        except Exception as e:
            print(self.service + ": Container access policy is not found. Error: ", e)
            return False


    # get container properties with try except block
    def get_container_properties(self, *args):
        args = list(args)
        try:
            self.container_client.get_container_properties()
            print(self.service + ": Container properties found")
            return True
        except Exception as e:
            print(self.service + ": Container properties are not found. Error: ", e)
            return False
        

    # list blob names with try except block
    def list_blob_names(self, *args):
        args = list(args)
        try:
            print(self.service + ": Listing blob names...")
            self.container_client.list_blob_names()
            print(self.service + ": Blob names listed successfully")
            return True
        except Exception as e:
            print(self.service + ": Blob names cannot be listed. Error: ", e)
            return False
        


    # list blobs with try except block
    def list_blobs(self, *args):
        args = list(args)
        try:
            print(self.service + ": Listing blobs...")
            res = self.container_client.list_blobs()
            print(self.service + ": Blob listed successfully")
            return True
        except Exception as e:
            print(self.service + ": Blobs cannot be listed. Error: ", e)
            return False
        

    # set container access policy with try except block
    def set_container_access_policy(self, *args):
        args = list(args)

        # signed identifiers
        if not len(args) > 0:
            args.append({'id': AccessPolicy()})

        public_access = PublicAccess('blob')

        try:
            self.container_client.set_container_access_policy(args[0], public_access)
            print(self.service + ": Container access policy is set.")
            return True
        except Exception as e:
            print(self.service + ": Container access policy is not set. Error: ", e)
            return False
        

    # set container metadata with try except block
    def set_container_metadata(self, *args):
        args = list(args)
        # metadata
        if not len(args) > 0:
            args.append({'hello': 'world', 'number': '42'})
        try:
            self.container_client.set_container_metadata(metadata=args[0])
            print(self.service + ": Container metadata is set.")
            return True
        except Exception as e:
            print(self.service + ": Container metadata is not set. Error: ", e)
            return False

    '''Applied to premium acounts only'''
    # set premium page blob tier with try except block
    def set_premium_page_blob_tier(self, *args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        # premium page blob tier
        if not len(args) > 1:
            args.append(PremiumPageBlobTier('P4'))
        try:
            self.container_client.set_premium_page_blob_tier_blobs(args[1], args[0])
            print(self.service + ": premium page blob tier is set.")
            return True
        except Exception as e:
            print(self.service + ": premium page blob tier is not set. Error: ", e)
            return False


    # set standard page blob tier with try except block
    def set_standard_page_blob_tier(self, *args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        # standard page blob tier
        if not len(args) > 1:
            args.append(StandardBlobTier('Cool'))
        try:
            self.container_client.set_standard_blob_tier_blobs(args[1], args[0])
            print(self.service + ": standard page blob tier is set")
            return True
        except Exception as e:
            print(self.service + ": standard page blob tier is not set. Error: ", e)
            return False
        

    # upload blob
    def upload_blob(self, *args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(f'blob{random.randint(1, 1000000000)}')
        # blob data
        if not len(args) > 1:
            args.append(b'hello world')
        # blob type
        if not len(args) > 2:
            args.append('BlockBlob')
        # blob metadata
        if not len(args) > 3:
            args.append({'hello': 'world', 'number': '42'})

        container_client = self.container_client

        try:
            print(self.service + ": Uploading blob: ", args[0])
            container_client.upload_blob(data=args[1], name=args[0], blob_type=args[2], length=len(args[1]), metadata=args[3])
            print(self.service + ": Blob is uploaded.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not uploaded. Error: ", e)
            return False
        

     # walk blob
    def walk_blobs(self, *args):
        args = list(args)
        # name starts with
        if not len(args) > 0:
            args.append('blob')
        # include
        if not len(args) > 1:
            args.append(['metadata'])
        # delimiter
        if not len(args) > 2:
            args.append('/')
        try:
            self.container_client.walk_blobs(name_starts_with=args[0], include=args[1], delimiter=args[2])
            print(self.service + ": Blobs walk successful.")
            return True
        except Exception as e:
            print(self.service + ": Blobs cannot be walked. Error: ", e)
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


    

# # delete all containers and blobs (Uncomment this after long testing)
# cc = ContainerClient(False)
# containers = cc.blob_service_client.list_containers()

# for container in containers:
#     concli = cc.blob_service_client.get_container_client(container.name)
#     print("Container: ", container.name)
# #     # list blobs
# #     # blobs = concli.list_blobs()
# #     # for blob in blobs:
# #     #     blobcli = concli.get_blob_client(blob)
# #     #     # delete blob
# #     #     try:
# #     #         blobcli.delete_blob()
# #     #     except Exception as e:
# #     #         print("Blob cannot be deleted.")

# #     # delete container
#     try:
#         concli.delete_container()
#         print("Container deleted successfully: ", container)
#     except Exception as e:
#         print("Container cannot be deleted.")