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
            
        self.account_name = 'sdkfuzz'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=Kt8fMYDEpeaq/A6TRBU+1+LRMIqd2h9Nv7Hd/qCn4B9DqvbNDXPJWU4BRqu50GVEjFfcocumL1lr+AStfVsaPA==;EndpointSuffix=core.windows.net'
            self.service = "**AZURE**"


        # create container client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        self.container_client.create_container()

        # create blob client
        self.container_client.upload_blob(data=b'First one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
        self.blob_client = self.container_client.get_blob_client(self.blob_name)


    # abort copy with parameters default none and try except block
    def abort_copy(self, *args):
        args = list(args)
        # copy id
        if not len(args) > 0:
            args.append('C56A4180-65AA-42EC-A945-5FD21DEC0538')
        try:
            self.blob_client.abort_copy(args[0])
            print(self.service + ": Copy is aborted -- successful.")
            return True
        except Exception as e:
            print(self.service + ": Copy is not aborted -- unsuccessful. Error: ", e)
            return False


    # decreases coverage during testing
    # acquire lease with try except block
    def acquire_lease(self, *args):
        args = list(args)
        # lease duration
        if not len(args) > 0:
            args.append(20)
        # lease id
        if not len(args) > 1:
            args.append('f81d4fae-7dec-11d0-a765-00a0c91e6bf6')

        try:
            self.blob_client.acquire_lease(args[0], args[1])
            print(self.service + ": Lease is acquired.")
            return True
        except Exception as e:
            print(self.service + ": Lease is not acquired. Error: ", e)
            return False

    # Not implemented in the emulator
    # append blob with try except block
    def append_block(self, *args):
        args = list(args)
        # data
        if not len(args) > 0:
            args.append(b'First one')
        # length
        if not len(args) > 1:
            args.append(len(args[0]))
        else:
            args.append(args[1])

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            with open('page', 'rb') as data1:
                self.container_client.upload_blob(data=data1, name=random_blob_name, blob_type='AppendBlob')

            blobclient = self.container_client.get_blob_client(random_blob_name)
            blobclient.append_block(args[0], length=args[1])
            print(self.service + ": Blob is appended.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not appended. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # append block from url with try except block
    def append_block_from_url(self, *args):
        args = list(args)
        # copy blob name
        if not len(args) > 0:
            args.append(f'blob{random.randint(1, 1000000000)}')
        # source url
        if not len(args) > 1:
            args.append(f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{args[0]}')
        # source offset
        if not len(args) > 2:
            args.append(0)
        # source length
        if not len(args) > 3:
            args.append(512)
        

        try:
            self.blob_client.append_block_from_url(copy_source_url=args[1], source_offset=args[2], source_length=args[3])
            print(self.service + ": Block is appended.")
            return True
        except Exception as e:
            print(self.service + ": Block is not appended. Error: ", e)
            return False
        

    # clear page with try except block
    def clear_page(self, *args):
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
            blobclient.clear_page(args[0], args[1])
            print(self.service + ": Page is cleared.")
            return True
                
            
        except Exception as e:
            print(self.service + ": Page is not cleared. Error: ", e)
            return False
        
    
    # commit block list with try except block
    def commit_block_list(self, *args):
        args = list(args)
        # block list
        if not len(args) > 0:
            args.append(['AAA=', 'BBB=', 'CCC='])
            
        # metadata
        if not len(args) > 1:
            args.append({'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'})


        content_setting = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            self.container_client.upload_blob(data=b'First one', name=random_blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            blobclient = self.container_client.get_blob_client(random_blob_name)

            blobclient.commit_block_list(args[0], content_settings=content_setting, metadata=args[1])
            print(self.service + ": Block list is committed.")
            return True
        except Exception as e:
            print(self.service + ": Block list is not committed. Error: ", e)
            return False
        

    # create append blob with try except block
    def create_append_blob(self, *args):
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

            blobclient.create_append_blob(content_setting, args[0])
            print(self.service + ": Append blob is created.")
            return True
        except Exception as e:
            print(self.service + ": Append blob is not created. Error: ", e)
            return False
    

    # create page blob with try except block
    def create_page_blob(self, *args):
        args = list(args)
        # size
        if not len(args) > 0:
            args.append(512)
        # metadata
        if not len(args) > 1:
            args.append({'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'})
        # premium page blob tier
        if not len(args) > 2:
            args.append('P4')

        content_setting = ContentSettings(content_type='text/plain', content_encoding='utf-8', cache_control='None', content_language='en-US', content_disposition='inline')

        try:
            random_blob_name = f'blob{random.randint(1, 1000000000)}'

            # create page blob, data as file page.txt and upload
            with open('page', 'rb') as data:
                self.container_client.upload_blob(data=data, name=random_blob_name, blob_type='PageBlob')
            blobclient = self.container_client.get_blob_client(random_blob_name)

            blobclient.create_page_blob(args[0], content_setting, args[1])
            print(self.service + ": Page blob is created.")
            return True
        except Exception as e:
            print(self.service + ": Page blob is not created. Error: ", e)
            return False
    


    # create snapshot with try except block
    def create_snapshot(self, *args):
        args = list(args)
        # metadata
        if not len(args) > 0:
            args.append({'category': 'test', 'created': '2020-01-01', 'author': 'test', 'description': 'test', 'tags': 'test', 'title': 'test', 'version': '1.0', 'filename': 'test'})

        try:
            self.blob_client.create_snapshot(args[0])
            print(self.service + ": Snapshot is created.")
            return True
        except Exception as e:
            print(self.service + ": Snapshot is not created. Error: ", e)
            return False
        

    # # delete blob with try except block
    def delete_blob(self, *args):
        args = list(args)
        # delete snapshots
        if not len(args) > 0:
            args.append('include')

        try:
            self.blob_client.delete_blob(args[0])
            print(self.service + ": Blob is deleted.")
            # create same blob again
            self.container_client.upload_blob(data=b'Second one', name=self.blob_name, blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
            self.blob_client = self.container_client.get_blob_client(self.blob_name)
            return True
        except Exception as e:
            print(self.service + ": Blob is not deleted. Error: ", e)
            return False
        
    
    # delete immutability policy with try except block
    def delete_immutability_policy(self, *args):
        args = list(args)
        try:
            self.blob_client.delete_immutability_policy()
            print(self.service + ": Immutability policy is deleted.")
            return True
        except Exception as e:
            print(self.service + ": Immutability policy is not deleted. Error: ", e)
            return False
        


    # download blob with try except block
    def download_blob(self, *args):
        args = list(args)
        # offset
        if not len(args) > 0:
            args.append(0)
        # length
        if not len(args) > 1:
            args.append(512)

        try:
            self.blob_client.download_blob(args[0], args[1])
            print(self.service + ": Blob is downloaded.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not downloaded. Error: ", e)
            return False
        

    # check if blob exists with try except block
    def exists(self, *args):
        args = list(args)

        try:
            self.blob_client.exists()
            print(self.service + ": Blob exists.")
            return True
        except Exception as e:
            print(self.service + ": Blob does not exist. Error: ", e)
            return False
        

    # get account information with try except block
    def get_account_information(self, *args):
        args = list(args)
        try:
            self.blob_client.get_account_information()
            print(self.service + ": Account information is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Account information is not retrieved. Error: ", e)
            return False
        

    # get blob properties with try except block
    def get_blob_properties(self, *args):
        args = list(args)

        try:
            self.blob_client.get_blob_properties()
            print(self.service + ": Blob properties are retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Blob properties are not retrieved. Error: ", e)
            return False
        


    # get blob tags with try except block
    def get_blob_tags(self, *args):
        args = list(args)

        try:
            self.blob_client.get_blob_tags()
            print(self.service + ": Blob tags are retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Blob tags are not retrieved. Error: ", e)
            return False
        

    # get block list with try except block
    def get_block_list(self, *args):
        args = list(args)
        # block list type
        if not len(args) > 0:
            args.append('committed')

        try:
            self.blob_client.get_block_list(args[0])
            print(self.service + ": Block list is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Block list is not retrieved. Error: ", e)
            return False
        
        
    # get page ranges with try except block
    def get_page_ranges(self, *args):
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
            blobclient.get_page_ranges(offset=args[0], length=args[1])
            print(self.service + ": Page ranges are retrieved.")
            return True
            
        except Exception as e:
            print(self.service + ": Page ranges are not retrieved. Error: ", e)
            return False
            

    # list page ranges diff with try except block
    def list_page_ranges_diff(self, *args):
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
            self.blob_client.list_page_ranges(previous_snapshot=args[0], offset=args[1], length=args[2])
            print(self.service + ": Page ranges diff is retrieved.")
            return True
        except Exception as e:
            print(self.service + ": Page ranges diff is not retrieved. Error: ", e)
            return False
        

    # query blob contents with try except block
    def query_blob(self, *args):
        args = list(args)
        # query expression
        if not len(args) > 0:
            args.append('SELECT _2 from BlobStorage')

        try:
            self.blob_client.query_blob(args[0])
            print(self.service + ": Blob contents are queried.")
            return True
        except Exception as e:
            print(self.service + ": Blob contents are not queried. Error: ", e)
            return False
        

        

    # set blob metadata with try except block
    def set_blob_metadata(self, *args):
        args = list(args)
        # metadata
        if not len(args) > 0:
            args.append({'metadata1': 'value1', 'metadata2': 'value2'})


        try:
            self.blob_client.set_blob_metadata(args[0])
            print(self.service + ": Blob metadata is set.")
            return True
        except Exception as e:
            print(self.service + ": Blob metadata is not set. Error: ", e)
            return False
        


    # set blob tags with try except block
    def set_blob_tags(self, *args):
        args = list(args)
        # tags
        if not len(args) > 0:
            args.append({'tag1': 'value1', 'tag2': 'value2'})

        try:
            self.blob_client.set_blob_tags(args[0])
            print(self.service + ": Blob tags are set.")
            return True
        except Exception as e:
            print(self.service + ": Blob tags are not set. Error: ", e)
            return False
        

    # set http headers with try except block
    def set_http_headers(self, *args):
        args = list(args)
        
        # content settings
        content_setting = ContentSettings(content_type='text/plain')

        try:
            self.blob_client.set_http_headers(content_setting)
            print(self.service + ": HTTP headers are set.")
            return True
        except Exception as e:
            print(self.service + ": HTTP headers are not set. Error: ", e)
            return False
        


    # set immutability policy with try except block
    def set_immutability_policy(self, *args):
        args = list(args)
        # immutability policy
        policy = ImmutabilityPolicy(expiry_time=datetime.datetime.utcnow() + datetime.timedelta(days=1), policy_mode='unlocked')

        try:
            self.blob_client.set_immutability_policy(policy)
            print(self.service + ": Immutability policy is set.")
            return True
        except Exception as e:
            print(self.service + ": Immutability policy is not set. Error: ", e)
            return False
        

    # set legal hold with try except block
    def set_legal_hold(self, *args):
        args = list(args)
        # legal hold
        if not len(args) > 0:
            args.append(random.choice([True, False]))

        try:
            self.blob_client.set_legal_hold(args[0])
            print(self.service + ": Legal hold is set.")
            return True
        except Exception as e:
            print(self.service + ": Legal hold is not set. Error: ", e)
            return False
        
    
    # skip premium page blob tier (with premium acc)


    # set tier with try except block
    def set_standard_blob_tier(self, *args):
        args = list(args)
        print(self.service + ": Setting blob tier...")
        # standard blob tier
        if not len(args) > 0:
            args.append(random.choice(['Hot', 'Cool', 'Archive']))

        try:
            self.blob_client.set_standard_blob_tier(args[0])
            print(self.service + ": Blob tier is set.")
            return True
        except Exception as e:
            print(self.service + ": Blob tier is not set. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # stage block from url with try except block
    def stage_block_from_url(self, *args):
        args = list(args)
        # block id
        if not len(args) > 0:
            args.append(b'0x8D')
        # source url
        if not len(args) > 1:
            args.append(f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob')
        # source offset
        if not len(args) > 2:
            args.append(0)
        # source length
        if not len(args) > 3:
            args.append(512)
        # source content md5
        if not len(args) > 4:
            args.append(b'0x8D')


        try:
            self.blob_client.stage_block_from_url(block_id=args[0], source_url=args[1], source_offset=args[2], source_length=args[3], source_content_md5=args[4])
            print(self.service + ": Block is staged from url.")
            return True
        except Exception as e:
            print(self.service + ": Block is not staged from url. Error: ", e)
            return False
        

    # stage block with try except block
    def stage_block(self, *args):
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
            self.blob_client.stage_block(args[0], args[1], length=args[2])
            print(self.service + ": Block is staged.")
            return True
        except Exception as e:
            print(self.service + ": Block is not staged. Error: ", e)
            return False
        

    # Not implemented in the emulator
    # undelete blob with try except block
    def undelete_blob(self, *args):
        args = list(args)
            
        try:
            self.blob_client.undelete_blob()
            print(self.service + ": Blob is undeleted.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not undeleted. Error: ", e)
            return False
        

    # upload blob from bytes with try except block
    def upload_blob_from_bytes(self, *args):
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
            self.blob_client.upload_blob(data=args[0], blob_type=args[1], length=args[2], metadata=args[3])
            print(self.service + ": Blob is uploaded from bytes.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not uploaded from bytes. Error: ", e)
            return False
        

    # upload blob from a url with try except block
    def upload_blob_from_url(self, *args):
        args = list(args)
        # source url
        if not len(args) > 0:
            args.append(f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob')
        try:    
            self.blob_client.upload_blob_from_url(args[0])
            print(self.service + ": Blob is uploaded from url.")
            return True
        except Exception as e:
            print(self.service + ": Blob is not uploaded from url. Error: ", e)
            return False


    # upload page
    def upload_page(self, *args):
        args = list(args)
        # data
        if not len(args) > 0:
            # open page.txt file
            with open('page', 'rb') as f:
                args.append(f.read())
        if not len(args) > 1:
            offset = 0

        try:
            self.blob_client.upload_page(args[0], args[1], length=len(args[0]))
            print(self.service + ": Page is uploaded.")
            return True
        except Exception as e:
            print(self.service + ": Page is not uploaded. Error: ", e)
            return False
    
    # Not implemented in the emulator
    # upload pages from url
    def upload_pages_from_url(self, *args):
        args = list(args)
        # source url
        if not len(args) > 0:
            args.append(f'https://{self.account_name}.blob.core.windows.net/mycontainer/myblob')
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
            self.blob_client.upload_pages_from_url(args[0], args[1], args[2], args[3])
            print(self.service + ": Pages are uploaded from url.")
            return True
        except Exception as e:
            print(self.service + ": Pages are not uploaded from url. Error: ", e)
            return False

    # destructor
    def __del__(self):
        
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
            

