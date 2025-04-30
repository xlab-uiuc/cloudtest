import datetime
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings, ImmutabilityPolicy, BlobLeaseClient, BlobBlock, DelimitedJsonDialect, DelimitedTextDialect
import random
import json

# Point to certificates
# os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()
config = json.loads(open('config.json').read())

class MyBlobClient:
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
        self.account_name = config["cloud_account_name"]

        # connection string
        if emulator:
            self.connection_string = config["emulator_connection_string"]
            self.service = "**EMULATOR**"
        else:
            self.connection_string = config["cloud_connection_string"]
            self.service = "**AZURE**"

        # token
        global credential

        # create service client
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string, credential=credential)
        except Exception as e:
            print(self.service + ": Fail -- Blob service client is not received. Error: ", e)
            
        # create container client
        try:
            self.container_client = self.blob_service_client.get_container_client(self.container_name)
        except Exception as e:
            print(self.service + ": Fail -- Container client is not received. Error: ", e)
        
        # create container
        try:
            self.container_client.create_container()
        except Exception as e:
            print(self.service + ": Fail -- Container is not created. Error: ", e)

        # upload blob
        try:
            self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
        except Exception as e:
            print(self.service + ": Fail -- Blob is not created. Error: ", e)

        # create blob client
        try:
            self.blob_client = self.container_client.get_blob_client(self.blob_name)
        except Exception as e:
            print(self.service + ": Fail -- Blob client is not received. Error: ", e)


    def abort_copy(self, args):
        args = list(args)

        random_blob_name = f'blob{random.randint(1, 1000000000)}'

        if not len(args) > 0:
            if self.service == '**AZURE**':
                args.append(f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{random_blob_name}')
            else:
                args.append(f'https://127.0.0.1:10000/devstoreaccount1/{self.container_name}/{random_blob_name}')

        try:
            # create blob
            with open('page', 'rb') as data1:
                self.container_client.upload_blob(data=data1, name=random_blob_name, blob_type='BlockBlob')
            
            try:
                resp = self.blob_client.start_copy_from_url(args[0])
            except Exception as e:
                print(self.service + ": Fail -- Copy is not started. Error: ", e)
            
            res = self.blob_client.abort_copy(resp['copy_id'])
            print(self.service + ": Success -- Copy is aborted -- successful.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Copy is not aborted -- unsuccessful. Error: ", e)
            return False, e


    # acquire lease with try except block
    def acquire_lease(self, args):
        args = list(args)
        # lease duration
        if not len(args) > 0:
            args.append(20)
        # lease id
        if not len(args) > 1:
            args.append('f81d4fae-7dec-11d0-a765-00a0c91e6bf6')

        try:
            res = self.blob_client.acquire_lease(args[0], args[1])
            print(self.service + ": Success -- Lease is acquired.")

            # break lease for garbage collection
            blob_lease_client = BlobLeaseClient(self.blob_client)
            blob_lease_client.break_lease(lease_break_period=0)

            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Lease is not acquired. Error: ", e)
            return False, e

    # append blob with try except block
    def append_block(self, args):
        args = list(args)
        # data
        if not len(args) > 0:
            args.append(b'Second one')
        # length
        if not len(args) > 1:
            args.append(len(args[0]))

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            self.container_client.upload_blob(data=b'For append blob', name=random_blob_name, blob_type='AppendBlob')

            blobclient = self.container_client.get_blob_client(random_blob_name)
            res = blobclient.append_block(args[0], length=args[1])
            print(self.service + ": Success -- Blob is appended.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not appended. Error: ", e)
            return False, e
        

    # Not implemented in the emulator
    # append block from url with try except block
    def append_block_from_url(self, args):
        args = list(args)
        # copy blob name
        if not len(args) > 0:
            args.append(f'blob{random.randint(1, 1000000000)}')
        # source url
        if not len(args) > 1:
            args.append(f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{self.blob_name}')
        # source offset
        if not len(args) > 2:
            args.append(0)
        # source length
        if not len(args) > 3:
            args.append(512)
        

        try:
            self.container_client.upload_blob(data=b'For append blob', name=args[0], blob_type='AppendBlob')
            cc = self.container_client.get_blob_client(args[0])
            res = cc.append_block_from_url(copy_source_url=args[1], source_offset=args[2], source_length=args[3])
            print(self.service + ": Success -- Block is appended from url.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Block is not appended from url. Error: ", e)
            return False, e
        

    # clear page with try except block
    def clear_page(self, args):
        args = list(args)

        # offset
        if not len(args) > 0:
            args.append(0)
        # length
        if not len(args) > 1:
            args.append(512)

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)
            res = blobclient.clear_page(args[0], args[1])
            print(self.service + ": Success -- Page is cleared.")
            return True, res
                
            
        except Exception as e:
            print(self.service + ": Fail -- Page is not cleared. Error: ", e)
            return False, e
        
    
    # commit block list with try except block
    def commit_block_list(self, args):
        args = list(args)
        # block list
        if not len(args) > 0:
            args.append([BlobBlock(block_id='1'), BlobBlock(block_id='2'), BlobBlock(block_id='3')])
            
        # metadata
        if not len(args) > 1:
            args.append({'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'})


        content_setting = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            self.container_client.upload_blob(data=b'First one', name=random_blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            blobclient = self.container_client.get_blob_client(random_blob_name)
            blobclient.stage_block('1', b'AAA')
            blobclient.stage_block('2', b'BBB')
            blobclient.stage_block('3', b'CCC')

            res = blobclient.commit_block_list(args[0], content_settings=content_setting, metadata=args[1])
            print(self.service + ": Success -- Block list is committed.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Block list is not committed. Error: ", e)
            return False, e
        

    # create append blob with try except block
    def create_append_blob(self, args):
        args = list(args)
        
        # metadata
        if not len(args) > 0:
            args.append({'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'})

        content_setting = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='AppendBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)

            res = blobclient.create_append_blob(content_setting, args[0])
            print(self.service + ": Success -- Append blob is created.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Append blob is not created. Error: ", e)
            return False, e
    

    # create page blob with try except block
    def create_page_blob(self, args):
        args = list(args)
        # size
        if not len(args) > 0:
            args.append(512)
        # metadata
        if not len(args) > 1:
            args.append({'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'})
        # premium page blob tier
        # if not len(args) > 2:
        #     args.append('P4')

        content_setting = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)

            res = blobclient.create_page_blob(args[0], content_setting, args[1])
            print(self.service + ": Success -- Page blob is created.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Page blob is not created. Error: ", e)
            return False, e
    


    # create snapshot with try except block
    def create_snapshot(self, args):
        args = list(args)
        # metadata
        if not len(args) > 0:
            args.append({'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'})

        try:
            res = self.blob_client.create_snapshot(args[0])
            print(self.service + ": Success -- Snapshot is created.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Snapshot is not created. Error: ", e)
            return False, e
        

    # delete blob with try except block
    def delete_blob(self, args):
        args = list(args)
        # delete snapshots
        if not len(args) > 0:
            args.append('include')

        try:
            res = self.blob_client.delete_blob(args[0])
            print(self.service + ": Success -- Blob is deleted.")

            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not deleted. Error: ", e)
            return False, e
        
    
    # delete immutability policy with try except block
    def delete_immutability_policy(self, args):
        args = list(args)
        try:
            res = self.blob_client.delete_immutability_policy()
            print(self.service + ": Success -- Immutability policy is deleted.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Immutability policy is not deleted. Error: ", e)
            return False, e
        


    # download Block blob with try except block
    def download_block_blob(self, args):
        args = list(args)
        # offset
        if not len(args) > 0:
            args.append(0)
        # length
        if not len(args) > 1:
            args.append(512)

        try:
            res = self.blob_client.download_blob(args[0], args[1])
            print(self.service + ": Success -- Block Blob is downloaded.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Block Blob is not downloaded. Error: ", e)
            return False, e
        
    # download Append blob with try except block
    def download_append_blob(self, args):
        args = list(args)
        # offset
        if not len(args) > 0:
            args.append(0)
        # length
        if not len(args) > 1:
            args.append(512)

        try:
            # upload append blob
            self.blob_name = f'blob{random.randint(1, 1000000000)}'
            self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='AppendBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            blob_client = self.container_client.get_blob_client(self.blob_name)
            # download append blob
            res = blob_client.download_blob(args[0], args[1])
            print(self.service + ": Success -- Append Blob is downloaded.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Append Blob is not downloaded. Error: ", e)
            return False, e
        
    # download Page blob with try except block
    def download_page_blob(self, args):
        args = list(args)
        # offset
        if not len(args) > 0:
            args.append(0)
        # length
        if not len(args) > 1:
            args.append(512)

        try:
            # upload page blob
            self.blob_name = f'blob{random.randint(1, 1000000000)}'
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=self.blob_name, blob_type='PageBlob')
            blob_client = self.container_client.get_blob_client(self.blob_name)
            # download page blob
            res = blob_client.download_blob(args[0], args[1])
            print(self.service + ": Success -- Page Blob is downloaded.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Page Blob is not downloaded. Error: ", e)
            return False, e


    # check if blob exists with try except block
    def exists(self, args):
        args = list(args)

        try:
            res = self.blob_client.exists()
            print(self.service + ": Success -- Blob exists succeeded -- ", res)
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob exists failed. Error: ", e)
            return False, e
        
    # create blob client from blob url with try except block
    def from_blob_url(self, args):
        args = list(args)

        if not len(args) > 0:
            if self.service == '**AZURE**':
                args.append(f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{self.blob_name}')
            else:
                args.append(f'https://127.0.0.1:10000/devstoreaccount1/{self.container_name}/{self.blob_name}')
                
        try: 
            res = self.blob_client.from_blob_url(args[0])
            print(self.service + ": Success -- Blob client is created from blob url.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob client is not created from blob url. Error: ", e)
            return False, e
        

    # get account information with try except block
    def get_account_information(self, args):
        args = list(args)
        try:
            res = self.blob_client.get_account_information()
            print(self.service + ": Success -- Account information is retrieved.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Account information is not retrieved. Error: ", e)
            return False, e
        

    # get blob properties with try except block
    def get_blob_properties(self, args):
        args = list(args)

        try:
            res = self.blob_client.get_blob_properties()
            print(self.service + ": Success -- Blob properties are retrieved.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob properties are not retrieved. Error: ", e)
            return False, e
        


    # get blob tags with try except block
    def get_blob_tags(self, args):
        args = list(args)

        try:
            res = self.blob_client.get_blob_tags()
            print(self.service + ": Success -- Blob tags are retrieved.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob tags are not retrieved. Error: ", e)
            return False, e
        

    # get block list with try except block
    def get_block_list(self, args):
        args = list(args)
        # block list type
        if not len(args) > 0:
            args.append('committed')

        try:
            res = self.blob_client.get_block_list(args[0])
            print(self.service + ": Success -- Block list is retrieved.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Block list is not retrieved. Error: ", e)
            return False, e
        
        
    # get page ranges with try except block
    def get_page_ranges(self, args):
        args = list(args)

        # start range
        if not len(args) > 0:
            args.append(0)
        # end range
        if not len(args) > 1:
            args.append(512)

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)
            res = blobclient.get_page_ranges(offset=args[0], length=args[1])
            print(self.service + ": Success -- Page ranges are retrieved.")
            return True, res
            
        except Exception as e:
            print(self.service + ": Fail -- Page ranges are not retrieved. Error: ", e)
            return False, e
            

    # list page ranges diff with try except block
    def list_page_ranges_diff(self, args):
        args = list(args)
        # previous snapshot
        if not len(args) > 0:
            args.append('snapshot')
        # start range
        if not len(args) > 1:
            args.append(0)
        # end range
        if not len(args) > 2:
            args.append(512)

        try:
            res = self.blob_client.list_page_ranges(previous_snapshot=args[0], offset=args[1], length=args[2])
            print(self.service + ": Success -- Page ranges diff is retrieved.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Page ranges diff is not retrieved. Error: ", e)
            return False, e
        

    # query blob contents with try except block
    def query_blob(self, args):
        args = list(args)
        # query expression
        if not len(args) > 0:
            args.append('SELECT _2 from BlobStorage')
        # input format
        if not len(args) > 1:
            args.append(DelimitedTextDialect(delimiter=',', quotechar='"', lineterminator='\n', escapechar="", has_header=False))
        # output format
        if not len(args) > 2:
            args.append(DelimitedJsonDialect(delimiter='\n'))

        try:
            res = self.blob_client.query_blob(args[0], blob_format=args[1], output_format=args[2])
            print(self.service + ": Success -- Blob contents are queried.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob contents are not queried. Error: ", e)
            return False, e
        

    # resize blob with try except block
    def resize_blob(self, args):
        args = list(args)
        # size
        if not len(args) > 0:
            args.append(1024)

        try:
            # create page blob
            random_blob_name = f'blob{random.randint(1, 1000000000)}'
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')

            blobclient = self.container_client.get_blob_client(random_blob_name)
            res = blobclient.resize_blob(args[0])
            
            print(self.service + ": Success -- Blob is resized.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not resized. Error: ", e)
            return False, e
        
    # seal append blob by first creating it with try except block
    def seal_append_blob(self, args):
        args = list(args)

        try:
            # create append blob
            random_blob_name = f'blob{random.randint(1, 1000000000)}'
            self.container_client.upload_blob(data=b'Hello World', name=random_blob_name, blob_type='AppendBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)
            res = blobclient.seal_append_blob()
            print(self.service + ": Success -- Append blob is sealed.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Append blob is not sealed. Error: ", e)
            return False, e
        
    

    # set blob metadata with try except block
    def set_blob_metadata(self, args):
        args = list(args)
        # metadata
        if not len(args) > 0:
            args.append({'metadata1': 'value1', 'metadata2': 'value2'})


        try:
            res = self.blob_client.set_blob_metadata(args[0])
            print(self.service + ": Success -- Blob metadata is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob metadata is not set. Error: ", e)
            return False, e
        


    # set blob tags with try except block
    def set_blob_tags(self, args):
        args = list(args)
        # tags
        if not len(args) > 0:
            args.append({'tag1': 'value1', 'tag2': 'value2'})

        try:
            res = self.blob_client.set_blob_tags(args[0])
            print(self.service + ": Success -- Blob tags are set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob tags are not set. Error: ", e)
            return False, e
        

    # set http headers with try except block
    def set_http_headers(self, args):
        args = list(args)
        
        # content settings
        content_setting = ContentSettings(content_type='text/plain')

        try:
            res = self.blob_client.set_http_headers(content_setting)
            print(self.service + ": Success -- HTTP headers are set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- HTTP headers are not set. Error: ", e)
            return False, e
        


    # set immutability policy with try except block
    def set_immutability_policy(self, args):
        args = list(args)
        # immutability policy
        policy = ImmutabilityPolicy(expiry_time=datetime.datetime.utcnow() + datetime.timedelta(1), policy_mode='unlocked')

        try:
            res = self.blob_client.set_immutability_policy(policy)
            print(self.service + ": Success -- Immutability policy is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Immutability policy is not set. Error: ", e)
            return False, e
        

    # set legal hold with try except block
    def set_legal_hold(self, args):
        args = list(args)
        # legal hold
        if not len(args) > 0:
            args.append(False)

        try:
            res = self.blob_client.set_legal_hold(args[0])
            print(self.service + ": Success -- Legal hold is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Legal hold is not set. Error: ", e)
            return False, e
        
    
    # set sequence number with try except block
    def set_sequence_number(self, args):
        args = list(args)
        # sequence number action
        if not len(args) > 0:
            args.append("UPDATE")

        # sequence number
        if not len(args) > 1:
            args.append(6)

        try:
            # create page blob
            random_blob_name = f'blob{random.randint(1, 1000000000)}'
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blob_client = self.container_client.get_blob_client(random_blob_name)

            res = blob_client.set_sequence_number(args[0], args[1])
            print(self.service + ": Success -- Sequence number is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Sequence number is not set. Error: ", e)
            return False, e


    # set tier with try except block
    def set_standard_blob_tier(self, args):
        args = list(args)
      
        # standard blob tier
        if not len(args) > 0:
            args.append(['Hot'])

        try:
            res = self.blob_client.set_standard_blob_tier(args[0])
            print(self.service + ": Success -- Blob tier is set.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob tier is not set. Error: ", e)
            return False, e


    # stage block with try except block
    def stage_block(self, args):
        args = list(args)
        # block id
        if not len(args) > 0:
            args.append(b'0x8D')
        # data
        if not len(args) > 1:
            args.append(b'Hello World')
        # length
        if not len(args) > 2:
            args.append(len(args[1]))

        try:
            res = self.blob_client.stage_block(args[0], args[1], length=args[2])
            print(self.service + ": Success -- Block is staged.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Block is not staged. Error: ", e)
            return False, e    

    # Not implemented in the emulator
    # stage block from url with try except block
    def stage_block_from_url(self, args):
        args = list(args)

        random_blob = f'blob{random.randint(1, 1000000)}'
        # upload blob
        try:
            #upload blob from file page
            with open('page', 'rb') as data:
                self.container_client.upload_blob(random_blob, data, blob_type='BlockBlob')
            print(self.service + ": Success -- Blob is uploaded.")
        except Exception as e:
            print(self.service + ": Fail -- Blob is not uploaded. Error: ", e)
            return False, e
 
        # block id
        if not len(args) > 0:
            args.append(b'0x8D')
        # source url
        if not len(args) > 1:
            args.append(f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{random_blob}')
        # source offset
        if not len(args) > 2:
            args.append(0)
        # source length
        if not len(args) > 3:
            args.append(512)
        # source content valid md5
        if not len(args) > 4:
            args.append('')


        try:
            res = self.blob_client.stage_block_from_url(block_id=args[0], source_url=args[1], source_offset=args[2], source_length=args[3], source_content_md5=args[4])
            print(self.service + ": Success -- Block is staged from url.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Block is not staged from url. Error: ", e)
            return False, e
        
        

    # start copy from url with try except block
    def start_copy_from_url(self, args):
        args = list(args)
        # source url
        blob_name = ''
        if not len(args) > 0:
            args.append(f'blob{random.randint(1, 10000000)}')

        # metadata
        if not len(args) > 1:
            args.append({'hello': 'world'})

        # source url
        if not len(args) > 2:
            if self.service == '**AZURE**':
                args.append(f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{args[0]}')
            else:
                args.append(f'https://127.0.0.1:10000/devstoreaccount1/{self.container_name}/{args[0]}')

        try:
            with open('page', 'rb') as data1:
                self.container_client.upload_blob(data=data1, name=args[0], blob_type='BlockBlob')

            res = self.blob_client.start_copy_from_url(args[2], metadata=args[1])
            print(self.service + ": Success -- Copy from url started.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Copy from url not started. Error: ", e)
            return False, e
        

    # Not implemented in the emulator
    # undelete blob with try except block
    def undelete_blob(self, args):
        args = list(args)

        # delete blob or not
        if not len(args) > 0:
            args.append(True)
            
        try:
            if args[0]:
                try:
                    self.blob_client.delete_blob()
                    print(self.service + ": Success -- Blob is deleted before undeletion.")
                except Exception as e:
                    print(self.service + ": Fail -- Blob is not deleted before undeletion. Error: ", e)
            res = self.blob_client.undelete_blob()
            print(self.service + ": Success -- Blob is undeleted.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not undeleted. Error: ", e)
            return False, e
        

    # upload blob from bytes with try except block
    def upload_blob_from_bytes(self, args):
        args = list(args)
        # data
        if not len(args) > 0:
            args.append(b'Hello World')
        # blob type
        if not len(args) > 1:
            args.append('BlockBlob')
        # length
        if not len(args) > 2:
            args.append(len(args[0]))
        # metadata
        if not len(args) > 3:
            args.append({'metadata1': 'value1', 'metadata2': 'value2'})

        try:
            blob_client = self.container_client.get_blob_client(f'blob{random.randint(0, 1000000)}')
            res = blob_client.upload_blob(data=args[0], blob_type=args[1], length=args[2], metadata=args[3])
            print(self.service + ": Success -- Blob is uploaded from bytes.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not uploaded from bytes. Error: ", e)
            return False, e
        

    # upload blob from a url with try except block
    def upload_blob_from_url(self, args):
        args = list(args)

        random_blob_name = f'blob{random.randint(0, 1000000)}'
        # source url
        if not len(args) > 0:
            if self.service == '**AZURE**':
                args.append(f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{self.blob_name}')
            else:
                args.append(f'https://127.0.0.1:10000/devstoreaccount1/{self.container_name}/{self.blob_name}')
        try:
            blob_client = self.container_client.get_blob_client(random_blob_name)    
            res = blob_client.upload_blob_from_url(args[0])
            print(self.service + ": Success -- Blob is uploaded from url.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not uploaded from url. Error: ", e)
            return False, e


    # upload page
    def upload_page(self, args):
        args = list(args)
        # data
        if not len(args) > 0:
            # open page.txt file
            with open('page', 'rb') as f:
                args.append(f.read())
        if not len(args) > 1:
            args.append(0)

        try:
            # upload blob
            blob = f'blob{random.randint(0, 1000000)}'
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=blob, blob_type='PageBlob')

            blob_client = self.container_client.get_blob_client(blob)
            res = blob_client.upload_page(args[0], 0, length=512)
            res = blob_client.upload_page(args[0], 512+args[1], length=len(args[0])-512)
            print(self.service + ": Success -- Page is uploaded.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Page is not uploaded. Error: ", e)
            return False, e
    
    # Not implemented in the emulator
    # upload pages from url
    def upload_pages_from_url(self, args):
        args = list(args)

        random_blob = f'blob{random.randint(0, 1000000)}'
        # upload blob
        try:
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob, blob_type='PageBlob')
        except Exception as e:
            print(self.service + ": Fail -- Page is not uploaded. Error: ", e)
            return False, e

        # source url
        if not len(args) > 0:
            args.append(f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{random_blob}')
        # offset
        if not len(args) > 1:
            args.append(0)
        # length
        if not len(args) > 2:
            args.append(512)
        # source offset
        if not len(args) > 3:
            args.append(0)
        try:
            cc = self.container_client.get_blob_client(random_blob)
            res = cc.upload_pages_from_url(args[0], args[1], args[2], args[3])
            print(self.service + ": Success -- Pages are uploaded from url.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Pages are not uploaded from url. Error: ", e)
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
            

