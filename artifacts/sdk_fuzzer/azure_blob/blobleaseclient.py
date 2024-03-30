import datetime
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobLeaseClient
import random
import json

# Point to certificates
# os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()
config = json.loads(open('config.json').read())

class MyBlobLeaseClient:
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
        self.account_name = config['cloud_account_name']

        # connection string
        if emulator:
            self.connection_string = config['emulator_connection_string']
            self.service = "**EMULATOR**"
        else:
            self.connection_string = config['cloud_connection_string']
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

        # get blob lease client
        try:
            self.blob_lease_client = BlobLeaseClient(self.container_client)
        except Exception as e:
            print(self.service + ": Fail -- Blob lease client is not received. Error: ", e)


    def acquire_lease(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(15)

        try:
            res = self.blob_lease_client.acquire(args[0])
            print(self.service + ": Success -- Blob lease is acquired.")

            # break lease for sequences run
            self.blob_lease_client.break_lease(0)
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob lease is not acquired. Error: ", e)
            return False, e


    def break_lease(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(0)

        try:
            # acquire lease to break it
            self.blob_lease_client.acquire(15)

            # break lease
            res = self.blob_lease_client.break_lease(args[0])
            print(self.service + ": Success -- Blob lease is broken.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob lease is not broken. Error: ", e)
            return False, e

    def change_lease(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append('f81d4fae-7dec-11d0-a765-00a0c91e6bf6')

        try:
            # acquire lease to change it
            self.blob_lease_client.acquire(15)

            # change lease
            res = self.blob_lease_client.change(args[0])
            print(self.service + ": Success -- Blob lease is changed.")

            # break lease for sequences run
            self.blob_lease_client.break_lease(0)
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob lease is not changed. Error: ", e)
            return False, e


    def release_lease(self, args):
        args = list(args)

        try:
            # acquire lease to release it
            self.blob_lease_client.acquire(15)

            # release lease
            res = self.blob_lease_client.release()
            print(self.service + ": Success -- Blob lease is released.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob lease is not released. Error: ", e)
            return False, e


    def renew_lease(self, args):
        args = list(args)

        try:
            # acquire lease to renew it
            self.blob_lease_client.acquire(15)

            # renew lease
            res = self.blob_lease_client.renew()
            print(self.service + ": Success -- Blob lease is renewed.")

            # break lease for sequences run
            self.blob_lease_client.break_lease(0)
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob lease is not renewed. Error: ", e)
            return False, e

    # random delete blob for increasing cov in sequences run   
    def delete_blob(self, args):
        args = list(args)

        try:
            # delete blob
            res = self.container_client.delete_blob(self.blob_name)
            print(self.service + ": Success -- Blob is deleted.")
            return True, res
        except Exception as e:
            print(self.service + ": Fail -- Blob is not deleted. Error: ", e)
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