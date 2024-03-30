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
            self.profile = 'aws'
            url = 'REDACTED'
        else:
            self.service = '**EMULATOR**'
            self.region = 'us-west-1'
            self.profile = 'localstack'
            url = 'http://localhost:4566'

        # set up session
        boto3.setup_default_session(profile_name=self.profile)

        try:
            self.client = boto3.client('s3', endpoint_url=url, region_name=self.region)
            print('S3 client created')
        except Exception as e:
            print('S3 client creation failed; error: ', e)

        # create bucket
        try:
            self.client.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region})
            print(f'S3 bucket {self.bucket_name} created')
        except Exception as e:
            print('Bucket creation failed; error: ', e)

    

    # abort multipart upload 
    def s3_abort_multipart_upload(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            resp = self.client.create_multipart_upload(Bucket=self.bucket_name, Key=args[0])
            self.client.abort_multipart_upload(Bucket=self.bucket_name, Key=args[0], UploadId=resp['UploadId'])
            print(self.service, ': ' + f'Success -- Multipart upload aborted for {args[0]} in {self.service} S3 bucket {self.bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error aborting multipart upload for {args[0]} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e
        
    # check if can paginate 
    def s3_can_paginate(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append("list_buckets")

        try:
            self.client.can_paginate(args[0])
            print(self.service, ': ' + f'Success -- Operation {args[0]} can be paginated')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error checking if S3 client can paginate {args[0]}: {e}')
            return False, e
        
    
    # complete multipart upload 
    def s3_complete_multipart_upload(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')

        if not len(args) > 1:
            etag = 2837193728
            try:
                resp = self.client.create_multipart_upload(Bucket=self.bucket_name, Key=args[0])
                args.append(resp['UploadId'])
                res = self.client.upload_part(Bucket=self.bucket_name, Key=args[0], UploadId=resp['UploadId'], PartNumber=1, Body='test'+str(random.randint(1, 1000000000)))
                etag = res['ETag']
            except Exception as e:
                print(self.service, ': ' + f'Error completing multipart upload: ', e)

            args.append([
            {
                'ETag': f'"{etag}"',
                'PartNumber': 1,
            }])


        try:
            self.client.complete_multipart_upload(Bucket=self.bucket_name, Key=args[0], UploadId=args[1], MultipartUpload={'Parts': args[2]})
            print(self.service, ': ' + f'Success -- Multipart upload completed for S3 bucket {self.bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error completing multipart upload for S3 bucket {self.bucket_name}: {e}')
            return False, e


    # copy 
    def s3_copy(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append({'Bucket': self.bucket_name, 'Key': args[0]})

        try:
            self.client.put_object(Bucket=self.bucket_name, Key=args[0], Body=b'test213')

            new_buc = f'test{random.randint(1, 1000000000)}'
            self.client.create_bucket(Bucket=new_buc, CreateBucketConfiguration={'LocationConstraint': self.region})

            self.client.copy(CopySource=args[1], Bucket=new_buc, Key=args[0])
            print(self.service, ': ' + f'Success -- Copy successful for S3 bucket {new_buc}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error copying for S3 bucket {new_buc}: {e}')
            return False, e
        
    # copy object 
    def s3_copy_object(self, args):
        args = list(args)
            
        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append({'Bucket': self.bucket_name, 'Key': args[0]})

        try:
            self.client.put_object(Bucket=self.bucket_name, Key=args[0], Body=b'test213')

            new_buc = f'test{random.randint(1, 1000000000)}'
            self.client.create_bucket(Bucket=new_buc, CreateBucketConfiguration={'LocationConstraint': self.region})

            self.client.copy_object(CopySource=args[1], Bucket=new_buc, Key=args[0])
            print(self.service, ': ' + f'Success -- Copy object successful for S3 bucket {new_buc}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error copying object for S3 bucket {new_buc}: {e}')
            return False, e
        

    # create bucket 
    def s3_create_bucket(self, args):
        args = list(args)

        lock = False
        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000000)}')

        try:
            if lock:
                self.client.create_bucket(Bucket=args[0], CreateBucketConfiguration={'LocationConstraint': self.region}, ObjectLockEnabledForBucket=True)
            else:
                self.client.create_bucket(Bucket=args[0], CreateBucketConfiguration={'LocationConstraint': self.region})
            print(self.service, ': ' + f'Success -- Created bucket {args[0]} in {self.service} S3')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket {args[0]} in {self.service} S3: {e}')
            return False, e


    # create multipart upload 
    def s3_create_multipart_upload(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            resp = self.client.create_multipart_upload(Bucket=self.bucket_name, Key=args[0])
            print(self.service, ': ' + f'Success -- Multipart upload created for {args[0]} in {self.service} S3 bucket {self.bucket_name}')
            return True, resp['UploadId']
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating multipart upload for {args[0]} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e

    # delete bucket 
    def s3_delete_bucket(self, args):
        args = list(args)

        try:
            self.client.delete_bucket(Bucket=self.bucket_name)
            print(self.service, ': ' + f'Success -- Bucket {self.bucket_name} deleted')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket {self.bucket_name}: {e}')
            return False, e
        
    # delete bucket analytics configuration 
    def s3_delete_bucket_analytics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        try:
            self.client.put_bucket_analytics_configuration(Bucket=args[0], Id=args[1], AnalyticsConfiguration={'Id': args[1], 'StorageClassAnalysis': {'DataExport': {'OutputSchemaVersion': 'V_1', 'Destination': {'S3BucketDestination': {'Format': 'CSV', 'BucketAccountId': '123456789012', 'Bucket': 'arn:aws:s3:::mybucket', 'Prefix': 'test'}}}}})
            self.client.delete_bucket_analytics_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket analytics configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket analytics configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
    # delete bucket analytics configuration 
    def s3_delete_empty_bucket_analytics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        try:
            # self.client.put_bucket_analytics_configuration(Bucket=args[0], Id=args[1], AnalyticsConfiguration={'Id': args[1], 'StorageClassAnalysis': {'DataExport': {'OutputSchemaVersion': 'V_1', 'Destination': {'S3BucketDestination': {'Format': 'CSV', 'BucketAccountId': '123456789012', 'Bucket': 'arn:aws:s3:::mybucket', 'Prefix': 'test'}}}}})
            self.client.delete_bucket_analytics_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket analytics configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket analytics configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e

    # delete bucket cors 
    def s3_delete_bucket_cors(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.put_bucket_cors(Bucket=args[0], CORSConfiguration={'CORSRules': [{'AllowedHeaders': ['Authorization'], 'AllowedMethods': ['GET'], 'AllowedOrigins': ['*'], 'ExposeHeaders': ['GET'], 'MaxAgeSeconds': 300}]})
            self.client.delete_bucket_cors(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket cors deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket cors from bucket {args[0]}: {e}')
            return False, e

    # delete bucket encryption 
    def s3_delete_bucket_encryption(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.put_bucket_encryption(Bucket=args[0], ServerSideEncryptionConfiguration={'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]})
            self.client.delete_bucket_encryption(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket encryption deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket encryption from bucket {args[0]}: {e}')
            return False, e

    # delete intellegent tiering configuration 
    def s3_delete_bucket_intelligent_tiering_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        self.s3_put_bucket_intelligent_tiering_configuration(args)

        try:
            # discrepancy -> less than 90 days work for emulator but not for aws
            # self.client.put_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1], IntelligentTieringConfiguration={'Id': args[1], 'Status': 'Enabled', 'Tierings': [{'Days': 1, 'AccessTier': 'ARCHIVE_ACCESS'}, {'Days': 90, 'AccessTier': 'DEEP_ARCHIVE_ACCESS'}]})
            self.client.delete_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket intelligent tiering configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket intelligent tiering configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
    # delete intellegent tiering configuration 
    def s3_delete_bucket_intelligent_tiering_configuration_v2(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        # self.s3_put_bucket_intelligent_tiering_configuration(args)

        try:
            # discrepancy -> less than 90 days work for emulator but not for aws
            self.client.put_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1], IntelligentTieringConfiguration={'Id': args[1], 'Status': 'Enabled', 'Tierings': [{'Days': 1, 'AccessTier': 'ARCHIVE_ACCESS'}, {'Days': 35, 'AccessTier': 'DEEP_ARCHIVE_ACCESS'}]})
            self.client.delete_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket intelligent tiering configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket intelligent tiering configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
    # delete intellegent tiering configuration 
    def s3_delete_bucket_empty_intelligent_tiering_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        # self.s3_put_bucket_intelligent_tiering_configuration(args)

        try:
            self.client.delete_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket intelligent tiering configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket intelligent tiering configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e

    # delete bucket inventory configuration 
    def s3_delete_bucket_inventory_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        self.s3_put_bucket_inventory_configuration(args)

        try:
            self.client.delete_bucket_inventory_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket inventory configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket inventory configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
    # delete bucket inventory configuration 
    def s3_delete_bucket_empty_inventory_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        # self.s3_put_bucket_inventory_configuration(args)

        try:
            self.client.delete_bucket_inventory_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket inventory configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket inventory configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e


    # delete bucket lifecycle 
    def s3_delete_bucket_lifecycle(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_lifecycle([])

        try:
            self.client.delete_bucket_lifecycle(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket lifecycle deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket lifecycle from bucket {args[0]}: {e}')
            return False, e
        
    # delete bucket lifecycle 
    def s3_delete_bucket_empty_lifecycle(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_lifecycle([])

        try:
            self.client.delete_bucket_lifecycle(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket lifecycle deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket lifecycle from bucket {args[0]}: {e}')
            return False, e

    # delete bucket metrics configuration 
    def s3_delete_bucket_metrics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        try:
            self.client.put_bucket_metrics_configuration(Bucket=args[0], Id=args[1], MetricsConfiguration={'Id': args[1],'Filter': {'Prefix': 'test'}})
            self.client.delete_bucket_metrics_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket metrics configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket metrics configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
    # delete bucket metrics configuration 
    def s3_delete_bucket_empty_metrics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'test{random.randint(1, 1000000000)}')

        try:
            # self.client.put_bucket_metrics_configuration(Bucket=args[0], Id=args[1], MetricsConfiguration={'Id': args[1],'Filter': {'Prefix': 'test'}})
            self.client.delete_bucket_metrics_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Bucket metrics configuration {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket metrics configuration {args[1]} from bucket {args[0]}: {e}')
            return False, e
        

    # delete ownership controls 
    def s3_delete_bucket_ownership_controls(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_ownership_controls([])

        try:
            self.client.delete_bucket_ownership_controls(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket ownership controls deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket ownership controls from bucket {args[0]}: {e}')
            return False, e
        
    # delete ownership controls 
    def s3_delete_bucket_empty_ownership_controls(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_ownership_controls([])

        try:
            self.client.delete_bucket_ownership_controls(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket ownership controls deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket ownership controls from bucket {args[0]}: {e}')
            return False, e

    # delete bucket policy 
    def s3_delete_bucket_policy(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_policy([])

        try:
            self.client.delete_bucket_policy(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket policy deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket policy from bucket {args[0]}: {e}')
            return False, e
        
    # delete bucket policy 
    def s3_delete_bucket_empty_policy(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_policy([])

        try:
            self.client.delete_bucket_policy(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket policy deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket policy from bucket {args[0]}: {e}')
            return False, e
        

    # delete bucket replication 
    def s3_delete_bucket_replication(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_replication([f'test{random.randint(1, 1000000000)}'])

        try:
            self.client.delete_bucket_replication(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket replication deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket replication from bucket {args[0]}: {e}')
            return False, e
        
    # delete bucket replication 
    def s3_delete_bucket_empty_replication(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_replication([f'test{random.randint(1, 1000000000)}'])

        try:
            self.client.delete_bucket_replication(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket replication deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket replication from bucket {args[0]}: {e}')
            return False, e

    # delete bucket tagging 
    def s3_delete_bucket_tagging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.put_bucket_tagging(Bucket=args[0], Tagging={'TagSet': [{'Key': 'string', 'Value': 'string'}]})
            self.client.delete_bucket_tagging(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket tagging deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket tagging from bucket {args[0]}: {e}')
            return False, e
        
    # delete bucket tagging 
    def s3_delete_bucket_empty_tagging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            # self.client.put_bucket_tagging(Bucket=args[0], Tagging={'TagSet': [{'Key': 'string', 'Value': 'string'}]})
            self.client.delete_bucket_tagging(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket tagging deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket tagging from bucket {args[0]}: {e}')
            return False, e
        

    # delete bucket website 
    def s3_delete_bucket_website(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.put_bucket_website(Bucket=args[0], WebsiteConfiguration={'RedirectAllRequestsTo': {'HostName': 'string', 'Protocol': 'http'}})
            self.client.delete_bucket_website(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket website deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket website from bucket {args[0]}: {e}')
            return False, e
        
    
    # delete bucket website 
    def s3_delete_bucket_empty_website(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            # self.client.put_bucket_website(Bucket=args[0], WebsiteConfiguration={'RedirectAllRequestsTo': {'HostName': 'string', 'Protocol': 'http'}})
            self.client.delete_bucket_website(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket website deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting bucket website from bucket {args[0]}: {e}')
            return False, e
        

    # delete object 
    def s3_delete_object(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1], Body='string')
            self.client.delete_object(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting object {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
    # delete object 
    def s3_delete_empty_object(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            # self.client.put_object(Bucket=args[0], Key=args[1], Body='string')
            self.client.delete_object(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object {args[1]} deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting object {args[1]} from bucket {args[0]}: {e}')
            return False, e
        

    # delete object tagging 
    def s3_delete_object_tagging(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.put_object_tagging(Bucket=args[0], Key=args[1], Tagging={'TagSet': [{'Key': 'string', 'Value': 'string'}]})
            self.client.delete_object_tagging(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object tagging deleted from object {args[1]} in bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting object tagging from object {args[1]} in bucket {args[0]}: {e}')
            return False, e
        
    # delete object tagging 
    def s3_delete_object_empty_tagging(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            # self.client.put_object(Bucket=args[0], Key=args[1])
            # self.client.put_object_tagging(Bucket=args[0], Key=args[1], Tagging={'TagSet': [{'Key': 'string', 'Value': 'string'}]})
            self.client.delete_object_tagging(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object tagging deleted from object {args[1]} in bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting object tagging from object {args[1]} in bucket {args[0]}: {e}')
            return False, e

    # delete objects 
    def s3_delete_objects(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1], Body='string')
            self.client.put_object(Bucket=args[0], Key=args[2], Body='string')
            self.client.delete_objects(Bucket=args[0], Delete={'Objects': [{'Key': args[1]}, {'Key': args[2]}]})
            print(self.service, ': ' + f'Success -- Objects deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting objects from bucket {args[0]}: {e}')
            return False, e

    # delete public access block 
    def s3_delete_public_access_block(self, args):
        args = list(args)
     
        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.delete_public_access_block(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Public access block deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting public access block from bucket {args[0]}: {e}')
            return False, e
        
    # delete public access block 
    def s3_delete_empty_public_access_block(self, args):
        args = list(args)
     
        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.delete_public_access_block(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Public access block deleted from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error deleting public access block from bucket {args[0]}: {e}')
            return False, e
        


    # download file 
    def s3_download_file(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append(f'file{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.download_file(Bucket=args[0], Key=args[1], Filename=args[2])
            print(self.service, ': ' + f'Success -- File {args[2]} downloaded from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error downloading file {args[2]} from bucket {args[0]}: {e}')
            return False, e
        

    # download fileobj 
    def s3_download_fileobj(self, args):
        args = list(args)
       
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            with open('filename', 'wb') as data:
                self.client.download_fileobj(Bucket=args[0], Key=args[1], Fileobj=data)
            print(self.service, ': ' + f'Success -- Fileobj downloaded from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error downloading fileobj from bucket {args[0]}: {e}')
            return False, e


    # generate presigned post 
    def s3_generate_presigned_post(self, args):
        args = list(args)
            
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append(None)
        if not len(args) > 3:
            args.append(None)
        if not len(args) > 4:
            args.append(3600)

        try:
            self.client.generate_presigned_post(Bucket=args[0], Key=args[1], Fields=args[2], Conditions=args[3], ExpiresIn=args[4])
            print(self.service, ': ' + f'Success -- Presigned post generated for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error generating presigned post for bucket {args[0]}: {e}')
            return False, e
            
    # generate presigned url 
    def s3_generate_presigned_url(self, args):
        args = list(args)
                
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append(3600)
        if not len(args) > 3:
            args.append('get_object')

        try:
            self.client.generate_presigned_url(ClientMethod=args[3], Params={'Bucket': args[0], 'Key': args[1]}, ExpiresIn=args[2])
            print(self.service, ': ' + f'Success -- Presigned url generated for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error generating presigned url for bucket {args[0]}: {e}')
            return False, e

    # get bucket accelerate configuration 
    def s3_get_bucket_accelerate_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_accelerate_configuration(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Accelerate configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving accelerate configuration from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket acl 
    def s3_get_bucket_acl(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_acl(Bucket=args[0])
            print(self.service, ': ' + f'Success -- ACL retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving ACL from bucket {args[0]}: {e}')
            return False, e

    # get bucket analytics configuration 
    def s3_get_bucket_analytics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append('test')

        self.s3_put_bucket_analytics_configuration(args)

        try:
            self.client.get_bucket_analytics_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Analytics configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving analytics configuration from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket analytics configuration 
    def s3_get_bucket_empty_analytics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append('test')

        # self.s3_put_bucket_analytics_configuration(args)

        try:
            self.client.get_bucket_analytics_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Analytics configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving analytics configuration from bucket {args[0]}: {e}')
            return False, e

    # get bucket cors 
    def s3_get_bucket_cors(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_cors(args)

        try:
            self.client.get_bucket_cors(Bucket=args[0])
            print(self.service, ': ' + f'Success -- CORS retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving CORS from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket cors 
    def s3_get_bucket_empty_cors(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_cors(args)

        try:
            self.client.get_bucket_cors(Bucket=args[0])
            print(self.service, ': ' + f'Success -- CORS retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving CORS from bucket {args[0]}: {e}')
            return False, e

    # get bucket encryption 
    def s3_get_bucket_encryption(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_encryption(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Encryption retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving encryption from bucket {args[0]}: {e}')
            return False, e
        
        
    # get intellegent tiering configuration 
    def s3_get_bucket_intelligent_tiering_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        self.s3_put_bucket_intelligent_tiering_configuration(args)

        try:
            resp = self.client.get_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Intelligent tiering configuration retrieved from bucket {args[0]}')
            print(resp)
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving intelligent tiering configuration from bucket {args[0]}: {e}')
            return False, e

    # get intellegent tiering configuration 
    def s3_get_bucket_empty_intelligent_tiering_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        # self.s3_put_bucket_intelligent_tiering_configuration(args)

        try:
            resp = self.client.get_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Intelligent tiering configuration retrieved from bucket {args[0]}')
            print(resp)
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving intelligent tiering configuration from bucket {args[0]}: {e}')
            return False, e
        
    # get intellegent tiering configuration 
    def s3_get_bucket_intelligent_tiering_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        self.s3_put_bucket_intelligent_tiering_configuration(args)

        try:
            resp = self.client.get_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Intelligent tiering configuration retrieved from bucket {args[0]}')
            print(resp)
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving intelligent tiering configuration from bucket {args[0]}: {e}')
            return False, e
        
    # get intellegent tiering configuration 
    def s3_get_bucket_empty_intelligent_tiering_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        # self.s3_put_bucket_intelligent_tiering_configuration(args)

        try:
            resp = self.client.get_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Intelligent tiering configuration retrieved from bucket {args[0]}')
            print(resp)
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving intelligent tiering configuration from bucket {args[0]}: {e}')
            return False, e

    # get bucket inventory configuration 
    def s3_get_bucket_inventory_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        self.s3_put_bucket_inventory_configuration(args)

        try:
            self.client.get_bucket_inventory_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Inventory configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving inventory configuration from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket inventory configuration 
    def s3_get_bucket_empty_inventory_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        # self.s3_put_bucket_inventory_configuration(args)

        try:
            self.client.get_bucket_inventory_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Inventory configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving inventory configuration from bucket {args[0]}: {e}')
            return False, e


    # get bucket lifecycle 
    def s3_get_bucket_lifecycle(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_lifecycle([])

        try:
            self.client.get_bucket_lifecycle(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Lifecycle retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving lifecycle from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket lifecycle 
    def s3_get_bucket_empty_lifecycle(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_lifecycle([])

        try:
            self.client.get_bucket_lifecycle(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Lifecycle retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving lifecycle from bucket {args[0]}: {e}')
            return False, e


    # get bucket lifecycle configuration 
    def s3_get_bucket_lifecycle_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_lifecycle_configuration([])

        try:
            self.client.get_bucket_lifecycle_configuration(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Lifecycle configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving lifecycle configuration from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket lifecycle configuration 
    def s3_get_bucket_empty_lifecycle_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_lifecycle_configuration([])

        try:
            self.client.get_bucket_lifecycle_configuration(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Lifecycle configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving lifecycle configuration from bucket {args[0]}: {e}')
            return False, e

    # get bucket location 
    def s3_get_bucket_location(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_location(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Location retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving location from bucket {args[0]}: {e}')
            return False, e


    # get bucket logging 
    def s3_get_bucket_logging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_logging(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Logging retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving logging from bucket {args[0]}: {e}')
            return False, e

    # get bucket metrics configuration 
    def s3_get_bucket_metrics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        self.s3_put_bucket_metrics_configuration(args)

        try:
            self.client.get_bucket_metrics_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Metrics configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving metrics configuration from bucket {args[0]}: {e}')
            return False, e
        

    # get bucket metrics configuration 
    def s3_get_bucket_empty_metrics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        # self.s3_put_bucket_metrics_configuration(args)

        try:
            self.client.get_bucket_metrics_configuration(Bucket=args[0], Id=args[1])
            print(self.service, ': ' + f'Success -- Metrics configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving metrics configuration from bucket {args[0]}: {e}')
            return False, e
        

    # get bucket notification 
    def s3_get_bucket_notification(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_notification(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Notification retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving notification from bucket {args[0]}: {e}')
            return False, e

    # get bucket notification configuration 
    def s3_get_bucket_notification_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_notification_configuration(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Notification configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving notification configuration from bucket {args[0]}: {e}')
            return False, e
        
    # gte ownership controls 
    def s3_get_bucket_ownership_controls(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_ownership_controls([])

        try:
            self.client.get_bucket_ownership_controls(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Ownership controls retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving ownership controls from bucket {args[0]}: {e}')
            return False, e
        
    # get ownership controls 
    def s3_get_bucket_empty_ownership_controls(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_ownership_controls([])

        try:
            self.client.get_bucket_ownership_controls(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Ownership controls retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving ownership controls from bucket {args[0]}: {e}')
            return False, e

    # get bucket policy 
    def s3_get_bucket_policy(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_policy([])

        try:
            self.client.get_bucket_policy(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Policy retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving policy from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket policy 
    def s3_get_bucket_empty_policy(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_policy([])

        try:
            self.client.get_bucket_policy(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Policy retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving policy from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket policy status 
    def s3_get_bucket_policy_status(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_policy([])

        try:
            self.client.get_bucket_policy_status(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Policy status retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving policy status from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket policy status 
    def s3_get_bucket_empty_policy_status(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_policy([])

        try:
            self.client.get_bucket_policy_status(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Policy status retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving policy status from bucket {args[0]}: {e}')
            return False, e
        

    # get bucket replication 
    def s3_get_bucket_replication(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_replication([])

        try:
            self.client.get_bucket_replication(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Replication retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving replication from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket replication 
    def s3_get_bucket_empty_replication(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_replication([])

        try:
            self.client.get_bucket_replication(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Replication retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving replication from bucket {args[0]}: {e}')
            return False, e

    # get bucket request payment 
    def s3_get_bucket_request_payment(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_request_payment(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Request payment retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving request payment from bucket {args[0]}: {e}')
            return False, e


    # get bucket tagging 
    def s3_get_bucket_tagging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_tagging([])

        try:
            self.client.get_bucket_tagging(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Tagging retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving tagging from bucket {args[0]}: {e}')
            return False, e
        
    # get bucket tagging 
    def s3_get_bucket_empty_tagging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_tagging([])

        try:
            self.client.get_bucket_tagging(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Tagging retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving tagging from bucket {args[0]}: {e}')
            return False, e
        

    # get bucket versioning 
    def s3_get_bucket_versioning(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_bucket_versioning(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Versioning retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving versioning from bucket {args[0]}: {e}')
            return False, e


    # get bucket website 
    def s3_get_bucket_website(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_bucket_website([])

        try:
            self.client.get_bucket_website(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Website retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving website from bucket {args[0]}: {e}')
            return False, e
        
    
    # get bucket website 
    def s3_get_bucket_empty_website(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        # self.s3_put_bucket_website([])

        try:
            self.client.get_bucket_website(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Website retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving website from bucket {args[0]}: {e}')
            return False, e
        

    # get object 
    def s3_get_object(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.get_object(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object {args[1]} from bucket {args[0]}: {e}')
            return False, e


    # get object acl 
    def s3_get_object_acl(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')


        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.get_object_acl(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object ACL {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object ACL {args[1]} from bucket {args[0]}: {e}')
            return False, e

    # get attributes of object 
    def s3_get_object_attributes(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.get_object_attributes(Bucket=args[0], Key=args[1], ObjectAttributes=['ETag','Checksum','ObjectParts','StorageClass','ObjectSize'])
            print(self.service, ': ' + f'Success -- Object attributes {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object attributes {args[1]} from bucket {args[0]}: {e}')
            return False, e

    # get object legal hold 
    def s3_get_object_legal_hold(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        self.s3_put_object_legal_hold(args)

        try:
            self.client.get_object_legal_hold(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object legal hold {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object legal hold {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
    # get object legal hold 
    def s3_get_object_empty_legal_hold(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        # self.s3_put_object_legal_hold(args)

        try:
            self.client.get_object_legal_hold(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object legal hold {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object legal hold {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
    # get object lock configuration 
    def s3_get_object_lock_configuration(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000)}')

        self.s3_put_object_lock_configuration([args[0]])

        try:
            self.client.get_object_lock_configuration(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Object lock configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object lock configuration from bucket {args[0]}: {e}')
            return False, e
        
    # get object lock configuration 
    def s3_get_object_empty_lock_configuration(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000)}')

        # self.s3_put_object_lock_configuration([args[0]])

        try:
            self.client.get_object_lock_configuration(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Object lock configuration retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object lock configuration from bucket {args[0]}: {e}')
            return False, e
        

    # get object retention 
    def s3_get_object_retention(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        self.s3_put_object_legal_hold(args)

        try:
            self.client.get_object_retention(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object retention {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object retention {args[1]} from bucket {args[0]}: {e}')
            return False, e
        

    # get object retention 
    def s3_get_object_empty_retention(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        # self.s3_put_object_legal_hold(args)

        try:
            self.client.get_object_retention(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object retention {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object retention {args[1]} from bucket {args[0]}: {e}')
            return False, e
        

    # get object tagging 
    def s3_get_object_tagging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.get_object_tagging(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object tagging {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object tagging {args[1]} from bucket {args[0]}: {e}')
            return False, e


    # get object torrent 
    def s3_get_object_torrent(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.get_object_torrent(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object torrent {args[1]} retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving object torrent {args[1]} from bucket {args[0]}: {e}')
            return False, e
        
        

    # !!ignore
    # get paginator 
    def s3_get_paginator(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append('list_object_versions')

        try:
            self.client.get_paginator(args[0])
            print(self.service, ': ' + f'Success -- Paginator retrieved')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving paginator: {e}')
            return False, e
        

    # get public access block 
    def s3_get_public_access_block(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        self.s3_put_public_access_block([])

        try:
            self.client.get_public_access_block(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Public access block retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving public access block from bucket {args[0]}: {e}')
            return False, e

    # !!ignore
    # get waiters 
    def s3_get_waiter(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.get_waiter(args[0])
            print(self.service, ': ' + f'Success -- Waiter retrieved from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error retrieving waiter from bucket {args[0]}: {e}')
            return False, e
        

    # head bucket 
    def s3_head_bucket(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.head_bucket(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket {args[0]} head')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error head bucket {args[0]}: {e}')
            return False, e
        
    # head object 
    def s3_head_object(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.head_object(Bucket=args[0], Key=args[1])
            print(self.service, ': ' + f'Success -- Object {args[1]} head from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error head object {args[1]} from bucket {args[0]}: {e}')
            return False, e


    # list bucket analytics configurations 
    def s3_list_bucket_analytics_configurations(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.list_bucket_analytics_configurations(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket analytics configurations listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing bucket analytics configurations from bucket {args[0]}: {e}')
            return False, e

    # list bucket intelligent tiering configuration 
    def s3_list_bucket_intelligent_tiering_configurations(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.list_bucket_intelligent_tiering_configurations(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket intelligent tiering configurations listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing bucket intelligent tiering configurations from bucket {args[0]}: {e}')
            return False, e

    # list bucket inventory configurations 
    def s3_list_bucket_inventory_configurations(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.list_bucket_inventory_configurations(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket inventory configurations listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing bucket inventory configurations from bucket {args[0]}: {e}')
            return False, e


    # list bucket metrics configurations 
    def s3_list_bucket_metrics_configurations(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.list_bucket_metrics_configurations(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Bucket metrics configurations listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing bucket metrics configurations from bucket {args[0]}: {e}')
            return False, e
        
    # list buckets 
    def s3_list_buckets(self, args):
        args = list(args)
            
        try:
            self.client.list_buckets()
            print(self.service, ': ' + f'Success -- Buckets listed')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing buckets: {e}')
            return False, e

    # list multipart uploads 
    def s3_list_multipart_uploads(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.list_multipart_uploads(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Multipart uploads listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing multipart uploads from bucket {args[0]}: {e}')
            return False, e

    # list object versions 
    def s3_list_object_versions(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.list_object_versions(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Object versions listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing object versions from bucket {args[0]}: {e}')
            return False, e
        
    # list objects 
    def s3_list_objects(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.list_objects(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Objects listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing objects from bucket {args[0]}: {e}')
            return False, e


    # list objects v2 
    def s3_list_objects_v2(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)

        try:
            self.client.list_objects_v2(Bucket=args[0])
            print(self.service, ': ' + f'Success -- Objects v2 listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing objects v2 from bucket {args[0]}: {e}')
            return False, e
        

    # list parts 
    def s3_list_parts(self, args):
        args = list(args)
            
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            resp = self.client.create_multipart_upload(Bucket=args[0], Key=args[1])
            args.append(resp['UploadId'])

        try:
            self.client.list_parts(Bucket=args[0], Key=args[1], UploadId=args[2])
            print(self.service, ': ' + f'Success -- Parts listed from bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error listing parts from bucket {args[0]}: {e}')
            return False, e


    # put bucket acelerate configuration 
    def s3_put_bucket_accelerate_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({'Status': 'Enabled'})

        try:
            self.client.put_bucket_accelerate_configuration(Bucket=args[0], AccelerateConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket accelerate configuration added to bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error adding bucket accelerate configuration to bucket {args[0]}: {e}')
            return False, e

    # put bucket acl 
    def s3_put_bucket_acl(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append('public-read')

        try:
            self.client.put_bucket_acl(Bucket=args[0], ACL=args[1])
            print(self.service, ': ' + f'Success -- Bucket ACL added to bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error adding bucket ACL to bucket {args[0]}: {e}')
            return False, e


    # put analytics configuration 
    def s3_put_bucket_analytics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append({
                'Id': args[1],
                'StorageClassAnalysis': {
                    'DataExport': {
                        'OutputSchemaVersion': 'V_1',
                        'Destination': {
                            'S3BucketDestination': {
                                'Bucket': f'arn:aws:s3:::{args[0]}',
                                'Format': 'CSV'
                            }
                        }
                    }
                }
            })

        try:
            self.client.put_bucket_analytics_configuration(Bucket=args[0], Id=args[1], AnalyticsConfiguration=args[2])
            print(self.service, ': ' + f'Success -- Bucket analytics configuration {args[1]} created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket analytics configuration {args[1]} for bucket {args[0]}: {e}')
            return False, e


    # put bucket cors 
    def s3_put_bucket_cors(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
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
            })

        try:
            self.client.put_bucket_cors(Bucket=args[0], CORSConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket cors created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket cors for bucket {args[0]}: {e}')
            return False, e

    # put bucket encryption 
    def s3_put_bucket_encryption(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    },
                ]
            })

        try:
            self.client.put_bucket_encryption(Bucket=args[0], ServerSideEncryptionConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket encryption created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket encryption for bucket {args[0]}: {e}')
            return False, e


    # put intellegent tiering configuration 
    def s3_put_bucket_intelligent_tiering_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append({
                'Id': args[1],
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
            })

        try:
            self.client.put_bucket_intelligent_tiering_configuration(Bucket=args[0], Id=args[1], IntelligentTieringConfiguration=args[2])
            print(self.service, ': ' + f'Success -- Bucket intelligent tiering configuration {args[1]} created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket intelligent tiering configuration {args[1]} for bucket {args[0]}: {e}')
            return False, e


    # put bucket inventory configuration 
    def s3_put_bucket_inventory_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append({
                'Id': args[1],
                'IsEnabled': True,
                'Destination': {
                    'S3BucketDestination': {
                        'Bucket': f'arn:aws:s3:::{args[0]}',
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
            })

        try:
            self.client.put_bucket_inventory_configuration(Bucket=args[0], Id=args[1], InventoryConfiguration=args[2])
            print(self.service, ': ' + f'Success -- Bucket inventory configuration {args[1]} created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket inventory configuration {args[1]} for bucket {args[0]}: {e}')
            return False, e

    # put bucket lifecycle 
    def s3_put_bucket_lifecycle(self, args):
        args = list(args)
            
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'Rules': [
                    {
                        'Expiration': {
                            'Days': 365
                        },
                        'Prefix': 'test',
                        'ID': 'test',
                        'Status': 'Enabled'
                    },
                ]
            })

        try:
            self.client.put_bucket_lifecycle(Bucket=args[0], LifecycleConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket lifecycle created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket lifecycle for bucket {args[0]}: {e}')
            return False, e
            

    # put bucket lifecycle configuration 
    def s3_put_bucket_lifecycle_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
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
            })

        try:
            self.client.put_bucket_lifecycle_configuration(Bucket=args[0], LifecycleConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket lifecycle configuration created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket lifecycle configuration for bucket {args[0]}: {e}')
            return False, e


    # put bucket logging 
    def s3_put_bucket_logging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'LoggingEnabled': {
                    'TargetBucket': args[0],
                    'TargetPrefix': 'test'
                }
            })

        try:
            res = self.client.put_bucket_logging(Bucket=args[0], BucketLoggingStatus=args[1])
            print(self.service, ': ' + f'Success -- Bucket logging configuration created for bucket {args[0]}')
            print(res)

            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket logging configuration for bucket {args[0]}: {e}')
            return False, e



    # put bucket metrics configuration 
    def s3_put_bucket_metrics_configuration(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append({
                'Id': args[1],
                'Filter': {
                    'Prefix': 'test'
                }
            })

        try:
            self.client.put_bucket_metrics_configuration(Bucket=args[0], Id=args[1], MetricsConfiguration=args[2])
            print(self.service, ': ' + f'Success -- Bucket metrics configuration {args[2]} created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket metrics configuration {args[2]} for bucket {args[0]}: {e}')
            return False, e
        
        

    # put_bucket_notification
    # deprecated


    # put bucket notification configuration 
    def s3_put_bucket_notification_configuration(self, args):
        args = list(args)
            
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'TopicConfigurations': [
                    {
                        'TopicArn': f'arn:aws:sns:{self.region}:818637742267:MyTopic',
                        'Events': [
                            's3:ObjectCreated:*'
                        ]
                    },
                ]
            })

        try:
            boto3.setup_default_session(profile_name=self.profile)
            client = boto3.client('sns')
            client.create_topic(Name='MyTopic')

            self.client.put_bucket_notification_configuration(Bucket=args[0], NotificationConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket notification configuration created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket notification configuration for bucket {args[0]}: {e}')
            return False, e

    # put ownership controls 
    def s3_put_bucket_ownership_controls(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'Rules': [
                    {
                        'ObjectOwnership': 'BucketOwnerPreferred'
                    },
                ]
            })

        try:
            self.client.put_bucket_ownership_controls(Bucket=args[0], OwnershipControls=args[1])
            print(self.service, ': ' + f'Success -- Bucket ownership controls created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket ownership controls for bucket {args[0]}: {e}')
            return False, e

    # !!ignore
    # put bucket policy 
    def s3_put_bucket_policy(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Sid': 'AddPerm',
                        'Effect': 'Allow',
                        'Principal': '*',
                        'Action': ['s3:GetObject'],
                        'Resource': f'arn:aws:s3:::{args[0]}/*'
                    },
                ]
            })

        try:
            self.client.put_bucket_policy(Bucket=args[0], Policy=json.dumps(args[1]))
            print(self.service, ': ' + f'Success -- Bucket policy created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket policy for bucket {args[0]}: {e}')
            return False, e


    # put bucket replication 
    def s3_put_bucket_replication(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000000)}')

        if not len(args) > 1:
            args.append({
                'Role': 'arn:aws:iam::123456789012:role/replication-role',
                'Rules': [
                    {
                        'ID': 'test',
                        'Prefix': 'test',
                        'Status': 'Enabled',
                        'Destination': {
                            'Bucket': f'arn:aws:s3:::{args[0]}'
                        }
                    },
                ]
            })

        try:
            self.client.create_bucket(Bucket=args[0], CreateBucketConfiguration={'LocationConstraint': self.region})
            self.s3_put_bucket_versioning([args[0]])
            self.client.put_bucket_replication(Bucket=args[0], ReplicationConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket replication configuration created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket replication configuration for bucket {args[0]}: {e}')
            return False, e
        

    # put bucket tagging 
    def s3_put_bucket_tagging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'TagSet': [
                    {
                        'Key': 'test',
                        'Value': 'test'
                    },
                ]
            })

        try:
            self.client.put_bucket_tagging(Bucket=args[0], Tagging=args[1])
            print(self.service, ': ' + f'Success -- Bucket tagging created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket tagging for bucket {args[0]}: {e}')
            return False, e


    # put bucket versioning 
    def s3_put_bucket_versioning(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'Status': 'Enabled',
                'MFADelete': 'Disabled',
            })

        try:
            self.client.put_bucket_versioning(Bucket=args[0], VersioningConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket versioning configuration created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket versioning configuration for bucket {args[0]}: {e}')
            return False, e


    # put bucket website 
    def s3_put_bucket_website(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'ErrorDocument': {
                    'Key': 'error.html'
                },
                'IndexDocument': {
                    'Suffix': 'index.html'
                }
            })

        try:
            self.client.put_bucket_website(Bucket=args[0], WebsiteConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Bucket website configuration created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating bucket website configuration for bucket {args[0]}: {e}')
            return False, e
        
    # put object 
    def s3_put_object(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 2:
            args.append('test')
        if not len(args) > 3:
            args.append('STANDARD')

        try:
            self.client.put_object(Bucket=args[0], Key=args[1], Body=args[2], StorageClass=args[3])
            print(self.service, ': ' + f'Success -- Put object {args[1]} in {self.service} S3 bucket {self.bucket_name}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error putting object {args[1]} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e


    # put object acl 
    def s3_put_object_acl(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append('public-read')

        try:
            self.client.put_object(Bucket=self.bucket_name, Key=args[0])
            self.client.put_object_acl(Bucket=self.bucket_name, Key=args[0], ACL=args[1])
            print(self.service, ': ' + f'Success -- Object ACL created for object {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object ACL for object {args[0]}: {e}')
            return False, e


    # put object legal hold 
    def s3_put_object_legal_hold(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000)}')

        if not len(args) > 1:
            args.append(f'{random.randint(1, 1000000)}')

        if not len(args) > 2:
            args.append({
                    'Status': 'OFF'
                })

        # comment for bult deletion
        self.s3_put_object_lock_configuration([args[0]])

        try:
            self.client.put_object(Bucket=args[0], Key=args[1])
            self.client.put_object_legal_hold(Bucket=args[0], Key=args[1], LegalHold=args[2])
            print(self.service, ': ' + f'Success -- Object legal hold created')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object legal hold: {e}')
            return False, e

    # put object lock configuration 
    def s3_put_object_lock_configuration(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'bucket{random.randint(1, 1000000)}')

        if not len(args) > 1:
            args.append({
                'ObjectLockEnabled': 'Enabled',
                'Rule': {
                    'DefaultRetention': {
                        'Days': 1,
                        'Mode': 'GOVERNANCE'
                    }
                }
            })

        try:
            self.client.create_bucket(Bucket=args[0], ObjectLockEnabledForBucket=True, CreateBucketConfiguration={'LocationConstraint': self.region})
            self.client.put_object_lock_configuration(Bucket=args[0], ObjectLockConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Object lock configuration created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object lock configuration for bucket {args[0]}: {e}')
            return False, e


    # put object retention 
    def s3_put_object_retention(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')


        if not len(args) > 1:
            args.append({
                    'Mode': 'GOVERNANCE',
                    'RetainUntilDate': datetime.datetime.today() + datetime.timedelta(days=1)
                })
        bucket_name = f'bucket{random.randint(1, 1000000)}'
        self.s3_put_object_lock_configuration([bucket_name])

        try:
            self.client.put_object(Bucket=bucket_name, Key=args[0])
            self.client.put_object_retention(Bucket=bucket_name, Key=args[0], Retention=args[1])
            print(self.service, ': ' + f'Success -- Object retention created for object {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object retention for object {args[0]}: {e}')
            return False, e

    # put object tagging 
    def s3_put_object_tagging(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append({
                'TagSet': [
                    {
                        'Key': 'test',
                        'Value': 'test'
                    },
                ]
            })

        try:
            self.client.put_object(Bucket=self.bucket_name, Key=args[0])
            self.client.put_object_tagging(Bucket=self.bucket_name, Key=args[0], Tagging=args[1])
            print(self.service, ': ' + f'Success -- Object tagging created for object {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating object tagging for object {args[0]}: {e}')
            return False, e

    # put public access block 
    def s3_put_public_access_block(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(self.bucket_name)
        if not len(args) > 1:
            args.append({
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            })

        try:
            self.client.put_public_access_block(Bucket=args[0], PublicAccessBlockConfiguration=args[1])
            print(self.service, ': ' + f'Success -- Public access block created for bucket {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error creating public access block for bucket {args[0]}: {e}')
            return False, e

        
    # restore object 
    def s3_restore_object(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append({
                'Days': 1,
                'GlacierJobParameters': {
                    'Tier': 'Standard'
                }
            })

        try:
            self.client.put_object(Bucket=self.bucket_name, Key=args[0], StorageClass='GLACIER')
            self.client.restore_object(Bucket=self.bucket_name, Key=args[0], RestoreRequest=args[1])
            print(self.service, ': ' + f'Success -- Object restored for object {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error restoring object for object {args[0]}: {e}')
            return False, e


    # select object content 
    def s3_select_object_content(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append('select * from s3object')
        if not len(args) > 2:
            args.append('SQL')
        if not len(args) > 3:
            args.append({
                'CSV': {
                    'FileHeaderInfo': 'USE',
                    'RecordDelimiter': '\n',
                    'FieldDelimiter': ','
                }
            })
        if not len(args) > 4:
            args.append({
                'CSV': {}
            })

        try:
            self.client.put_object(Bucket=self.bucket_name, Key=args[0])
            self.client.select_object_content(
                Bucket=self.bucket_name,
                Key=args[0],
                Expression=args[1],
                ExpressionType=args[2],
                InputSerialization=args[3],
                OutputSerialization=args[4]
            )
            print(self.service, ': ' + f'Success -- Object content selected for object {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error selecting object content for object {args[0]}: {e}')
            return False, e    


    # upload file 
    def s3_upload_file(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append('../sdk_tests/S3/test.txt')
        try:
            self.client.upload_file(args[1], self.bucket_name, args[0])
            print(self.service, ': ' + f'Success -- File uploaded to object {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error uploading file to object {args[0]}: {e}')
            return False, e

    # upload file object 
    def s3_upload_fileobj(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            args.append(open('../sdk_tests/S3/test.txt', 'rb'))
        try:
            self.client.upload_fileobj(args[1], self.bucket_name, args[0])
            print(self.service, ': ' + f'Success -- File object uploaded to object {args[0]}')
            return True, ""
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error uploading file object to object {args[0]}: {e}')
            return False, e

    # upload part 
    def s3_upload_part(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            res = self.s3_create_multipart_upload([args[0]])
            if res == False:
                print(self.service, ': ' + f'Fail -- Error creating multipart upload for {args[0]} in {self.service} S3 bucket {self.bucket_name}: {e}')
                return False, e
            upload_id = res[1]
            args.append(upload_id)
        if not len(args) > 2:
            args.append(1)
        if not len(args) > 3:
            args.append('test'+str(random.randint(1, 1000000000)))

        try:
            resp = self.client.upload_part(Bucket=self.bucket_name, Key=args[0], UploadId=args[1], PartNumber=args[2], Body=args[3])
            print(self.service, ': ' + f'Success -- Part uploaded for {args[0]} in {self.service} S3 bucket {self.bucket_name}')
            return True, resp['ETag']
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error uploading part for {args[0]} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e


    # upload part copy 
    def s3_upload_part_copy(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'{random.randint(1, 1000000)}')
        if not len(args) > 1:
            res = self.s3_create_multipart_upload([args[0]])
            if res == False:
                print(self.service, ': ' + f'Fail -- Error creating multipart upload for {args[0]} in {self.service} S3 bucket {self.bucket_name}: {e}')
                return False, e
            upload_id = res[1]
            args.append(upload_id)
        if not len(args) > 2:
            args.append(1)
        if not len(args) > 3:
            key = f'{random.randint(1, 1000000)}'
            args.append({'Bucket': self.bucket_name, 'Key': key})

        try:
            self.client.put_object(Bucket=self.bucket_name, Key=args[3]['Key'], Body='test')
            resp = self.client.upload_part_copy(Bucket=self.bucket_name, Key=args[0], UploadId=args[1], PartNumber=args[2], CopySource=args[3])
            print(self.service, ': ' + f'Success -- Part copy uploaded for {args[0]} in {self.service} S3 bucket {self.bucket_name}')
            return True, resp['CopyPartResult']['ETag']
        except Exception as e:
            print(self.service, ': ' + f'Fail -- Error uploading part copy for {args[0]} in {self.service} S3 bucket {self.bucket_name}: {e}')
            return False, e
            


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


