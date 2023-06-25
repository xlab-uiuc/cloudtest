import datetime
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobLeaseClient
import random
import os

# Point to certificates
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()

class MyBlobLeaseClient:
    def __init__(self, emulator=True, container_name=None, blob_name=None):

        # randomize seed
        random.seed(datetime.datetime.now())

        print("****************************************************************************")

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
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=https://127.0.0.1:10000/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=LGHPh+f0PHvNw8PVYtEkN0fWsqWO9ZsY3DrQox0veta/Ii+aW3m/E7VLVFna/qDMqm/CCg4lou9N+AStwMBcgA==;EndpointSuffix=core.windows.net'
            self.service = "**AZURE**"

        # token
        global credential

        # create blob service client
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        except Exception as e:
            print('Blob service client creation failed; error: ', e)

        # create container client
        try:
            self.container_client = self.blob_service_client.get_container_client(self.container_name)
        except Exception as e:
            print(self.service + ": Container client is not received. Error: ", e)
        
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

        # get blob lease client
        try:
            self.blob_lease_client = BlobLeaseClient(self.container_client)
        except Exception as e:
            print(self.service + ": Blob lease client is not received. Error: ", e)


    def acquire_lease(self, *args):
        args = list(args)

        if not len(args) > 0:
            args.append(15)

        try:
            self.blob_lease_client.acquire(args[0])
            print(self.service + ": Blob lease is acquired.")

            # break lease for sequences run
            self.blob_lease_client.break_lease(0)
        except Exception as e:
            print(self.service + ": Blob lease is not acquired. Error: ", e)


    def break_lease(self, *args):
        args = list(args)

        if not len(args) > 0:
            args.append(0)

        try:
            # acquire lease to break it
            self.blob_lease_client.acquire(15)

            # break lease
            self.blob_lease_client.break_lease(args[0])
            print(self.service + ": Blob lease is broken.")
        except Exception as e:
            print(self.service + ": Blob lease is not broken. Error: ", e)

    def change_lease(self, *args):
        args = list(args)

        if not len(args) > 0:
            args.append('f81d4fae-7dec-11d0-a765-00a0c91e6bf6')

        try:
            # acquire lease to change it
            self.blob_lease_client.acquire(15)

            # change lease
            self.blob_lease_client.change(args[0])
            print(self.service + ": Blob lease is changed.")

            # break lease for sequences run
            self.blob_lease_client.break_lease(0)
        except Exception as e:
            print(self.service + ": Blob lease is not changed. Error: ", e)


    def release_lease(self, *args):
        args = list(args)

        try:
            # acquire lease to release it
            self.blob_lease_client.acquire(15)

            # release lease
            self.blob_lease_client.release()
            print(self.service + ": Blob lease is released.")
        except Exception as e:
            print(self.service + ": Blob lease is not released. Error: ", e)


    def renew_lease(self, *args):
        args = list(args)

        try:
            # acquire lease to renew it
            self.blob_lease_client.acquire(15)

            # renew lease
            self.blob_lease_client.renew()
            print(self.service + ": Blob lease is renewed.")

            # break lease for sequences run
            self.blob_lease_client.break_lease(0)
        except Exception as e:
            print(self.service + ": Blob lease is not renewed. Error: ", e)


    # garbage collection
    def __cleanup__(self):
        try:
            containers = self.blob_service_client.list_containers()
            # delete all containers
            for container in containers:
                # delete all blobs in a container
                # cc = self.blob_service_client.get_container_client(container.name)
                # blobs = cc.list_blobs()
                # for blob in blobs:
                #     try:
                #         cc.delete_blob(blob.name)
                #         print("Blob is deleted.")
                #     except Exception as e:
                #         print("Blob is not deleted. Error: ", e)
                try:
                    self.blob_service_client.delete_container(container.name)
                    print("Container is deleted.")
                except Exception as e:
                    print("Container is not deleted. Error: ", e)
        except Exception as e:
            print("Containers could not be listed. Error: ", e)