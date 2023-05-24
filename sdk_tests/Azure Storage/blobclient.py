import datetime
from azure.storage.blob import BlobServiceClient, ContentSettings, ImmutabilityPolicy
import random


class BlobClient:
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


    # abort copy with parameters default none and try except block
    def abort_copy(self, copy_id=None):
        # copy id
        if copy_id is None:
            copy_id = 'C56A4180-65AA-42EC-A945-5FD21DEC0538'
        try:
            self.blob_client.abort_copy(copy_id)
            print(self.service + ": Copy is aborted -- successful.")
        except Exception as e:
            print(self.service + ": Copy is not aborted -- unsuccessful. Error: ", e)


    # decreases coverage during testing
    # acquire lease with try except block
    def acquire_lease(self, lease_duration=None, lease_id=None):
        # lease duration
        if lease_duration is None:
            lease_duration = 20
        # lease id
        if lease_id is None:
            lease_id = 'f81d4fae-7dec-11d0-a765-00a0c91e6bf6'

        try:
            self.blob_client.acquire_lease(lease_duration, lease_id)
            print(self.service + ": Lease is acquired.")
            return True
        except Exception as e:
            print(self.service + ": Lease is not acquired. Error: ", e)
            return False

    # Not implemented in the emulator
    # append blob with try except block
    def append_block(self, data=None, length=None, validate_content=None):
        # data
        if data is None:
            data = b'Hello World'
        # length
        if length is None:
            length = 11
        else:
            length = len(data)

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            with open('page', 'rb') as data1:
                self.container_client.upload_blob(data=data1, name=random_blob_name, blob_type='AppendBlob')

            blobclient = self.container_client.get_blob_client(random_blob_name)
            blobclient.append_block(data, length)
            print(self.service + ": Blob is appended.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not appended. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # append block from url with try except block
    def append_block_from_url(self, source_url=None, source_offset=None, source_length=None, copy_blob_name=None):
        # copy blob name
        if copy_blob_name is None:
            copy_blob_name = 'copy_blob_name'
        # source url
        if source_url is None:
            source_url = f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{copy_blob_name}'
        # source offset
        if source_offset is None:
            source_offset = 0
        # source length
        if source_length is None:
            source_length = 1024
        

        try:
            self.blob_client.append_block_from_url(copy_source_url=source_url, source_offset=source_offset, source_length=source_length)
            print(self.service + ": Block is appended.")
            return True
        except Exception as e:
            print(self.service + ": Block is not appended. Error: ", e)
            return False
        

    # clear page with try except block
    def clear_page(self, start_range=None, end_range=None):

        # offset
        if start_range is None:
            start_range = 0
        # length
        if end_range is None:
            end_range = 512

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)
            blobclient.clear_page(start_range, end_range)
            print(self.service + ": Page is cleared.")
            return True
                
            
        except Exception as e:
            print(self.service + ": Page is not cleared. Error: ", e)
            return False
        
    
    # commit block list with try except block
    def commit_block_list(self, block_list=None, content_settings=None, metadata=None):
        # block list
        if block_list is None:
            block_list = ['block_id']
        # content settings
        if content_settings is None:
            content_settings = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')
        # metadata
        if metadata is None:
            metadata = {'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'}


        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            self.container_client.upload_blob(data=b'First one', name=random_blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            blobclient = self.container_client.get_blob_client(random_blob_name)

            blobclient.commit_block_list(block_list, content_settings, metadata)
            print(self.service + ": Block list is committed.")
            return True
        except Exception as e:
            print(self.service + ": Block list is not committed. Error: ", e)
            return False
        

    # create append blob with try except block
    def create_append_blob(self, content_settings=None, metadata=None):
        # content settings
        if content_settings is None:
            content_settings = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')
        # metadata
        if metadata is None:
            metadata = {'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'}

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='AppendBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)

            blobclient.create_append_blob(content_settings, metadata)
            print(self.service + ": Append blob is created.")
            return True
        except Exception as e:
            print(self.service + ": Append blob is not created. Error: ", e)
            return False
    

    # create page blob with try except block
    def create_page_blob(self, size=None, content_settings=None, metadata=None, premium_page_blob_tier=None):
        # size
        if size is None:
            size = 512
        # content settings
        if content_settings is None:
            content_settings = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')
        # metadata
        if metadata is None:
            metadata = {'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'}
        # premium page blob tier
        if premium_page_blob_tier is None:
            premium_page_blob_tier = 'P4'

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)

            blobclient.create_page_blob(size, content_settings, metadata)
            print(self.service + ": Page blob is created.")
            return True
        except Exception as e:
            print(self.service + ": Page blob is not created. Error: ", e)
            return False
    


    # create snapshot with try except block
    def create_snapshot(self, metadata=None):
        # metadata
        if metadata is None:
            metadata = {'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'}

        try:
            self.blob_client.create_snapshot(metadata)
            print(self.service + ": Snapshot is created.")
            return True
        except Exception as e:
            print(self.service + ": Snapshot is not created. Error: ", e)
            return False
        

    # # delete blob with try except block
    def delete_blob(self, delete_snapshots=None):
        # delete snapshots
        if delete_snapshots is None:
            delete_snapshots = 'include'

        try:
            self.blob_client.delete_blob(delete_snapshots)
            print(self.service + ": Blob is deleted.")
            # create same blob again
            self.container_client.upload_blob(data=b'Second one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            self.blob_client = self.container_client.get_blob_client(self.blob_name)
            return True
        except Exception as e:
            print(self.service + ": Blob is not deleted. Error: ", e)
            return False
        
    
    # delete immutability policy with try except block
    def delete_immutability_policy(self):
        try:
            self.blob_client.delete_immutability_policy()
            print(self.service + ": Immutability policy is deleted.")
            return True
        except Exception as e:
            print(self.service + ": Immutability policy is not deleted. Error: ", e)
            return False
        


    # download blob with try except block
    def download_blob(self, offset=None, length=None):
        # offset
        if offset is None:
            offset = 0
        # length
        if length is None:
            length = 1024

        try:
            self.blob_client.download_blob(offset, length)
            print(self.service + ": Blob is downloaded.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not downloaded. Error: ", e)
            return False
        

    # check if blob exists with try except block
    def exists(self, timeout=None):

        try:
            self.blob_client.exists()
            print(self.service + ": Blob exists.")
            return True
        except Exception as e:
            print(self.service + ": Blob does not exist. Error: ", e)
            return False
        

    # get account information with try except block
    def get_account_information(self):
        try:
            self.blob_client.get_account_information()
            print(self.service + ": Account information is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Account information is not retrieved. Error: ", e)
            return False
        

    # get blob properties with try except block
    def get_blob_properties(self):

        try:
            self.blob_client.get_blob_properties()
            print(self.service + ": Blob properties are retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Blob properties are not retrieved. Error: ", e)
            return False
        


    # get blob tags with try except block
    def get_blob_tags(self):

        try:
            self.blob_client.get_blob_tags()
            print(self.service + ": Blob tags are retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Blob tags are not retrieved. Error: ", e)
            return False
        

    # get block list with try except block
    def get_block_list(self, block_list_type=None):
        # block list type
        if block_list_type is None:
            block_list_type = 'committed'

        try:
            self.blob_client.get_block_list(block_list_type)
            print(self.service + ": Block list is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Block list is not retrieved. Error: ", e)
            return False
        
        
    # get page ranges with try except block
    def get_page_ranges(self, start_range=None, end_range=None):


        # start range
        if start_range is None:
            start_range = 0
        # end range
        if end_range is None:
            end_range = 1024

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)
            blobclient.get_page_ranges(offset=start_range, length=end_range)
            print(self.service + ": Page ranges are retrieved.")
            return True
            
        except Exception as e:
            print(self.service + ": Page ranges are not retrieved. Error: ", e)
            return False
            

    # list page ranges diff with try except block
    def list_page_ranges_diff(self, previous_snapshot=None, start_range=None, end_range=None):
        # previous snapshot
        if previous_snapshot is None:
            previous_snapshot = 'snapshot'
        # start range
        if start_range is None:
            start_range = 0
        # end range
        if end_range is None:
            end_range = 1024

        try:
            self.blob_client.list_page_ranges(previous_snapshot=previous_snapshot, offset=start_range, length=end_range)
            print(self.service + ": Page ranges diff is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Page ranges diff is not retrieved. Error: ", e)
            return False
        

    # query blob contents with try except block
    def query_blob(self, query_expression=None):
        # query expression
        if query_expression is None:
            query_expression = 'SELECT _2 from BlobStorage'

        try:
            self.blob_client.query_blob(query_expression)
            print(self.service + ": Blob contents are queried.")
            return True
        except Exception as e:
            print(self.service + ": Blob contents are not queried. Error: ", e)
            return False
        

        

    # set blob metadata with try except block
    def set_blob_metadata(self, metadata=None):
        # metadata
        if metadata is None:
            metadata = {'metadata1': 'value1', 'metadata2': 'value2'}


        try:
            self.blob_client.set_blob_metadata(metadata)
            print(self.service + ": Blob metadata is set.")
            return True
        except Exception as e:
            print(self.service + ": Blob metadata is not set. Error: ", e)
            return False
        


    # set blob tags with try except block
    def set_blob_tags(self, tags=None):
        # tags
        if tags is None:
            tags = {'tag1': 'value1', 'tag2': 'value2'}

        try:
            self.blob_client.set_blob_tags(tags)
            print(self.service + ": Blob tags are set.")
            return True
        except Exception as e:
            print(self.service + ": Blob tags are not set. Error: ", e)
            return False
        

    # set http headers with try except block
    def set_http_headers(self, content_settings=None):
        # content settings
        if content_settings is None:
            content_settings = ContentSettings(content_type='text/plain')

        try:
            self.blob_client.set_http_headers(content_settings)
            print(self.service + ": HTTP headers are set.")
            return True
        except Exception as e:
            print(self.service + ": HTTP headers are not set. Error: ", e)
            return False
        


    # set immutability policy with try except block
    def set_immutability_policy(self, immutability_policy=None):
        # immutability policy
        if immutability_policy is None:
            immutability_policy = ImmutabilityPolicy(expiry_time=datetime.datetime.utcnow() + datetime.timedelta(days=1), policy_mode='unlocked')

        try:
            self.blob_client.set_immutability_policy(immutability_policy)
            print(self.service + ": Immutability policy is set.")
            return True
        except Exception as e:
            print(self.service + ": Immutability policy is not set. Error: ", e)
            return False
        

    # set legal hold with try except block
    def set_legal_hold(self, legal_hold=None):
        # legal hold
        if legal_hold is None:
            legal_hold = random.choice([True, False])

        try:
            self.blob_client.set_legal_hold(legal_hold)
            print(self.service + ": Legal hold is set.")
            return True
        except Exception as e:
            print(self.service + ": Legal hold is not set. Error: ", e)
            return False
        
    
    # skip premium page blob tier (with premium acc)


    # set tier with try except block
    def set_standard_blob_tier(self, standard_blob_tier=None):
        print(self.service + ": Setting blob tier...")
        # standard blob tier
        if standard_blob_tier is None:
            standard_blob_tier = random.choice(['Hot', 'Cool', 'Archive'])

        try:
            self.blob_client.set_standard_blob_tier(standard_blob_tier)
            print(self.service + ": Blob tier is set.")
            return True
        except Exception as e:
            print(self.service + ": Blob tier is not set. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # stage block from url with try except block
    def stage_block_from_url(self, block_id=None, source_url=None, source_offset=None, source_length=None, source_content_md5=None):
        # block id
        if block_id is None:
            block_id = b'0x8D'
        # source url
        if source_url is None:
            source_url = f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob'
        # source offset
        if source_offset is None:
            source_offset = 0
        # source length
        if source_length is None:
            source_length = 1024
        # source content md5
        if source_content_md5 is None:
            source_content_md5 = b'0x8D'


        try:
            self.blob_client.stage_block_from_url(block_id=block_id, source_url=source_url, source_offset=source_offset, source_length=source_length, source_content_md5=source_content_md5)
            print(self.service + ": Block is staged from url.")
            return True
        except Exception as e:
            print(self.service + ": Block is not staged from url. Error: ", e)
            return False
        

    # stage block with try except block
    def stage_block(self, block_id=None, data=None, length=None):
        # block id
        if block_id is None:
            block_id = b'0x8D'
        # data
        if data is None:
            data = b'Hello World'
        # length
        if length is None:
            length = len(data)

        try:
            self.blob_client.stage_block(block_id, data, length=length)
            print(self.service + ": Block is staged.")
            return True
        except Exception as e:
            print(self.service + ": Block is not staged. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # undelete blob with try except block
    def undelete_blob(self):
            
        try:
            self.blob_client.undelete_blob()
            print(self.service + ": Blob is undeleted.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not undeleted. Error: ", e)
            return False
        

    # upload blob from bytes with try except block
    def upload_blob_from_bytes(self, data=None, blob_type=None, length=None, metadata=None):
        # data
        if data is None:
            data = b'Hello World'
        # blob type
        if blob_type is None:
            blob_type = 'BlockBlob'
        # length
        if length is None:
            length = 1024
        # metadata
        if metadata is None:
            metadata = {'metadata1': 'value1', 'metadata2': 'value2'}

        try:
            self.blob_client.upload_blob(data=data, blob_type=blob_type, length=length, metadata=metadata)
            print(self.service + ": Blob is uploaded from bytes.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not uploaded from bytes. Error: ", e)
            return False
        

    # upload blob from a url with try except block
    def upload_blob_from_url(self, source_url=None):
        # source url
        if source_url is None:
            source_url = f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob'
        try:    
            self.blob_client.upload_blob_from_url(source_url)
            print(self.service + ": Blob is uploaded from url.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not uploaded from url. Error: ", e)
            return False


    # upload page
    def upload_page(self, data=None, offset=None, length=None, validate_content=None):
        # data
        if data is None:
            # open page.txt file
            with open('page', 'rb') as f:
                data = f.read()
        # offset
        if offset is None:
            offset = 0

        try:
            self.blob_client.upload_page(data, offset, length=len(data))
            print(self.service + ": Page is uploaded.")
            return True
        except Exception as e:
            print(self.service + ": Page is not uploaded. Error: ", e)
            return False
    
    # Not implemented in the emulator
    # upload pages from url
    def upload_pages_from_url(self, source_url=None, offset=None, length=None, source_offset=None):
        # source url
        if source_url is None:
            source_url = f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob'
        # offset
        if offset is None:
            offset = 0
        # length
        if length is None:
            length = 1024
        # source offset
        if source_offset is None:
            source_offset = 0
        try:
            self.blob_client.upload_pages_from_url(source_url, offset, length, source_offset)
            print(self.service + ": Pages are uploaded from url.")
            return True
        except Exception as e:
            print(self.service + ": Pages are not uploaded from url. Error: ", e)
            return False



# if __name__ == '__main__':

    
#     # create blob client
#     blob_client = BlobClient(True)
#     # get all methods
#     methods = [getattr(BlobClient, attr) for attr in dir(BlobClient) if callable(getattr(BlobClient, attr)) and not attr.startswith("__")]

#     for i in methods:
#         print(i.__name__)
#         i(blob_client)