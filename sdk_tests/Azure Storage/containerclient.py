from azure.storage.blob import BlobServiceClient, PublicAccess, AccessPolicy, PremiumPageBlobTier, StandardBlobTier, BlobLeaseClient
from azure.identity import DefaultAzureCredential
import random, os, datetime

# Point to certificates
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()

# all functions are individually tested cloud service

class ContainerClient:
    def __init__(self, emulator=True, container_name=None, blob_name=None):

        # randomize seed
        random.seed(datetime.datetime.now())
        
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
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=https://127.0.0.1:10000/devstoreaccount1;'
            self.service = '**EMULATOR**'
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=LGHPh+f0PHvNw8PVYtEkN0fWsqWO9ZsY3DrQox0veta/Ii+aW3m/E7VLVFna/qDMqm/CCg4lou9N+AStwMBcgA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'

        global credential

        # use blob service client to create a container client
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            self.container_client = self.blob_service_client.get_container_client(self.container_name)
        except Exception as e:
            print('Container creation failed; error: ', e)

        # create container
        try:
            self.container_client.create_container()
        except Exception as e:
            print(self.service + ": Container is not created. Error: ", e)

        # upload blob
        try:
            self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
        except Exception as e:
            print(self.service + ": Blob is not created. Error: ", e)

    # acquire lease with try except block
    def acquire_lease(self, args):
        args = list(args)
        # lease id
        if not len(args) > 0:
            args.append('7c9e6679-7425-40de-944b-e07fc1f90ae7')
        # lease duration
        if not len(args) > 1:
            args.append(15)

        try:
            res = self.container_client.acquire_lease(lease_duration=args[1], lease_id=args[0])
            print(self.service + ": Lease is acquired")

            # break lease for garbage collection
            blob_lease_client = BlobLeaseClient(self.container_client)
            blob_lease_client.break_lease(lease_break_period=0)
            
            return True, res
        except Exception as e:
            print(self.service + ": Lease is not acquired. Error: ", e)
            return False, e
        

      # create a container with random name with try except block
    def create_container(self, args):
        args = list(args)
        # container name
        if not len(args) > 0:
            args.append(f'container{random.randint(1, 1000000000)}')

        try:
            res = self.blob_service_client.get_container_client(args[0]).create_container()
            print(self.service + ": Container is created")
            return True, res
        except Exception as e:
            print(self.service + ": Container is not created. Error: ", e)
            return False, e


    # delete a given blob with try except block
    def delete_blob(self, args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            res = self.container_client.delete_blob(args[0])
            print(self.service + ": Blob is deleted")
            # create blob again
            self.container_client.upload_blob(data=b'Second one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            return True, res
        except Exception as e:
            print(self.service + ": Blob is not deleted. Error: ", e)
            return False, e


    # delete given list of blobs (delete_blobs operation) with try except block
    def delete_blobs(self, args):
        args = list(args)
        # blob list
        if not len(args) > 0:
            args.append({'name':'blob1', 'name':'blob2', 'name':'blob3'})

        try:
            # upload three new blobs in order to perform batch deletion of them
            self.container_client.upload_blob(data=b'First one', name='blob1', blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            self.container_client.upload_blob(data=b'Second one', name='blob2', blob_type='BlockBlob', length=len('Second one'), metadata={'hello': 'world', 'number': '42'})
            self.container_client.upload_blob(data=b'Third one', name='blob3', blob_type='BlockBlob', length=len('Third one'), metadata={'hello': 'world', 'number': '42'})

            # perform delete batch
            res = self.container_client.delete_blobs(args[0])
            print(self.service + ": Blobs are deleted successfully.")

            # # create blob again in order to perform other operations in sequences
            # self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            return True, res
        except Exception as e:
            print(self.service + ": Blobs are not deleted. Error: ", e)
            return False, e


    # delete container with try except block
    def delete_container(self, args):
        args = list(args)
        try:
            res = self.container_client.delete_container()
            print(self.service + ": Container deleted successfully.")
            # create container again
            random_name = f'container{random.randint(1, 1000000000)}'
            self.container_client = self.blob_service_client.get_container_client(random_name)
            self.container_client.create_container()
            return True, res
        except Exception as e:
            print(self.service + ": Container is not deleted. Error: ", e)
            return False, e


    # download a blob (download_blob operation) with try except block
    def download_blob(self, args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            res = self.container_client.download_blob(args[0])
            print(self.service + ": Blob is downloaded")
            return True, res
        except Exception as e:
            print(self.service + ": Blob is not downloaded. Error: ", e)
            return False, e
    

    # check if a container exists
    def exists(self, args):
        args = list(args)
        print(self.service + ": " + 'Checking if container exists: ')
        
        try:
            res = self.container_client.exists()
            print(self.service + ": Container exists:", res)
            return True, res
        except Exception as e:
            print(self.service + ": Container existence check failed. Error: ", e)
            return False, e


    # find blobs by tags with try except block
    def find_blobs_by_tags(self, args):
        args = list(args)
        # tags
        if not len(args) > 0:
            args.append({'tag1': 'value1', 'tag2': 'value2'})
        try:
            res = self.container_client.find_blobs_by_tags(args[0])
            print(self.service + ": Blobs are found.")
            return True, res
        except Exception as e:
            print(self.service + ": Blobs are not found. Error: ", e)
            return False, e


    # get account information with try except block
    def get_account_information(self, args):
        args = list(args)
        try:
            res = self.container_client.get_account_information()
            print(self.service + ": Account information found")
            return True, res
        except Exception as e:
            print(self.service + ": Account information is not found. Error: ", e)
            return False, e


    # get blob client with try except block
    def get_blob_client(self, args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            res = self.container_client.get_blob_client(args[0])
            print(self.service + ": Blob client accessed")
            return True, res
        except Exception as e:
            print(self.service + ": Blob client is not found. Error: ", e)
            return False, e


    # get container access policy with try except block
    def get_container_access_policy(self, args):
        args = list(args)
        try:
            res = self.container_client.get_container_access_policy()
            print(self.service + ": Container access policy accessed")
            return True, res
        except Exception as e:
            print(self.service + ": Container access policy is not found. Error: ", e)
            return False, e


    # get container properties with try except block
    def get_container_properties(self, args):
        args = list(args)
        try:
            res = self.container_client.get_container_properties()
            print(self.service + ": Container properties found")
            return True, res
        except Exception as e:
            print(self.service + ": Container properties are not found. Error: ", e)
            return False, e
        

    # list blob names with try except block
    def list_blob_names(self, args):
        args = list(args)
        try:
            print(self.service + ": Listing blob names...")
            res = self.container_client.list_blob_names()
            print(self.service + ": Blob names listed successfully")
            return True, res
        except Exception as e:
            print(self.service + ": Blob names cannot be listed. Error: ", e)
            return False, e
        


    # list blobs with try except block
    def list_blobs(self, args):
        args = list(args)
        try:
            print(self.service + ": Listing blobs...")
            res = self.container_client.list_blobs()
            print(self.service + ": Blob listed successfully")
            return True, res
        except Exception as e:
            print(self.service + ": Blobs cannot be listed. Error: ", e)
            return False, e
        

    # set container access policy with try except block
    def set_container_access_policy(self, args):
        args = list(args)

        # signed identifiers
        if not len(args) > 0:
            args.append({'id': AccessPolicy()})

        public_access = PublicAccess('blob')

        try:
            res = self.container_client.set_container_access_policy(args[0], public_access)
            print(self.service + ": Container access policy is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Container access policy is not set. Error: ", e)
            return False, e
        

    # set container metadata with try except block
    def set_container_metadata(self, args):
        args = list(args)
        # metadata
        if not len(args) > 0:
            args.append({'hello': 'world', 'number': '42'})
        try:
            res = self.container_client.set_container_metadata(metadata=args[0])
            print(self.service + ": Container metadata is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Container metadata is not set. Error: ", e)
            return False, e

    '''Applied to premium acounts only'''
    # set premium page blob tier with try except block
    def set_premium_page_blob_tier(self, args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(f'blob{random.randint(1, 10000)}')
        # premium page blob tier
        if not len(args) > 1:
            args.append(PremiumPageBlobTier('P4'))
        try:
            # create page blob
            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=args[0], blob_type='PageBlob')

            res = self.container_client.set_premium_page_blob_tier_blobs(premium_page_blob_tier=args[1])
            print(self.service + ": premium page blob tier is set.")
            return True, res
        except Exception as e:
            print(self.service + ": premium page blob tier is not set. Error: ", e)
            return False, e


    # set standard page blob tier with try except block
    def set_standard_page_blob_tier(self, args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        # standard page blob tier
        if not len(args) > 1:
            args.append(StandardBlobTier('Cool'))
        try:
            res = self.container_client.set_standard_blob_tier_blobs(args[1], args[0])
            print(self.service + ": standard page blob tier is set")
            return True, res
        except Exception as e:
            print(self.service + ": standard page blob tier is not set. Error: ", e)
            return False, e
        

    # upload blob
    def upload_blob(self, args):
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
            res = container_client.upload_blob(data=args[1], name=args[0], blob_type=args[2], length=len(args[1]), metadata=args[3])
            print(self.service + ": Blob is uploaded.")
            return True, res
        except Exception as e:
            print(self.service + ": Blob is not uploaded. Error: ", e)
            return False, e
        

     # walk blob
    def walk_blobs(self, args):
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
            res = self.container_client.walk_blobs(name_starts_with=args[0], include=args[1], delimiter=args[2])
            print(self.service + ": Blobs walk successful.")
            return True, res
        except Exception as e:
            print(self.service + ": Blobs cannot be walked. Error: ", e)
            return False, e
        
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