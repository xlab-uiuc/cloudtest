import datetime
import json
import logging
import boto3, random


class S3Client:
    def __init__(self, emulator=True, bucket_name=None):

        if bucket_name is None:
            self.bucket_name = f'bucket{random.randint(1, 1000000000)}'
        else:
            self.bucket_name = bucket_name


        # connection string
        if not emulator:
            self.service = '**AWS**'
            self.region = 'us-east-2'
            AWS_PROFILE = 'aws'
            url = 'https://s3.us-east-2.amazonaws.com'
        else:
            self.service = '**EMULATOR**'
            self.region = 'us-west-1'
            AWS_PROFILE = 'localstack'
            url = 'http://localhost:4566'

        # set up session
        boto3.setup_default_session(profile_name=AWS_PROFILE)
        self.client = boto3.client('s3', endpoint_url=url, region_name=self.region)

        # create bucket
        self.client.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region})

    

    # abort multipart upload with try accept and args as none
    def s3_abort_multipart_upload(self, key=None, upload_id=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if upload_id is None:
            upload_id = f'{random.randint(1, 1000000)}'

        try:
            self.client.abort_multipart_upload(Bucket=self.bucket_name, Key=key, UploadId=upload_id)
            print(self.service, ': ' + f'Success -- Multipart upload aborted for {key} in {self.service} S3 bucket {self.bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error aborting multipart upload for {key} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e
        
    # check if can paginate with try accept and args as none
    def s3_can_paginate(self, operation_name=None):
        if operation_name is None:
            operation_name = "list_buckets"

        try:
            self.client.can_paginate(operation_name)
            print(self.service, ': ' + f'Success -- Operation {operation_name} can be paginated')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error checking if {self.service} S3 client can paginate {operation_name}: {e}')
            return False, e
        
    
    # complete multipart upload with try accept and args as none
    def s3_complete_multipart_upload(self, key=None, upload_id=None, parts=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if upload_id is None:
            res = self.s3_create_multipart_upload(key)
            if res == False:
                print(self.service, ': ' + f'Fail -- Error creating multipart upload for {key} in {self.service} S3 bucket {self.bucket_name}: {e}')
                return False, e
            upload_id = res[1]
            res = self.s3_upload_part(key, upload_id)
            if res == False:
                print(self.service, ': ' + f'Fail -- Error uploading part for {key} in {self.service} S3 bucket {self.bucket_name}: {e}')
                return False, e
            part = res[1]

        if parts is None:
            parts = [
            {
                'ETag': f'"{part}"',
                'PartNumber': 1,
            }]

        try:
            self.client.complete_multipart_upload(Bucket=self.bucket_name, Key=key, UploadId='', MultipartUpload={'Parts': parts})
            print(self.service, ': ' + f'Success -- Multipart upload completed for {key} in {self.service} S3 bucket {self.bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error completing multipart upload for {key} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e


    # copy with try accept and args as none
    def s3_copy(self, key=None, copy_source=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if copy_source is None:
            copy_source = {'Bucket': self.bucket_name, 'Key': key}

        self.s3_put_object(key=key, body='test213')
        new_buc = f'test{random.randint(1, 1000000000)}'
        self.s3_create_bucket(bucket_name=new_buc)

        try:
            self.client.copy(CopySource=copy_source, Bucket=new_buc, Key=key)
            print(self.service, ': ' + f'Success -- Copied {copy_source} to {key} in {self.service} S3 bucket {new_buc}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error copying {copy_source} to {key} in {self.service} S3 bucket {new_buc}: {e}')
            return False, e
        

    # create bucket with try accept and args as none
    def s3_create_bucket(self, bucket_name=None, lock=False):
        if bucket_name is None:
            bucket_name = f'bucket{random.randint(1, 1000000000)}'

        try:
            if lock:
                self.client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region}, ObjectLockEnabledForBucket=True)
            else:
                self.client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region})
            print(self.service, ': ' + f'Success -- Created bucket {bucket_name} in {self.service} S3')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket {bucket_name} in {self.service} S3: {e}')
            return False, e


    # create multipart upload with try accept and args as none
    def s3_create_multipart_upload(self, key=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        try:
            resp = self.client.create_multipart_upload(Bucket=self.bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Multipart upload created for {key} in {self.service} S3 bucket {self.bucket_name}')
            return True, resp['UploadId']
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating multipart upload for {key} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e

    # delete bucket with try accept and args as none
    def s3_delete_bucket(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = f'test{random.randint(1, 1000000000)}'
            # self.s3_create_bucket(bucket_name=bucket_name)

        try:
            self.client.delete_bucket(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket {bucket_name} deleted')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket {bucket_name}: {e}')
            return False, e
        
    # delete bucket analytics configuration with try accept and args as none
    def s3_delete_bucket_analytics_configuration(self, bucket_name=None, id=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = f'test{random.randint(1, 1000000000)}'
            self.s3_put_bucket_analytics_configuration(bucket_name=bucket_name, id=id)

        try:
            self.client.delete_bucket_analytics_configuration(Bucket=bucket_name, Id=id)
            print(self.service, ': ' + f'Success -- Bucket analytics configuration {id} deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket analytics configuration {id} from bucket {bucket_name}: {e}')
            return False, e

    # delete bucket cors with try accept and args as none
    def s3_delete_bucket_cors(self, bucket_name=None):
        self.s3_put_bucket_cors()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_bucket_cors(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket cors deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket cors from bucket {bucket_name}: {e}')
            return False, e

    # delete bucket encryption with try accept and args as none
    def s3_delete_bucket_encryption(self, bucket_name=None):
        self.s3_put_bucket_encryption()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_bucket_encryption(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket encryption deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket encryption from bucket {bucket_name}: {e}')
            return False, e

    # delete intellegent tiering configuration with try accept and args as none
    def s3_delete_bucket_intelligent_tiering_configuration(self, bucket_name=None, id=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = f'test{random.randint(1, 1000000000)}'
            self.s3_put_bucket_intelligent_tiering_configuration(bucket_name=bucket_name, id=id)

        try:
            self.client.delete_bucket_intelligent_tiering_configuration(Bucket=bucket_name, Id=id)
            print(self.service, ': ' + f'Success -- Bucket intelligent tiering configuration {id} deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket intelligent tiering configuration {id} from bucket {bucket_name}: {e}')
            return False, e

    # delete bucket inventory configuration with try accept and args as none
    def s3_delete_bucket_inventory_configuration(self, bucket_name=None, id=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = f'test{random.randint(1, 1000000000)}'
            # self.s3_put_bucket_inventory_configuration(bucket_name=bucket_name, id=id)

        try:
            self.client.delete_bucket_inventory_configuration(Bucket=bucket_name, Id=id)
            print(self.service, ': ' + f'Success -- Bucket inventory configuration {id} deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket inventory configuration {id} from bucket {bucket_name}: {e}')
            return False, e

    # delete bucket lifecycle with try accept and args as none
    def s3_delete_bucket_lifecycle(self, bucket_name=None):
        self.s3_put_bucket_lifecycle()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_bucket_lifecycle(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket lifecycle deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket lifecycle from bucket {bucket_name}: {e}')
            return False, e
        

    # delete bucket metrics configuration with try accept and args as none
    def s3_delete_bucket_metrics_configuration(self, bucket_name=None, id=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = f'test{random.randint(1, 1000000000)}'
            self.s3_put_bucket_metrics_configuration(bucket_name=bucket_name, id=id)

        try:
            self.client.delete_bucket_metrics_configuration(Bucket=bucket_name, Id=id)
            print(self.service, ': ' + f'Success -- Bucket metrics configuration {id} deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket metrics configuration {id} from bucket {bucket_name}: {e}')
            return False, e

    # delete ownership controls with try accept and args as none
    def s3_delete_bucket_ownership_controls(self, bucket_name=None):
        self.s3_put_bucket_ownership_controls()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_bucket_ownership_controls(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket ownership controls deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket ownership controls from bucket {bucket_name}: {e}')
            return False, e

    # delete bucket policy with try accept and args as none
    def s3_delete_bucket_policy(self, bucket_name=None):
        self.s3_put_bucket_policy()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_bucket_policy(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket policy deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket policy from bucket {bucket_name}: {e}')
            return False, e
        

    # delete bucket replication with try accept and args as none
    def s3_delete_bucket_replication(self, bucket_name=None):
        self.s3_put_bucket_replication()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_bucket_replication(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket replication deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket replication from bucket {bucket_name}: {e}')
            return False, e
        

    # delete bucket tagging with try accept and args as none
    def s3_delete_bucket_tagging(self, bucket_name=None):
        self.s3_put_bucket_tagging()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_bucket_tagging(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket tagging deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket tagging from bucket {bucket_name}: {e}')
            return False, e
        

    # delete bucket website with try accept and args as none
    def s3_delete_bucket_website(self, bucket_name=None):
        self.s3_put_bucket_website()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_bucket_website(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket website deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket website from bucket {bucket_name}: {e}')
            return False, e
        

    # delete object with try accept and args as none
    def s3_delete_object(self, bucket_name=None, key=None):
        # comment this if you want to delete objects for deleting all the objects
        self.s3_put_object()
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        try:
            self.client.delete_object(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object {key} deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting object {key} from bucket {bucket_name}: {e}')
            return False, e
        

    # delete object tagging with try accept and args as none
    def s3_delete_object_tagging(self, bucket_name=None, key=None):
        
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        self.s3_put_object_tagging(key=key)

        try:
            self.client.delete_object_tagging(Bucket=bucket_name, Key=key, BypassGovernanceRetention=True)
            print(self.service, ': ' + f'Success -- Object tagging deleted from object {key} in bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting object tagging from object {key} in bucket {bucket_name}: {e}')
            return False, e

    # delete objects with try accept and args as none
    def s3_delete_objects(self, bucket_name=None, key=None):
        
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key1 = f'{random.randint(1, 1000000)}'
            self.s3_put_object(key=key1)
            key2 = f'{random.randint(1, 1000000)}'
            self.s3_put_object(key=key2)

        try:
            self.client.delete_objects(Bucket=bucket_name, Delete={'Objects': [{'Key': key1}, {'Key': key2}]})
            print(self.service, ': ' + f'Success -- Objects deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting objects from bucket {bucket_name}: {e}')
            return False, e

    # delete public access block with try accept and args as none
    def s3_delete_public_access_block(self, bucket_name=None):
        self.s3_put_public_access_block()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.delete_public_access_block(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Public access block deleted from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting public access block from bucket {bucket_name}: {e}')
            return False, e
        


    # download file with try accept and args as none
    def s3_download_file(self, bucket_name=None, key=None, filename=None):
        
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if filename is None:
            filename = f'{random.randint(1, 1000000)}'

        self.s3_put_object(key=key)

        try:
            self.client.download_file(Bucket=bucket_name, Key=key, Filename=filename)
            print(self.service, ': ' + f'Success -- File {filename} downloaded from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error downloading file {filename} from bucket {bucket_name}: {e}')
            return False, e
        

    # download fileobj with try accept and args as none
    def s3_download_fileobj(self, bucket_name=None, key=None, fileobj=None):
       
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object(key=key)

        try:
            with open('filename', 'wb') as data:
                self.client.download_fileobj(Bucket=bucket_name, Key=key, Fileobj=data)
            print(self.service, ': ' + f'Success -- Fileobj {fileobj} downloaded from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error downloading fileobj {fileobj} from bucket {bucket_name}: {e}')
            return False, e


    # generate presigned post with try accept and args as none
    def s3_generate_presigned_post(self, bucket_name=None, key=None, fields=None, conditions=None, expiration=None):
            
            if bucket_name is None:
                bucket_name = self.bucket_name
            if key is None:
                key = f'{random.randint(1, 1000000)}'
            if fields is None:
                fields = None
            if conditions is None:
                conditions = None
            if expiration is None:
                expiration = 3600
    
            try:
                self.client.generate_presigned_post(Bucket=bucket_name, Key=key, Fields=fields, Conditions=conditions, ExpiresIn=expiration)
                print(self.service, ': ' + f'Success -- Presigned post generated for bucket {bucket_name}')
                return True, ""
            except Exception as e:
                print(self.service, ': ' + f'Fail -- Error generating presigned post for bucket {bucket_name}: {e}')
                return False, e
            
    # generate presigned url with try accept and args as none
    def s3_generate_presigned_url(self, bucket_name=None, key=None, expiration=None, method=None):
                
            if bucket_name is None:
                bucket_name = self.bucket_name
            if key is None:
                key = f'{random.randint(1, 1000000)}'
            if expiration is None:
                expiration = 3600
            if method is None:
                method = 'get_object'
    
            try:
                self.client.generate_presigned_url(ClientMethod=method, Params={'Bucket': bucket_name, 'Key': key}, ExpiresIn=expiration)
                print(self.service, ': ' + f'Success -- Presigned url generated for bucket {bucket_name}')
                return True, ""
            except Exception as e:
                print(self.service, ': ' + f'Fail -- Error generating presigned url for bucket {bucket_name}: {e}')
                return False, e

    # get bucket accelerate configuration with try accept and args as none
    def s3_get_bucket_accelerate_configuration(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_accelerate_configuration(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Accelerate configuration retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving accelerate configuration from bucket {bucket_name}: {e}')
            return False, e
        
    # get bucket acl with try accept and args as none
    def s3_get_bucket_acl(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_acl(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- ACL retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving ACL from bucket {bucket_name}: {e}')
            return False, e

    # get bucket analytics configuration with try accept and args as none
    def s3_get_bucket_analytics_configuration(self, bucket_name=None, id=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = 'test'

        try:
            self.client.get_bucket_analytics_configuration(Bucket=bucket_name, Id=id)
            print(self.service, ': ' + f'Success -- Analytics configuration retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving analytics configuration from bucket {bucket_name}: {e}')
            return False, e

    # get bucket cors with try accept and args as none
    def s3_get_bucket_cors(self, bucket_name=None):
        self.s3_put_bucket_cors()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_cors(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- CORS retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving CORS from bucket {bucket_name}: {e}')
            return False, e

    # get bucket encryption with try accept and args as none
    def s3_get_bucket_encryption(self, bucket_name=None):
        self.s3_put_bucket_encryption()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_encryption(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Encryption retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving encryption from bucket {bucket_name}: {e}')
            return False, e
        
    # get intellegent tiering configuration with try accept and args as none
    def s3_get_bucket_intelligent_tiering_configuration(self, bucket_name=None, id=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = 'test'

        try:
            resp = self.client.get_bucket_intelligent_tiering_configuration(Bucket=bucket_name, Id=id)
            print(self.service, ': ' + f'Success -- Intelligent tiering configuration retrieved from bucket {bucket_name}')
            print(resp)
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving intelligent tiering configuration from bucket {bucket_name}: {e}')
            return False, e

    # get bucket inventory configuration with try accept and args as none
    def s3_get_bucket_inventory_configuration(self, bucket_name=None, id=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = 'test'

        try:
            self.client.get_bucket_inventory_configuration(Bucket=bucket_name, Id=id)
            print(self.service, ': ' + f'Success -- Inventory configuration retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving inventory configuration from bucket {bucket_name}: {e}')
            return False, e


    # get bucket lifecycle with try accept and args as none
    def s3_get_bucket_lifecycle(self, bucket_name=None):
        self.s3_put_bucket_lifecycle()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_lifecycle(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Lifecycle retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving lifecycle from bucket {bucket_name}: {e}')
            return False, e


    # get bucket lifecycle configuration with try accept and args as none
    def s3_get_bucket_lifecycle_configuration(self, bucket_name=None):
        self.s3_put_bucket_lifecycle()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Lifecycle configuration retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving lifecycle configuration from bucket {bucket_name}: {e}')
            return False, e

    # get bucket location with try accept and args as none
    def s3_get_bucket_location(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_location(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Location retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving location from bucket {bucket_name}: {e}')
            return False, e


    # get bucket logging with try accept and args as none
    def s3_get_bucket_logging(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_logging(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Logging retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving logging from bucket {bucket_name}: {e}')
            return False, e

    # get bucket metrics configuration with try accept and args as none
    def s3_get_bucket_metrics_configuration(self, bucket_name=None, id=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = 'test'

        try:
            self.client.get_bucket_metrics_configuration(Bucket=bucket_name, Id=id)
            print(self.service, ': ' + f'Success -- Metrics configuration retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving metrics configuration from bucket {bucket_name}: {e}')
            return False, e

    # get bucket notification with try accept and args as none
    def s3_get_bucket_notification(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_notification(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Notification retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving notification from bucket {bucket_name}: {e}')
            return False, e

    # get bucket notification configuration with try accept and args as none
    def s3_get_bucket_notification_configuration(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_notification_configuration(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Notification configuration retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving notification configuration from bucket {bucket_name}: {e}')
            return False, e
        
    # gte ownership controls with try accept and args as none
    def s3_get_bucket_ownership_controls(self, bucket_name=None):
        self.s3_put_bucket_ownership_controls()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_ownership_controls(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Ownership controls retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving ownership controls from bucket {bucket_name}: {e}')
            return False, e

    # get bucket policy with try accept and args as none
    def s3_get_bucket_policy(self, bucket_name=None):
        self.s3_put_bucket_policy()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_policy(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Policy retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving policy from bucket {bucket_name}: {e}')
            return False, e
        
    # get bucket policy status with try accept and args as none
    def s3_get_bucket_policy_status(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_policy_status(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Policy status retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving policy status from bucket {bucket_name}: {e}')
            return False, e
        

    # get bucket replication with try accept and args as none
    def s3_get_bucket_replication(self, bucket_name=None):
        self.s3_put_bucket_replication()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_replication(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Replication retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving replication from bucket {bucket_name}: {e}')
            return False, e

    # get bucket request payment with try accept and args as none
    def s3_get_bucket_request_payment(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_request_payment(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Request payment retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving request payment from bucket {bucket_name}: {e}')
            return False, e


    # get bucket tagging with try accept and args as none
    def s3_get_bucket_tagging(self, bucket_name=None):
        self.s3_put_bucket_tagging()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_tagging(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Tagging retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving tagging from bucket {bucket_name}: {e}')
            return False, e
        

    # get bucket versioning with try accept and args as none
    def s3_get_bucket_versioning(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_versioning(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Versioning retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving versioning from bucket {bucket_name}: {e}')
            return False, e


    # get bucket website with try accept and args as none
    def s3_get_bucket_website(self, bucket_name=None):
        self.s3_put_bucket_website()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_bucket_website(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Website retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving website from bucket {bucket_name}: {e}')
            return False, e
        

    # get object with try accept and args as none
    def s3_get_object(self, bucket_name=None, key=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object(key=key)

        try:
            self.client.get_object(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object {key} retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object {key} from bucket {bucket_name}: {e}')
            return False, e


    # get object acl with try accept and args as none
    def s3_get_object_acl(self, bucket_name=None, key=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object(key=key)

        try:
            self.client.get_object_acl(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object ACL {key} retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object ACL {key} from bucket {bucket_name}: {e}')
            return False, e

    # get attributes of object with try accept and args as none
    def s3_get_object_attributes(self, bucket_name=None, key=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object(key=key)

        try:
            self.client.head_object(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object attributes {key} retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object attributes {key} from bucket {bucket_name}: {e}')
            return False, e

    # get object legal hold with try accept and args as none
    def s3_get_object_legal_hold(self, bucket_name=None, key=None):
        if bucket_name is None:
            bucket_name = f'{random.randint(1, 1000000)}'
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object_legal_hold(key=key, bucket_name=bucket_name)

        try:
            self.client.get_object_legal_hold(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object legal hold {key} retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object legal hold {key} from bucket {bucket_name}: {e}')
            return False, e
        
    # get object lock configuration with try accept and args as none
    def s3_get_object_lock_configuration(self, bucket_name=None):
        
        if bucket_name is None:
            bucket_name = f'{random.randint(1, 1000000)}'

        self.s3_put_object_lock_configuration(bucket_name=bucket_name)

        try:
            self.client.get_object_lock_configuration(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Object lock configuration retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object lock configuration from bucket {bucket_name}: {e}')
            return False, e
        

    # get object retention with try accept and args as none
    def s3_get_object_retention(self, bucket_name=None, key=None):
        if bucket_name is None:
            bucket_name = f'{random.randint(1, 1000000)}'
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object_legal_hold(key=key, bucket_name=bucket_name)

        try:
            self.client.get_object_retention(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object retention {key} retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object retention {key} from bucket {bucket_name}: {e}')
            return False, e
        

    # get object tagging with try accept and args as none
    def s3_get_object_tagging(self, bucket_name=None, key=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object(key=key)

        try:
            self.client.get_object_tagging(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object tagging {key} retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object tagging {key} from bucket {bucket_name}: {e}')
            return False, e


    # get object torrent with try accept and args as none
    def s3_get_object_torrent(self, bucket_name=None, key=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object(key=key)

        try:
            self.client.get_object_torrent(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object torrent {key} retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object torrent {key} from bucket {bucket_name}: {e}')
            return False, e
        

    # !!ignore
    # get paginator with try accept and args as none
    def s3_get_paginator(self):

        try:
            self.client.get_paginator('list_object_versions')
            print(self.service, ': ' + f'Success -- Paginator retrieved')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving paginator: {e}')
            return False, e
        

    # get public access block with try accept and args as none
    def s3_get_public_access_block(self, bucket_name=None):
        self.s3_put_public_access_block()
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.get_public_access_block(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Public access block retrieved from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving public access block from bucket {bucket_name}: {e}')
            return False, e

    # # !!ignore
    # # get waiters with try accept and args as none
    # def s3_get_waiter(self, bucket_name=None):
    #     if bucket_name is None:
    #         bucket_name = self.bucket_name

    #     try:
    #         self.client.get_waiter(bucket_name)
    #         print(self.service, ': ' + f'Success -- Waiter retrieved from bucket {bucket_name}')
    #         return True, ""
    #     except Exception as e:
    #         print(self.service, ': ' + f'Fail -- Error retrieving waiter from bucket {bucket_name}: {e}')
    #         return False, e
        

    # head bucket with try accept and args as none
    def s3_head_bucket(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.head_bucket(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket {bucket_name} head')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error head bucket {bucket_name}: {e}')
            return False, e
        
    # head object with try accept and args as none
    def s3_head_object(self, bucket_name=None, key=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if key is None:
            key = f'{random.randint(1, 1000000)}'

        self.s3_put_object(key=key)

        try:
            self.client.head_object(Bucket=bucket_name, Key=key)
            print(self.service, ': ' + f'Success -- Object {key} head from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error head object {key} from bucket {bucket_name}: {e}')
            return False, e


    # list bucket analytics configurations with try accept and args as none
    def s3_list_bucket_analytics_configurations(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.list_bucket_analytics_configurations(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket analytics configurations listed from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing bucket analytics configurations from bucket {bucket_name}: {e}')
            return False, e

    # list bucket intelligent tiering configuration with try accept and args as none
    def s3_list_bucket_intelligent_tiering_configurations(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.list_bucket_intelligent_tiering_configurations(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket intelligent tiering configurations listed from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing bucket intelligent tiering configurations from bucket {bucket_name}: {e}')
            return False, e

    # list bucket inventory configurations with try accept and args as none
    def s3_list_bucket_inventory_configurations(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.list_bucket_inventory_configurations(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket inventory configurations listed from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing bucket inventory configurations from bucket {bucket_name}: {e}')
            return False, e


    # list bucket metrics configurations with try accept and args as none
    def s3_list_bucket_metrics_configurations(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.list_bucket_metrics_configurations(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Bucket metrics configurations listed from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing bucket metrics configurations from bucket {bucket_name}: {e}')
            return False, e

    # list multipart uploads with try accept and args as none
    def s3_list_multipart_uploads(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.list_multipart_uploads(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Multipart uploads listed from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing multipart uploads from bucket {bucket_name}: {e}')
            return False, e

    # list object versions with try accept and args as none
    def s3_list_object_versions(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.list_object_versions(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Object versions listed from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing object versions from bucket {bucket_name}: {e}')
            return False, e
        
    # list objects with try accept and args as none
    def s3_list_objects(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.list_objects(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Objects listed from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing objects from bucket {bucket_name}: {e}')
            return False, e


    # list objects v2 with try accept and args as none
    def s3_list_objects_v2(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            self.client.list_objects_v2(Bucket=bucket_name)
            print(self.service, ': ' + f'Success -- Objects v2 listed from bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing objects v2 from bucket {bucket_name}: {e}')
            return False, e
        


    # !!try again
    # list parts with try accept and args as none


    # list buckets with try accept and args as none
    def s3_list_buckets(self):
        try:
            res = self.client.list_buckets()
            print(self.service, ': ' + 'Success -- Buckets listed')
            return True, res
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing buckets: {e}')
            return False, e

    # put bucket acelerate configuration with try accept and args as none
    def s3_put_bucket_accelerate_configuration(self, bucket_name=None, accelerate_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if accelerate_configuration is None:
            accelerate_configuration = {'Status': 'Enabled'}

        try:
            self.client.put_bucket_accelerate_configuration(Bucket=bucket_name, AccelerateConfiguration=accelerate_configuration)
            print(self.service, ': ' + f'Success -- Bucket accelerate configuration added to bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error adding bucket accelerate configuration to bucket {bucket_name}: {e}')
            return False, e

    # put bucket acl with try accept and args as none
    def s3_put_bucket_acl(self, bucket_name=None, acl=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if acl is None:
            acl = 'public-read'

        try:
            self.client.put_bucket_acl(Bucket=bucket_name, ACL=acl)
            print(self.service, ': ' + f'Success -- Bucket ACL added to bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error adding bucket ACL to bucket {bucket_name}: {e}')
            return False, e


    # put analytics configuration with try accept and args as none
    def s3_put_bucket_analytics_configuration(self, bucket_name=None, id=None, analytics_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = f'test{random.randint(1, 1000000000)}'
        if analytics_configuration is None:
            analytics_configuration = {
                'Id': id,
                'StorageClassAnalysis': {
                    'DataExport': {
                        'OutputSchemaVersion': 'V_1',
                        'Destination': {
                            'S3BucketDestination': {
                                'Bucket': f'arn:aws:s3:::{bucket_name}',
                                'Format': 'CSV'
                            }
                        }
                    }
                }
            }

        try:
            self.client.put_bucket_analytics_configuration(Bucket=bucket_name, Id=id, AnalyticsConfiguration=analytics_configuration)
            print(self.service, ': ' + f'Success -- Bucket analytics configuration {id} created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket analytics configuration {id} for bucket {bucket_name}: {e}')
            return False, e


    # put bucket cors with try accept and args as none
    def s3_put_bucket_cors(self, bucket_name=None, cors_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if cors_configuration is None:
            cors_configuration = {
                'CORSRules': [
                    {
                        'AllowedHeaders': [
                            '*',
                        ],
                        'AllowedMethods': [
                            'GET',
                            'PUT',
                        ],
                        'AllowedOrigins': [
                            '*',
                        ],
                        'ExposeHeaders': [
                            'x-amz-server-side-encryption',
                            'x-amz-request-id',
                            'x-amz-id-2',
                        ],
                        'MaxAgeSeconds': 3000
                    },
                ]
            }

        try:
            self.client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)
            print(self.service, ': ' + f'Success -- Bucket cors created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket cors for bucket {bucket_name}: {e}')
            return False, e

    # put bucket encryption with try accept and args as none
    def s3_put_bucket_encryption(self, bucket_name=None, server_side_encryption_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if server_side_encryption_configuration is None:
            server_side_encryption_configuration = {
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    },
                ]
            }

        try:
            self.client.put_bucket_encryption(Bucket=bucket_name, ServerSideEncryptionConfiguration=server_side_encryption_configuration)
            print(self.service, ': ' + f'Success -- Bucket encryption created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket encryption for bucket {bucket_name}: {e}')
            return False, e


    # put intellegent tiering configuration with try accept and args as none
    def s3_put_bucket_intelligent_tiering_configuration(self, bucket_name=None, id=None, intelligent_tiering_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = f'test{random.randint(1, 1000000000)}'
        if intelligent_tiering_configuration is None:
            intelligent_tiering_configuration = {
                'Id': id,
                'Filter': {
                    'Prefix': 'test'
                },
                'Status': 'Enabled',
                'Tierings': [
                    {
                        'Days': 91,
                        'AccessTier': 'ARCHIVE_ACCESS'
                    },
                ]
            }

        try:
            self.client.put_bucket_intelligent_tiering_configuration(Bucket=bucket_name, Id=id, IntelligentTieringConfiguration=intelligent_tiering_configuration)
            print(self.service, ': ' + f'Success -- Bucket intelligent tiering configuration {id} created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket intelligent tiering configuration {id} for bucket {bucket_name}: {e}')
            return False, e


    # put bucket inventory configuration with try accept and args as none
    def s3_put_bucket_inventory_configuration(self, bucket_name=None, id=None, inventory_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = f'test{random.randint(1, 1000000000)}'
        if inventory_configuration is None:
            inventory_configuration = {
                'Id': id,
                'IsEnabled': True,
                'Destination': {
                    'S3BucketDestination': {
                        'Bucket': f'arn:aws:s3:::{bucket_name}',
                        'Format': 'CSV'
                    }
                },
                'IncludedObjectVersions': 'All',
                'OptionalFields': [
                    'Size',
                ],
                'Schedule': {
                    'Frequency': 'Daily'
                }
            }

        try:
            self.client.put_bucket_inventory_configuration(Bucket=bucket_name, Id=id, InventoryConfiguration=inventory_configuration)
            print(self.service, ': ' + f'Success -- Bucket inventory configuration {id} created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket inventory configuration {id} for bucket {bucket_name}: {e}')
            return False, e


    # put bucket lifecycle configuration with try accept and args as none
    def s3_put_bucket_lifecycle(self, bucket_name=None, lifecycle_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if lifecycle_configuration is None:
            lifecycle_configuration = {
                'Rules': [
                    {
                        'Expiration': {
                            'Days': 365
                        },
                        'Filter': {
                            'Prefix': 'test'
                        },
                        'ID': 'test',
                        'Status': 'Enabled'
                    },
                ]
            }

        try:
            self.client.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=lifecycle_configuration)
            print(self.service, ': ' + f'Success -- Bucket lifecycle configuration created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket lifecycle configuration for bucket {bucket_name}: {e}')
            return False, e


    # put bucket logging with try accept and args as none
    def s3_put_bucket_logging(self, bucket_name=None, logging_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if logging_configuration is None:
            logging_configuration = {
                'LoggingEnabled': {
                    'TargetBucket': bucket_name,
                    'TargetPrefix': 'test'
                }
            }

        try:
            res = self.client.put_bucket_logging(Bucket=bucket_name, BucketLoggingStatus=logging_configuration)
            print(self.service, ': ' + f'Success -- Bucket logging configuration created for bucket {bucket_name}')
            print(res)

            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket logging configuration for bucket {bucket_name}: {e}')
            return False, e



    # put bucket metrics configuration with try accept and args as none
    def s3_put_bucket_metrics_configuration(self, bucket_name=None, id=None, metrics_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if id is None:
            id = f'test{random.randint(1, 1000000000)}'
        if metrics_configuration is None:
            metrics_configuration = {
                'Id': id,
                'Filter': {
                    'Prefix': 'test'
                }
            }

        try:
            self.client.put_bucket_metrics_configuration(Bucket=bucket_name, Id=id, MetricsConfiguration=metrics_configuration)
            print(self.service, ': ' + f'Success -- Bucket metrics configuration {id} created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket metrics configuration {id} for bucket {bucket_name}: {e}')
            return False, e

    # put ownership controls with try accept and args as none
    def s3_put_bucket_ownership_controls(self, bucket_name=None, ownership_controls=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if ownership_controls is None:
            ownership_controls = {
                'Rules': [
                    {
                        'ObjectOwnership': 'BucketOwnerPreferred'
                    },
                ]
            }

        try:
            self.client.put_bucket_ownership_controls(Bucket=bucket_name, OwnershipControls=ownership_controls)
            print(self.service, ': ' + f'Success -- Bucket ownership controls created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket ownership controls for bucket {bucket_name}: {e}')
            return False, e

    # !!ignore
    # put bucket policy with try accept and args as none
    def s3_put_bucket_policy(self, bucket_name=None, policy=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if policy is None:
            policy = {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Sid': 'AddPerm',
                        'Effect': 'Allow',
                        'Principal': '*',
                        'Action': ['s3:GetObject'],
                        'Resource': f'arn:aws:s3:::{bucket_name}/*'
                    },
                ]
            }

        try:
            self.client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
            print(self.service, ': ' + f'Success -- Bucket policy created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket policy for bucket {bucket_name}: {e}')
            return False, e


    # put bucket replication with try accept and args as none
    def s3_put_bucket_replication(self, bucket_name=None, replication_configuration=None):
        
        # enable bucket versioning
        self.s3_put_bucket_versioning()

        if bucket_name is None:
            bucket_name = f'test{random.randint(1, 1000000000)}'
            self.s3_create_bucket(bucket_name)
            self.s3_put_bucket_versioning(bucket_name=bucket_name)

        if replication_configuration is None:
            replication_configuration = {
                'Role': 'arn:aws:iam::123456789012:role/replication-role',
                'Rules': [
                    {
                        'ID': 'test',
                        'Prefix': 'test',
                        'Status': 'Enabled',
                        'Destination': {
                            'Bucket': f'arn:aws:s3:::{bucket_name}'
                        }
                    },
                ]
            }

        try:
            self.client.put_bucket_replication(Bucket=self.bucket_name, ReplicationConfiguration=replication_configuration)
            print(self.service, ': ' + f'Success -- Bucket replication configuration created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket replication configuration for bucket {bucket_name}: {e}')
            return False, e
        

    # put bucket tagging with try accept and args as none
    def s3_put_bucket_tagging(self, bucket_name=None, tagging=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if tagging is None:
            tagging = {
                'TagSet': [
                    {
                        'Key': 'test',
                        'Value': 'test'
                    },
                ]
            }

        try:
            self.client.put_bucket_tagging(Bucket=bucket_name, Tagging=tagging)
            print(self.service, ': ' + f'Success -- Bucket tagging created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket tagging for bucket {bucket_name}: {e}')
            return False, e


    # put bucket versioning with try accept and args as none
    def s3_put_bucket_versioning(self, bucket_name=None, versioning_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if versioning_configuration is None:
            versioning_configuration = {
                'Status': 'Enabled',
                'MFADelete': 'Disabled',
            }

        try:
            self.client.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration=versioning_configuration)
            print(self.service, ': ' + f'Success -- Bucket versioning configuration created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket versioning configuration for bucket {bucket_name}: {e}')
            return False, e


    # put bucket website with try accept and args as none
    def s3_put_bucket_website(self, bucket_name=None, website_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if website_configuration is None:
            website_configuration = {
                'ErrorDocument': {
                    'Key': 'error.html'
                },
                'IndexDocument': {
                    'Suffix': 'index.html'
                }
            }

        try:
            self.client.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=website_configuration)
            print(self.service, ': ' + f'Success -- Bucket website configuration created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket website configuration for bucket {bucket_name}: {e}')
            return False, e
        
    # put object with try accept and args as none
    def s3_put_object(self, bucket_name=None, key=None, body=None, storage_class=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if body is None:
            body = 'test'
        if bucket_name is None:
            bucket_name = self.bucket_name
        if storage_class is None:
            storage_class = 'STANDARD'

        try:
            self.client.put_object(Bucket=bucket_name, Key=key, Body=body, StorageClass=storage_class)
            print(self.service, ': ' + f'Success -- Put object {key} in {self.service} S3 bucket {self.bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error putting object {key} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e


    # put object acl with try accept and args as none
    def s3_put_object_acl(self, key=None, acl=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if acl is None:
            acl = 'public-read'
        self.s3_put_object(key=key)

        try:
            self.client.put_object_acl(Bucket=self.bucket_name, Key=key, ACL=acl)
            print(self.service, ': ' + f'Success -- Object ACL created for object {key}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object ACL for object {key}: {e}')
            return False, e


    # put object legal hold with try accept and args as none
    def s3_put_object_legal_hold(self, key=None, legal_hold=None, bucket_name=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'


        if legal_hold is None:
            legal_hold = {
                    'Status': 'OFF'
                }
            
        if bucket_name is None:
            bucket_name = f'bucket{random.randint(1, 1000000)}'

        # comment for bult deletion
        self.s3_put_object_lock_configuration(bucket_name=bucket_name)
        self.s3_put_object(key=key, bucket_name=bucket_name)

        try:
            self.client.put_object_legal_hold(Bucket=bucket_name, Key=key, LegalHold=legal_hold)
            print(self.service, ': ' + f'Success -- Object legal hold created for object {key}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object legal hold for object {key}: {e}')
            return False, e

    # put object lock configuration with try accept and args as none
    def s3_put_object_lock_configuration(self, bucket_name=None, object_lock_configuration=None):
        
        if bucket_name is None:
            bucket_name = f'bucket{random.randint(1, 1000000)}'
        
        self.s3_create_bucket(bucket_name=bucket_name, lock=True)

        if object_lock_configuration is None:
            object_lock_configuration = {
                'ObjectLockEnabled': 'Enabled',
                'Rule': {
                    'DefaultRetention': {
                        'Days': 1,
                        'Mode': 'GOVERNANCE'
                    }
                }
            }

        try:
            self.client.put_object_lock_configuration(Bucket=bucket_name, ObjectLockConfiguration=object_lock_configuration)
            print(self.service, ': ' + f'Success -- Object lock configuration created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object lock configuration for bucket {bucket_name}: {e}')
            return False, e


    # put object retention with try accept and args as none
    def s3_put_object_retention(self, key=None, retention=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'


        if retention is None:
            retention = {
                    'Mode': 'GOVERNANCE',
                    'RetainUntilDate': datetime.datetime.today() + datetime.timedelta(days=1)
                }
        bucket_name = f'bucket{random.randint(1, 1000000)}'
        self.s3_put_object_lock_configuration(bucket_name=bucket_name)
        self.s3_put_object(key=key, bucket_name=bucket_name)


        try:
            self.client.put_object_retention(Bucket=bucket_name, Key=key, Retention=retention)
            print(self.service, ': ' + f'Success -- Object retention created for object {key}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object retention for object {key}: {e}')
            return False, e

    # put object tagging with try accept and args as none
    def s3_put_object_tagging(self, key=None, tagging=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if tagging is None:
            tagging = {
                'TagSet': [
                    {
                        'Key': 'test',
                        'Value': 'test'
                    },
                ]
            }
        self.s3_put_object(key=key)

        try:
            self.client.put_object_tagging(Bucket=self.bucket_name, Key=key, Tagging=tagging)
            print(self.service, ': ' + f'Success -- Object tagging created for object {key}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object tagging for object {key}: {e}')
            return False, e

    # put public access block with try accept and args as none
    def s3_put_public_access_block(self, bucket_name=None, public_access_block_configuration=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        if public_access_block_configuration is None:
            public_access_block_configuration = {
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }

        try:
            self.client.put_public_access_block(Bucket=bucket_name, PublicAccessBlockConfiguration=public_access_block_configuration)
            print(self.service, ': ' + f'Success -- Public access block created for bucket {bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating public access block for bucket {bucket_name}: {e}')
            return False, e

        
    # restore object with try accept and args as none
    def s3_restore_object(self, key=None, restore_request=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if restore_request is None:
            restore_request = {
                'Days': 1,
                'GlacierJobParameters': {
                    'Tier': 'Standard'
                }
            }
        self.s3_put_object( storage_class='GLACIER')

        try:
            self.client.restore_object(Bucket=self.bucket_name, Key=key, RestoreRequest=restore_request)
            print(self.service, ': ' + f'Success -- Object restored for object {key}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error restoring object for object {key}: {e}')
            return False, e


    # select object content with try accept and args as none
    def s3_select_object_content(self, key=None, expression=None, expression_type=None, input_serialization=None, output_serialization=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if expression is None:
            expression = 'select * from s3object'
        if expression_type is None:
            expression_type = 'SQL'
        if input_serialization is None:
            input_serialization = {
                'CSV': {
                    'FileHeaderInfo': 'USE',
                    'RecordDelimiter': '\n',
                    'FieldDelimiter': ','
                }
            }
        if output_serialization is None:
            output_serialization = {
                'CSV': {}
            }
        self.s3_put_object(key=key)

        try:
            response = self.client.select_object_content(
                Bucket=self.bucket_name,
                Key=key,
                Expression=expression,
                ExpressionType=expression_type,
                InputSerialization=input_serialization,
                OutputSerialization=output_serialization
            )
            print(self.service, ': ' + f'Success -- Object content selected for object {key}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error selecting object content for object {key}: {e}')
            return False, e    


    # upload file with try accept and args as none
    def s3_upload_file(self, key=None, file_path=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if file_path is None:
            file_path = 'test.txt'
        try:
            self.client.upload_file(file_path, self.bucket_name, key)
            print(self.service, ': ' + f'Success -- File uploaded to object {key}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error uploading file to object {key}: {e}')
            return False, e

    # upload file object with try accept and args as none
    def s3_upload_fileobj(self, key=None, fileobj=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if fileobj is None:
            fileobj = open('test.txt', 'rb')
        try:
            self.client.upload_fileobj(fileobj, self.bucket_name, key)
            print(self.service, ': ' + f'Success -- File object uploaded to object {key}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error uploading file object to object {key}: {e}')
            return False, e

    # upload part with try accept and args as none
    def s3_upload_part(self, key=None, upload_id=None, part_number=None, body=None):
        if key is None:
            key = f'{random.randint(1, 1000000)}'
        if upload_id is None:
            res = self.s3_create_multipart_upload(key)
            if res == False:
                print(self.service, ': ' + f'Fail -- Error creating multipart upload for {key} in {self.service} S3 bucket {self.bucket_name}: {e}')
                return False, e
            upload_id = res[1]
        if part_number is None:
            part_number = 1
        if body is None:
            body = 'test'+str(random.randint(1, 1000000000))

        try:
            resp = self.client.upload_part(Bucket=self.bucket_name, Key=key, UploadId=upload_id, PartNumber=part_number, Body=body)
            print(self.service, ': ' + f'Success -- Part uploaded for {key} in {self.service} S3 bucket {self.bucket_name}')
            return True, resp['ETag']
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error uploading part for {key} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e


    # try again
    # upload part copy 
    # write get object response body

    # garbage collector
    def __cleanup__(self):
        # delete all buckets
        try:
            for bucket in self.client.list_buckets()['Buckets']:

                try:
                    # delete all object versions
                    object_response_paginator = self.client.get_paginator('list_object_versions')
                    for object_response_itr in object_response_paginator.paginate(Bucket=bucket['Name']):

                        if 'DeleteMarkers' in object_response_itr:
                            for delete_marker in object_response_itr['DeleteMarkers']:
                                try:
                                    self.client.delete_object(Bucket=bucket['Name'], Key=delete_marker['Key'], VersionId=delete_marker['VersionId'], BypassGovernanceRetention=True)
                                except:
                                    self.client.delete_object(Bucket=bucket['Name'], Key=delete_marker['Key'], VersionId=delete_marker['VersionId'])

                        if 'Versions' in object_response_itr:
                            for version in object_response_itr['Versions']:
                                try:
                                    self.client.delete_object(Bucket=bucket['Name'], Key=version['Key'], VersionId=version['VersionId'], BypassGovernanceRetention=True)
                                except:
                                    self.client.delete_object(Bucket=bucket['Name'], Key=version['Key'], VersionId=version['VersionId'])
                   
                    # delete the bucket
                    self.client.delete_bucket(Bucket=bucket['Name'])
                    print(f'Success -- Bucket {bucket["Name"]} deleted in {self.service} S3')
                except Exception as e:
                    print(f'Fail -- Error deleting bucket {bucket["Name"]} in {self.service} S3: {e}')

        except Exception as e:
            print(f'Fail -- Error listing buckets in {self.service} S3: {e}')

            
        print(f'Cleaned all buckets in {self.service} S3')





# if __name__ == '__main__':

#     # create blob client
#     table_client = S3Client(emulator=False)
#     # logging.basicConfig(level=logging.DEBUG)

#     # table_client.s3_list_buckets()

#     # get all methods and run them
#     methods = [getattr(S3Client, attr) for attr in dir(S3Client) if callable(getattr(S3Client, attr)) and not attr.startswith("__")]

#     # print(len(methods))
#     # for i in methods:
#     #     print(i.__name__)
#     #     i(table_client)

#     table_client.__clean__()