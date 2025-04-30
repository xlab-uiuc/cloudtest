# from containerclient import ContainerClient
# from blobclient import BlobClient
# from blobserviceclient import MyBlobServiceClient
# from tableclient import MyTableClient
# from tableserviceclient import MyTableServiceClient
# from queueclient import MyQueueClient
# from queueserviceclient import MyQueueServiceClient

from azure.storage.blob import BlobServiceClient, StandardBlobTier



def main():

    flag = True

    # test_bc = BlobClient(flag)
    # test_cc = ContainerClient(flag)
    # test_bsc = MyBlobServiceClient(flag)
    # test_tc = MyTableClient(flag)
    # test_tsc = MyTableServiceClient(flag)
    # test_qc = MyQueueClient(flag)
    # test_qsc = MyQueueServiceClient(flag)

    # get methods
    # methods_bc = [getattr(BlobClient, attr) for attr in dir(BlobClient) if callable(getattr(BlobClient, attr)) and not attr.startswith("__")]
    # methods_cc = [getattr(ContainerClient, attr) for attr in dir(ContainerClient) if callable(getattr(ContainerClient, attr)) and not attr.startswith("__")]
    # methods_bsc = [getattr(MyBlobServiceClient, attr) for attr in dir(MyBlobServiceClient) if callable(getattr(MyBlobServiceClient, attr)) and not attr.startswith("__")]
    # methods_tc = [getattr(MyTableClient, attr) for attr in dir(MyTableClient) if callable(getattr(MyTableClient, attr)) and not attr.startswith("__")]
    # methods_tsc = [getattr(MyTableServiceClient, attr) for attr in dir(MyTableServiceClient) if callable(getattr(MyTableServiceClient, attr)) and not attr.startswith("__")]
    # methods_qc = [getattr(MyQueueClient, attr) for attr in dir(MyQueueClient) if callable(getattr(MyQueueClient, attr)) and not attr.startswith("__")]
    # methods_qsc = [getattr(MyQueueServiceClient, attr) for attr in dir(MyQueueServiceClient) if callable(getattr(MyQueueServiceClient, attr)) and not attr.startswith("__")]
    
    # run methods
    # for i in methods_bc:
    #     if "commit_block_list" in i.__name__:
    #         i(test_bc)

    # for i in methods_cc:
    #     i(test_cc)
    # for i in methods_bsc:
    #     i(test_bsc)
    # for i in methods_tc:
    #     i(test_tc)
    # for i in methods_tsc:
    #     i(test_tsc)
    # for i in methods_qc:
    #     i(test_qc)
    # for i in methods_qsc:
    #     i(test_qsc)

    connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client("testcontainer11")
    container_client.create_container()
    container_client.upload_blob(data=b'First one', name="testblob", blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})

    args = []
    # blob name
    if not len(args) > 0:
        args.append("testblob")
    # standard page blob tier
    if not len(args) > 1:
        args.append(StandardBlobTier('Cool'))
    
    try: 
        res = container_client.set_standard_blob_tier_blobs(args[1], args[0])
    except Exception as e:
        print(e) 




    # connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
    # service = "**EMULATOR**"
    # blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    # container_client = blob_service_client.get_container_client("testcontainer4")
    # container_client.create_container()
    # blob_client = container_client.get_blob_client("testblob")
    # container_client.upload_blob(data=b'First one', name="testblob", blob_type='BlockBlob', length=len('First one'), metadata={'hello': 'world', 'number': '42'})
    # try:
    #     res = blob_client.get_blob_tags() 
    # except Exception as e:
    #     print(e)
        # print(f"Error message: {e.response.reason}")
        # print(f"Status code: {e.response.status_code}")

main()