from azure.storage.blob import BlobServiceClient, PublicAccess, AccessPolicy, PremiumPageBlobTier, StandardBlobTier, BlobLeaseClient
from azure.identity import DefaultAzureCredential
import random, datetime, json

# Point to certificates
# os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()
config = json.loads(open('config.json').read())

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
        
        global config
        
        # connection string
        if emulator:
            self.connection_string = config['emulator_connection_string']
            self.service = '**EMULATOR**'
        else:
            self.connection_string = config['cloud_connection_string']
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
            print(self.service + ": Fail -- Container is not created. Error: ", e)

        # upload blob
        try:
            self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            print(f"Blob is created {self.blob_name}")
        except Exception as e:
            print(self.service + ": Fail -- Blob is not created. Error: ", e)

        
        # get blob client
        try:
            self.blob_client = self.container_client.get_blob_client(self.blob_name)
        except Exception as e:
            print(self.service + ": Fail -- Blob client is not created. Error: ", e)

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
            print(self.service + ": Success -- Lease is acquired")

            # break lease for garbage collection
            blob_lease_client = BlobLeaseClient(self.container_client)
            blob_lease_client.break_lease(lease_break_period=0)
            
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Lease is not acquired. Error: ", e)
            return False, e
        

      # create a container with random name with try except block
    def create_container(self, args):
        args = list(args)
        # container name
        if not len(args) > 0:
            args.append(f'container{random.randint(1, 1000000000)}')

        try:
            res = self.blob_service_client.get_container_client(args[0]).create_container()
            print(self.service + ": Success -- Container is created")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Container is not created. Error: ", e)
            return False, e


    # delete a given blob with try except block
    def delete_blob(self, args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            res = self.container_client.delete_blob(args[0])
            print(self.service + ": Success -- Blob is deleted")

            return True, res
        except Exception as e:
            print(self.service + f": Fail -- Blob {args[0]} is not deleted. Error: ", e)
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
            print(self.service + ": Success -- Blobs are deleted successfully.")

            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blobs are not deleted. Error: ", e)
            return False, e


    # delete container with try except block
    def delete_container(self, args):
        args = list(args)
        try:
            res = self.container_client.delete_container()
            print(self.service + ": Success -- Container deleted successfully.")

            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Container is not deleted. Error: ", e)
            return False, e


    # download a blob (download_blob operation) with try except block
    def download_blob(self, args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            res = self.container_client.download_blob(args[0])
            print(self.service + ": Success -- Blob is downloaded")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not downloaded. Error: ", e)
            return False, e
    

    # check if a container exists
    def exists(self, args):
        args = list(args)
        print(self.service + ": Success -- " + 'Checking if container exists: ')
        
        try:
            res = self.container_client.exists()
            print(self.service + ": Success -- Container exists:", res)
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Container existence check failed. Error: ", e)
            return False, e


    # find blobs by tags with try except block
    def find_blobs_by_tags(self, args):
        args = list(args)
        # tags
        if not len(args) > 0:
            args.append({'tag1': 'value1', 'tag2': 'value2'})
        try:
            res = self.container_client.find_blobs_by_tags(args[0])
            print(self.service + ": Success -- Blobs are found.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blobs are not found. Error: ", e)
            return False, e


    # skip --> from_connection_string (covered in constructor)

    # get account information with try except block
    def get_account_information(self, args):
        args = list(args)
        try:
            res = self.container_client.get_account_information()
            print(self.service + ": Success -- Account information found")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Account information is not found. Error: ", e)
            return False, e


    # get blob client with try except block
    def get_blob_client(self, args):
        args = list(args)
        # blob name
        if not len(args) > 0:
            args.append(self.blob_name)
        try:
            res = self.container_client.get_blob_client(args[0])
            print(self.service + ": Success -- Blob client accessed")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob client is not found. Error: ", e)
            return False, e


    # get container access policy with try except block
    def get_container_access_policy(self, args):
        args = list(args)
        try:
            res = self.container_client.get_container_access_policy()
            print(self.service + ": Success -- Container access policy accessed")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Container access policy is not found. Error: ", e)
            return False, e


    # get container properties with try except block
    def get_container_properties(self, args):
        args = list(args)
        try:
            res = self.container_client.get_container_properties()
            print(self.service + ": Success -- Container properties found")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Container properties are not found. Error: ", e)
            return False, e
        

    # list blob names with try except block
    def list_blob_names(self, args):
        # starts with
        if not len(args) > 0:
            args.append("blob")

        args = list(args)
        try:
            print(self.service + ": Success -- Listing blob names...")
            res = self.container_client.list_blob_names(name_starts_with=args[0])
            print(self.service + ": Success -- Blob names listed successfully")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob names cannot be listed. Error: ", e)
            return False, e
        


    # list blobs with try except block
    def list_blobs(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append('blob')

        if not len(args) > 1:
            args.append([ 'deleted', 'deletedwithversions'])
        try:
            self.delete_blob([])
            print(self.service + ": Success -- Listing blobs...")
            res = self.container_client.list_blobs(name_starts_with=args[0], include=args[1])
            for i in res: 
                print(i)
            print(self.service + ": Success -- Blob listed successfully")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blobs cannot be listed. Error: ", e)
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
            print(self.service + ": Success -- Container access policy is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Container access policy is not set. Error: ", e)
            return False, e
        

    # set container metadata with try except block
    def set_container_metadata(self, args):
        args = list(args)
        # metadata
        if not len(args) > 0:
            args.append({'hello': 'world', 'number': '42'})
        try:
            res = self.container_client.set_container_metadata(metadata=args[0])
            print(self.service + ": Success -- Container metadata is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Container metadata is not set. Error: ", e)
            return False, e

    '''Applied to premium acounts only'''
    # set premium page blob tier with try except block (batch operation)
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
            print(self.service + ": Success -- premium page blob tier is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- premium page blob tier is not set. Error: ", e)
            return False, e


    # set standard page blob tier with try except block (batch operation)
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
            print(self.service + ": Success -- standard page blob tier is set")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- standard page blob tier is not set. Error: ", e)
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
            print(self.service + ": Success -- Uploading blob: ", args[0])
            res = container_client.upload_blob(data=args[1], name=args[0], blob_type=args[2], length=len(args[1]), metadata=args[3])
            print(self.service + ": Success -- Blob is uploaded.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not uploaded. Error: ", e)
            return False, e
        

     # walk blob
    def walk_blobs(self, args):
        args = list(args)
        # name starts with
        if not len(args) > 0:
            args.append('blob')
        # include
        if not len(args) > 1:
            args.append(['snapshots', 'metadata', 'uncommittedblobs', 'copy', 'deleted', 'deletedwithversions', 'tags', 'versions', 'immutabilitypolicy', 'legalhold'])
        # delimiter
        if not len(args) > 2:
            args.append('/')
        try:
            res = self.container_client.walk_blobs(name_starts_with=args[0], include=args[1], delimiter=args[2])
            print(self.service + ": Success -- Blobs walk successful.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blobs cannot be walked. Error: ", e)
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


    