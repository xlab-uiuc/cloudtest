import logging
import time
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
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=restlertest1;AccountKey=En0z7F3kBwgMv8YIlU57bifLmr2Nb71m4sNVndRvtFiOlpWRNhnlOOPsJG5C7uwZgP92rkFFj4rx+AStw5Q7sA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'

        # use blob service client to create a container client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        self.container_client.create_container()

        self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})


    # acquire lease with try except block
    def acquire_lease(self, lease_id=None, lease_duration=None):
        # lease id
        if lease_id is None:
            lease_id = 'ashg-jaha-jhds0a-23sds-23423'
        # lease duration
        if lease_duration is None:
            lease_duration = 10

        try:
            self.container_client.acquire_lease()
            print(self.service + ": Lease is acquired")
            return True
        except Exception as e:
            print(self.service + ": Lease is not acquired. Error: ", e)
            return False
        

      # create a container with random name with try except block
    def create_container(self, container_name=None):
        # container name
        if container_name is None:
            container_name = f'container{random.randint(1, 1000000000)}'

        try:
            self.blob_service_client.get_container_client(container_name).create_container()
            print(self.service + ": Container is created")
            return True
        except Exception as e:
            print(self.service + ": Container is not created. Error: ", e)
            return False


    # delete a given blob with try except block
    def delete_blob(self, blob_name=None):
        # blob name
        if blob_name is None:
            blob_name = self.blob_name
        try:
            self.container_client.delete_blob(blob_name)
            print(self.service + ": Blob is deleted")
            return True
        except Exception as e:
            print(self.service + ": Blob is not deleted. Error: ", e)
            return False


    # delete given list of blobs (delete_blobs operation) with try except block
    def delete_blobs(self, blob_list=None):
        # blob list
        if blob_list is None:
            blob_list = {'name':'blob1', 'name':'blob2', 'name':'blob3'}

        try:
            self.container_client.delete_blobs(blob_list)
            print(self.service + ": Blobs are deleted successfully.")
            return True
        except Exception as e:
            print(self.service + ": Blobs are not deleted. Error: ", e)
            return False


    # delete container with try except block
    def delete_container(self):
        try:
            self.container_client.delete_container()
            print(self.service + ": Container deleted successfully.")
            return True
        except Exception as e:
            print(self.service + ": Container is not deleted. Error: ", e)
            return False


    # download a blob (download_blob operation) with try except block
    def download_blob(self, blob_name=None):
        # blob name
        if blob_name is None:
            blob_name = self.blob_name
        try:
            self.container_client.download_blob(blob_name)
            print(self.service + ": Blob is downloaded")
            return True
        except Exception as e:
            print(self.service + ": Blob is not downloaded. Error: ", e)
            return False
    

    # check if a container exists
    def exists(self):
        print(self.service + ": " + 'Checking if container exists: ')
        
        try:
            resp = self.container_client.exists()
            print(self.service + ": Container exists:", resp)
            return True
        except Exception as e:
            print(self.service + ": Container existence check failed. Error: ", e)
            return False


    # find blobs by tags with try except block
    def find_blobs_by_tags(self, tags=None):
        # tags
        if tags is None:
            tags = {'tag1': 'value1', 'tag2': 'value2'}
        try:
            self.container_client.find_blobs_by_tags(tags)
            print(self.service + ": Blobs are found.")
            return True
        except Exception as e:
            print(self.service + ": Blobs are not found. Error: ", e)
            return False


    # get account information with try except block
    def get_account_information(self):
        try:
            self.container_client.get_account_information()
            print(self.service + ": Account information found")
            return True
        except Exception as e:
            print(self.service + ": Account information is not found. Error: ", e)
            return False


    # get blob client with try except block
    def get_blob_client(self, blob_name=None):
        # blob name
        if blob_name is None:
           blob_name = self.blob_name
        try:
            self.container_client.get_blob_client(blob_name)
            print(self.service + ": Blob client accessed")
            return True
        except Exception as e:
            print(self.service + ": Blob client is not found. Error: ", e)
            return False


    # get container access policy with try except block
    def get_container_access_policy(self):
        try:
            self.container_client.get_container_access_policy()
            print(self.service + ": Container access policy accessed")
            return True
        except Exception as e:
            print(self.service + ": Container access policy is not found. Error: ", e)
            return False


    # get container properties with try except block
    def get_container_properties(self):
        try:
            self.container_client.get_container_properties()
            print(self.service + ": Container properties found")
            return True
        except Exception as e:
            print(self.service + ": Container properties are not found. Error: ", e)
            return False
        

    # list blob names with try except block
    def list_blob_names(self):
        try:
            print(self.service + ": Listing blob names...")
            self.container_client.list_blob_names()
            print(self.service + ": Blob names listed successfully")
            return True
        except Exception as e:
            print(self.service + ": Blob names cannot be listed. Error: ", e)
            return False
        


    # list blobs with try except block
    def list_blobs(self):
        try:
            print(self.service + ": Listing blobs...")
            res = self.container_client.list_blobs()
            print(self.service + ": Blob listed successfully")
            return True
        except Exception as e:
            print(self.service + ": Blobs cannot be listed. Error: ", e)
            return False
        

    # set container access policy with try except block
    def set_container_access_policy(self, signed_identifier=None, public_access=None):

        # signed identifiers
        if signed_identifier is None:
            signed_identifier = {'id': AccessPolicy()}

        # public access
        if public_access is None:
            public_access = PublicAccess('blob')

        try:
            self.container_client.set_container_access_policy(signed_identifier, public_access)
            print(self.service + ": Container access policy is set.")
            return True
        except Exception as e:
            print(self.service + ": Container access policy is not set. Error: ", e)
            return False
        

    # set container metadata with try except block
    def set_container_metadata(self, metadata=None):
        # metadata
        if metadata is None:
            metadata = {'hello': 'world', 'number': '42'}
        try:
            self.container_client.set_container_metadata(metadata=metadata)
            print(self.service + ": Container metadata is set.")
            return True
        except Exception as e:
            print(self.service + ": Container metadata is not set. Error: ", e)
            return False

    '''Applied to premium acounts only'''
    # set premium page blob tier with try except block
    # def set_premium_page_blob_tier(self, blob_name=None, premium_blob_tier=None):
    #     # blob name
    #     if blob_name is None:
    #         blob_name = self.blob_name
    #     # premium page blob tier
    #     if premium_blob_tier is None:
    #         premium_blob_tier = PremiumPageBlobTier('P4')
    #     try:
    #         self.container_client.set_premium_page_blob_tier_blobs(premium_blob_tier, blob_name)
    #         print(self.service + ": premium page blob tier is set.")
    #         return True
    #     except Exception as e:
    #         print(self.service + ": premium page blob tier is not set. Error: ", e)
    #         return False


    # set standard page blob tier with try except block
    def set_standard_page_blob_tier(self, blob_name=None, standard_blob_tier=None):
        # blob name
        if blob_name is None:
            blob_name = self.blob_name
        # standard page blob tier
        if standard_blob_tier is None:
            standard_blob_tier = StandardBlobTier('Cool')
        try:
            self.container_client.set_standard_blob_tier_blobs(standard_blob_tier, blob_name)
            print(self.service + ": standard page blob tier is set")
            return True
        except Exception as e:
            print(self.service + ": standard page blob tier is not set. Error: ", e)
            return False
        

    # upload blob
    def upload_blob(self, container_client=None,blob_name=None, data=None, blob_type=None, metadata=None):
        # blob name
        if blob_name is None:
            blob_name = f'blob{random.randint(1, 1000000000)}'
        # blob data
        if data is None:
            data = b'hello world'
        # blob type
        if blob_type is None:
            blob_type = 'BlockBlob'
        # blob metadata
        if metadata is None:
            metadata = {'hello': 'world', 'number': '42'}

        if container_client is None:
            container_client = self.container_client

        try:
            print(self.service + ": Uploading blob: ", blob_name)
            container_client.upload_blob(data=data, name=blob_name, blob_type=blob_type, length=len(data), metadata=metadata)
            print(self.service + ": Blob is uploaded.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not uploaded. Error: ", e)
            return False
        

     # walk blob
    def walk_blobs(self, name_starts_with=None, include=None, delimiter=None):
        # name starts with
        if name_starts_with is None:
            name_starts_with = 'blob'
        # include
        if include is None:
            include = ['metadata']
        # delimiter
        if delimiter is None:
            delimiter = '/'
        try:
            self.container_client.walk_blobs(name_starts_with=name_starts_with, include=include, delimiter=delimiter)
            print(self.service + ": Blobs walk successful.")
            return True
        except Exception as e:
            print(self.service + ": Blobs cannot be walked. Error: ", e)
            return False

    

# '''Check if a sublist exists in a list'''
# def check_sublist_in_list(given_list, sublist):
#     res = False
#     for idx in range(len(given_list) - len(sublist) + 1):
#         if given_list[idx: idx + len(sublist)] == sublist:
#             res = True
#             break

#     return res
        
