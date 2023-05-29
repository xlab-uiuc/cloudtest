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
    def abort_copy(self, **args):
        # copy id
        if args['copy_id'] is None:
            args['copy_id'] = 'C56A4180-65AA-42EC-A945-5FD21DEC0538'
        try:
            self.blob_client.abort_copy(args['copy_id'])
            print(self.service + ": Copy is aborted -- successful.")
            return True
        except Exception as e:
            print(self.service + ": Copy is not aborted -- unsuccessful. Error: ", e)
            return False


    # decreases coverage during testing
    # acquire lease with try except block
    def acquire_lease(self, **args):
        # lease duration
        if args['lease_duration'] is None:
            args['lease_duration'] = 20
        # lease id
        if args['lease_id'] is None:
            args['lease_id'] = 'f81d4fae-7dec-11d0-a765-00a0c91e6bf6'

        try:
            self.blob_client.acquire_lease(args['lease_duration'], args['lease_id'])
            print(self.service + ": Lease is acquired.")
            return True
        except Exception as e:
            print(self.service + ": Lease is not acquired. Error: ", e)
            return False

    # Not implemented in the emulator
    # append blob with try except block
    def append_block(self, **args):
        # data
        if args['data'] is None:
            args['data'] = b'First one'
        # length
        if args['length'] is None:
            args['length'] = len(args['data'])
        else:
            args['length'] = args['length']

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            with open('page', 'rb') as data1:
                self.container_client.upload_blob(data=data1, name=random_blob_name, blob_type='AppendBlob')

            blobclient = self.container_client.get_blob_client(random_blob_name)
            blobclient.append_block(args['data'], length=args['length'])
            print(self.service + ": Blob is appended.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not appended. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # append block from url with try except block
    def append_block_from_url(self, **args):
        # copy blob name
        if args['copy_blob_name'] is None:
            args['copy_blob_name'] = f'blob{random.randint(1, 1000000000)}'
        # source url
        if args['source_url'] is None:
            args['source_url'] = f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/'+args['copy_blob_name']
        # source offset
        if args['source_offset'] is None:
            args['source_offset'] = 0
        # source length
        if args['source_length'] is None:
            args['source_length'] = 512
        

        try:
            self.blob_client.append_block_from_url(copy_source_url=args['source_url'], source_offset=args['source_offset'], source_length=args['source_length'])
            print(self.service + ": Block is appended.")
            return True
        except Exception as e:
            print(self.service + ": Block is not appended. Error: ", e)
            return False
        

    # clear page with try except block
    def clear_page(self, **args):

        # offset
        if args['offset'] is None:
            args['offset'] = 0
        # length
        if args['length'] is None:
            args['length'] = 512

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)
            blobclient.clear_page(args['offset'], args['length'])
            print(self.service + ": Page is cleared.")
            return True
                
            
        except Exception as e:
            print(self.service + ": Page is not cleared. Error: ", e)
            return False
        
    
    # commit block list with try except block
    def commit_block_list(self, **args):
        # block list
        if args['block_list'] is None:
            args['block_list'] = ['AAA=', 'BBB=', 'CCC=']
        # content settings
        if args['content_settings'] is None:
            args['content_settings'] = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')
        # metadata
        if args['metadata'] is None:
            args['metadata'] = {'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'}


        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            self.container_client.upload_blob(data=b'First one', name=random_blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            blobclient = self.container_client.get_blob_client(random_blob_name)

            blobclient.commit_block_list(args['block_list'], content_settings=args['content_settings'], metadata=args['metadata'])
            print(self.service + ": Block list is committed.")
            return True
        except Exception as e:
            print(self.service + ": Block list is not committed. Error: ", e)
            return False
        

    # create append blob with try except block
    def create_append_blob(self, **args):
        # content settings
        if args['content_settings'] is None:
            args['content_settings'] = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')
        # metadata
        if args['metadata'] is None:
            args['metadata'] = {'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'}

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='AppendBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)

            blobclient.create_append_blob(args['content_settings'], args['metadata'])
            print(self.service + ": Append blob is created.")
            return True
        except Exception as e:
            print(self.service + ": Append blob is not created. Error: ", e)
            return False
    

    # create page blob with try except block
    def create_page_blob(self, **args):
        # size
        if args['size'] is None:
            args['size'] = 512
        # content settings
        if args['content_settings'] is None:
            args['content_settings'] = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')
        # metadata
        if args['metadata'] is None:
            args['metadata'] = {'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'}
        # premium page blob tier
        if args['premium_page_blob_tier'] is None:
            args['premium_page_blob_tier'] = 'P4'

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)

            blobclient.create_page_blob(args['size'], args['content_settings'], args['metadata'])
            print(self.service + ": Page blob is created.")
            return True
        except Exception as e:
            print(self.service + ": Page blob is not created. Error: ", e)
            return False
    


    # create snapshot with try except block
    def create_snapshot(self, **args):
        # metadata
        if args['metadata'] is None:
            args['metadata'] = {'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'}

        try:
            self.blob_client.create_snapshot(args['metadata'])
            print(self.service + ": Snapshot is created.")
            return True
        except Exception as e:
            print(self.service + ": Snapshot is not created. Error: ", e)
            return False
        

    # # delete blob with try except block
    def delete_blob(self, **args):
        # delete snapshots
        if args['delete_snapshots'] is None:
            args['delete_snapshots'] = 'include'

        try:
            self.blob_client.delete_blob(args['delete_snapshots'])
            print(self.service + ": Blob is deleted.")
            # create same blob again
            self.container_client.upload_blob(data=b'Second one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            self.blob_client = self.container_client.get_blob_client(self.blob_name)
            return True
        except Exception as e:
            print(self.service + ": Blob is not deleted. Error: ", e)
            return False
        
    
    # delete immutability policy with try except block
    def delete_immutability_policy(self, **args):
        try:
            self.blob_client.delete_immutability_policy()
            print(self.service + ": Immutability policy is deleted.")
            return True
        except Exception as e:
            print(self.service + ": Immutability policy is not deleted. Error: ", e)
            return False
        


    # download blob with try except block
    def download_blob(self, **args):
        # offset
        if args['offset'] is None:
            args['offset'] = 0
        # length
        if args['length'] is None:
            args['length'] = 512

        try:
            self.blob_client.download_blob(args['offset'], args['length'])
            print(self.service + ": Blob is downloaded.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not downloaded. Error: ", e)
            return False
        

    # check if blob exists with try except block
    def exists(self, **args):

        try:
            self.blob_client.exists()
            print(self.service + ": Blob exists.")
            return True
        except Exception as e:
            print(self.service + ": Blob does not exist. Error: ", e)
            return False
        

    # get account information with try except block
    def get_account_information(self, **args):
        try:
            self.blob_client.get_account_information()
            print(self.service + ": Account information is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Account information is not retrieved. Error: ", e)
            return False
        

    # get blob properties with try except block
    def get_blob_properties(self, **args):

        try:
            self.blob_client.get_blob_properties()
            print(self.service + ": Blob properties are retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Blob properties are not retrieved. Error: ", e)
            return False
        


    # get blob tags with try except block
    def get_blob_tags(self, **args):

        try:
            self.blob_client.get_blob_tags()
            print(self.service + ": Blob tags are retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Blob tags are not retrieved. Error: ", e)
            return False
        

    # get block list with try except block
    def get_block_list(self, **args):
        # block list type
        if args['block_list_type'] is None:
            args['block_list_type'] = 'committed'

        try:
            self.blob_client.get_block_list(args['block_list_type'])
            print(self.service + ": Block list is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Block list is not retrieved. Error: ", e)
            return False
        
        
    # get page ranges with try except block
    def get_page_ranges(self, **args):

        # start range
        if args['start_range'] is None:
            args['start_range'] = 0
        # end range
        if args['end_range'] is None:
            args['end_range'] = 512

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)
            blobclient.get_page_ranges(offset=args['start_range'], length=args['end_range'])
            print(self.service + ": Page ranges are retrieved.")
            return True
            
        except Exception as e:
            print(self.service + ": Page ranges are not retrieved. Error: ", e)
            return False
            

    # list page ranges diff with try except block
    def list_page_ranges_diff(self, **args):
        # previous snapshot
        if args['previous_snapshot'] is None:
            args['previous_snapshot'] = 'snapshot'
        # start range
        if args['start_range'] is None:
            args['start_range'] = 0
        # end range
        if args['end_range'] is None:
            args['end_range'] = 512

        try:
            self.blob_client.list_page_ranges(previous_snapshot=args['previous_snapshot'], offset=args['start_range'], length=args['end_range'])
            print(self.service + ": Page ranges diff is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Page ranges diff is not retrieved. Error: ", e)
            return False
        

    # query blob contents with try except block
    def query_blob(self, **args):
        # query expression
        if args['query_expression'] is None:
            args['query_expression'] = 'SELECT _2 from BlobStorage'

        try:
            self.blob_client.query_blob(args['query_expression'])
            print(self.service + ": Blob contents are queried.")
            return True
        except Exception as e:
            print(self.service + ": Blob contents are not queried. Error: ", e)
            return False
        

        

    # set blob metadata with try except block
    def set_blob_metadata(self, **args):
        # metadata
        if args['metadata'] is None:
            args['metadata'] = {'metadata1': 'value1', 'metadata2': 'value2'}


        try:
            self.blob_client.set_blob_metadata(args['metadata'])
            print(self.service + ": Blob metadata is set.")
            return True
        except Exception as e:
            print(self.service + ": Blob metadata is not set. Error: ", e)
            return False
        


    # set blob tags with try except block
    def set_blob_tags(self, **args):
        # tags
        if args['tags'] is None:
            args['tags'] = {'tag1': 'value1', 'tag2': 'value2'}

        try:
            self.blob_client.set_blob_tags(args['tags'])
            print(self.service + ": Blob tags are set.")
            return True
        except Exception as e:
            print(self.service + ": Blob tags are not set. Error: ", e)
            return False
        

    # set http headers with try except block
    def set_http_headers(self, **args):
        # content settings
        if args['content_settings'] is None:
            args['content_settings'] = ContentSettings(content_type='text/plain')

        try:
            self.blob_client.set_http_headers(args['content_settings'])
            print(self.service + ": HTTP headers are set.")
            return True
        except Exception as e:
            print(self.service + ": HTTP headers are not set. Error: ", e)
            return False
        


    # set immutability policy with try except block
    def set_immutability_policy(self, **args):
        # immutability policy
        if args['immutability_policy'] is None:
            args['immutability_policy'] = ImmutabilityPolicy(expiry_time=datetime.datetime.utcnow() + datetime.timedelta(days=1), policy_mode='unlocked')

        try:
            self.blob_client.set_immutability_policy(args['immutability_policy'])
            print(self.service + ": Immutability policy is set.")
            return True
        except Exception as e:
            print(self.service + ": Immutability policy is not set. Error: ", e)
            return False
        

    # set legal hold with try except block
    def set_legal_hold(self, **args):
        # legal hold
        if args['legal_hold'] is None:
            args['legal_hold'] = random.choice([True, False])

        try:
            self.blob_client.set_legal_hold(args['legal_hold'])
            print(self.service + ": Legal hold is set.")
            return True
        except Exception as e:
            print(self.service + ": Legal hold is not set. Error: ", e)
            return False
        
    
    # skip premium page blob tier (with premium acc)


    # set tier with try except block
    def set_standard_blob_tier(self, **args):
        print(self.service + ": Setting blob tier...")
        # standard blob tier
        if args['standard_blob_tier'] is None:
            args['standard_blob_tier'] = random.choice(['Hot', 'Cool', 'Archive'])

        try:
            self.blob_client.set_standard_blob_tier(args['standard_blob_tier'])
            print(self.service + ": Blob tier is set.")
            return True
        except Exception as e:
            print(self.service + ": Blob tier is not set. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # stage block from url with try except block
    def stage_block_from_url(self, **args):
        # block id
        if args['block_id'] is None:
            args['block_id'] = b'0x8D'
        # source url
        if args['source_url'] is None:
            args['source_url'] = f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob'
        # source offset
        if args['source_offset'] is None:
            args['source_offset'] = 0
        # source length
        if args['source_length'] is None:
            args['source_length'] = 512
        # source content md5
        if args['source_content_md5'] is None:
            args['source_content_md5'] = b'0x8D'


        try:
            self.blob_client.stage_block_from_url(block_id=args['block_id'], source_url=args['source_url'], source_offset=args['source_offset'], source_length=args['source_length'], source_content_md5=args['source_content_md5'])
            print(self.service + ": Block is staged from url.")
            return True
        except Exception as e:
            print(self.service + ": Block is not staged from url. Error: ", e)
            return False
        

    # stage block with try except block
    def stage_block(self, **args):
        # block id
        if args['block_id'] is None:
            args['block_id'] = b'0x8D'
        # data
        if args['data'] is None:
            args['data'] = b'Hello World'
        # length
        if args['length'] is None:
            args['length'] = len(args['data'])

        try:
            self.blob_client.stage_block(args['block_id'], args['data'], length=args['length'])
            print(self.service + ": Block is staged.")
            return True
        except Exception as e:
            print(self.service + ": Block is not staged. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # undelete blob with try except block
    def undelete_blob(self, **args):
            
        try:
            self.blob_client.undelete_blob()
            print(self.service + ": Blob is undeleted.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not undeleted. Error: ", e)
            return False
        

    # upload blob from bytes with try except block
    def upload_blob_from_bytes(self, **args):
        # data
        if args['data'] is None:
            args['data'] = b'Hello World'
        # blob type
        if args['blob_type'] is None:
            args['blob_type'] = 'BlockBlob'
        # length
        if args['length'] is None:
            args['length'] = len(args['data'])
        # metadata
        if args['metadata'] is None:
            args['metadata'] = {'metadata1': 'value1', 'metadata2': 'value2'}

        try:
            self.blob_client.upload_blob(data=args['data'], blob_type=args['blob_type'], length=args['length'], metadata=args['metadata'])
            print(self.service + ": Blob is uploaded from bytes.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not uploaded from bytes. Error: ", e)
            return False
        

    # upload blob from a url with try except block
    def upload_blob_from_url(self, **args):
        # source url
        if args['source_url'] is None:
            args['source_url'] = f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob'
        try:    
            self.blob_client.upload_blob_from_url(args['source_url'])
            print(self.service + ": Blob is uploaded from url.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not uploaded from url. Error: ", e)
            return False


    # upload page
    def upload_page(self, **args):
        # data
        if args['data'] is None:
            # open page.txt file
            with open('page', 'rb') as f:
                args['data'] = f.read()
        # offset
        if offset is None:
            offset = 0

        try:
            self.blob_client.upload_page(args['data'], offset, length=len(args['data']))
            print(self.service + ": Page is uploaded.")
            return True
        except Exception as e:
            print(self.service + ": Page is not uploaded. Error: ", e)
            return False
    
    # Not implemented in the emulator
    # upload pages from url
    def upload_pages_from_url(self, **args):
        # source url
        if args['source_url'] is None:
            args['source_url'] = f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob'
        # offset
        if args['offset'] is None:
            args['offset'] = 0
        # length
        if args['length'] is None:
            args['length'] = 512
        # source offset
        if args['source_offset'] is None:
            args['source_offset'] = 0
        try:
            self.blob_client.upload_pages_from_url(args['source_url'], args['offset'], args['length'], args['source_offset'])
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