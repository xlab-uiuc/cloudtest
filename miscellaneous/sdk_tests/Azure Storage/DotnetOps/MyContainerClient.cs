using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Batch;
using Azure.Storage.Blobs.Specialized;
using Azure.Storage.Blobs.Models;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

class MyContainerClient
{
    private string containerName;
    private string blobName;
    private string connectionString;
    private string service;
    private BlobServiceClient blobServiceClient;
    private BlobContainerClient containerClient;

    public MyContainerClient(bool emulator = true)
    {
        // randomize seed
        Random random = new Random();
        
        // container name
        this.containerName = $"container{random.Next(1, 1000000000)}";


        // blob name
        this.blobName = $"blob{random.Next(1, 1000000000)}";
        

        // connection string
        if (emulator)
        {
            this.connectionString = "DefaultEndpointsProtocol=https;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=https://127.0.0.1:10000/devstoreaccount1;";
            this.service = "**EMULATOR**";
        }
        else
        {
            this.connectionString = "DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=LGHPh+f0PHvNw8PVYtEkN0fWsqWO9ZsY3DrQox0veta/Ii+aW3m/E7VLVFna/qDMqm/CCg4lou9N+AStwMBcgA==;EndpointSuffix=core.windows.net";
            this.service = "**AZURE**";
        }

        // use blob service client to create a container client
        try
        {
            this.blobServiceClient = new BlobServiceClient(connectionString);
            this.containerClient = blobServiceClient.GetBlobContainerClient(this.containerName);
        }
        catch (Exception e)
        {
            Console.WriteLine("Container creation failed; error: " + e.Message);
            // exit
            Environment.Exit(1);
        }

        // create container
        try
        {
            containerClient.Create();
        }
        catch (Exception e)
        {
            Console.WriteLine(service + ": Fail -- Container is not created. Error: " + e.Message);
        }


    }

    // delete given list of blobs (delete_blobs operation) with try-except block
    public Tuple<bool, object> DeleteBlobs()
    {
        
        try
        {
            BlobClient foo = containerClient.GetBlobClient("foo");
            BlobClient bar = containerClient.GetBlobClient("bar");
            BlobClient baz = containerClient.GetBlobClient("baz");

            // upload three new blobs in order to perform batch deletion of them
            containerClient.UploadBlob("foo", new System.IO.MemoryStream(System.Text.Encoding.UTF8.GetBytes("First one")));
            containerClient.UploadBlob("bar", new System.IO.MemoryStream(System.Text.Encoding.UTF8.GetBytes("Second one")));
            containerClient.UploadBlob("baz", new System.IO.MemoryStream(System.Text.Encoding.UTF8.GetBytes("Third one")));

            // perform delete batch
            BlobBatchClient batch = blobServiceClient.GetBlobBatchClient();
            var res = batch.DeleteBlobs(new Uri[] { foo.Uri, bar.Uri, baz.Uri });
            Console.WriteLine(service + ": Success -- Blobs are deleted successfully.");

            return new Tuple<bool, object>(true, res);
        }
        catch (Exception e)
        {
            Console.WriteLine(service + ": Fail -- Blobs are not deleted. Error: " + e.Message);
            return new Tuple<bool, object>(false, e);
        }
    }

    // submit a batch operation (inlduing creation/updates/deletion) with try except block
    public Tuple<bool, object> SubmitBatch()
    {
        try
        {
            // Create three blobs named "foo", "bar", and "baz"
            BlobClient foo = containerClient.GetBlobClient("foo");
            BlobClient bar = containerClient.GetBlobClient("bar");
            BlobClient baz = containerClient.GetBlobClient("baz");
            foo.Upload(BinaryData.FromString("Foo!"));
            foo.CreateSnapshot();
            bar.Upload(BinaryData.FromString("Bar!"));
            bar.CreateSnapshot();
            baz.Upload(BinaryData.FromString("Baz!"));

            // Create a batch with three deletes
            BlobBatchClient batchClient = blobServiceClient.GetBlobBatchClient();
            BlobBatch batch = batchClient.CreateBatch();
            batch.DeleteBlob(foo.Uri, DeleteSnapshotsOption.IncludeSnapshots);
            batch.DeleteBlob(bar.Uri, DeleteSnapshotsOption.OnlySnapshots);
            batch.DeleteBlob(baz.Uri);

            // Submit the batch
            var res = batchClient.SubmitBatch(batch);

            return new Tuple<bool, object>(true, res);
        }
        catch (Exception e)
        {
            Console.WriteLine(service + ": Fail -- Batch operation is not submitted. Error: " + e.Message);
            return new Tuple<bool, object>(false, e);
        }
    }

    // set batch access tiers with try except block
    public Tuple<bool, object> SetBatchAccessTier()
    {
        try
        {
            BlobClient foo = containerClient.GetBlobClient("foo1");
            BlobClient bar = containerClient.GetBlobClient("bar2");
            BlobClient baz = containerClient.GetBlobClient("baz3");
            foo.Upload(BinaryData.FromString("Foo!"));
            bar.Upload(BinaryData.FromString("Bar!"));
            baz.Upload(BinaryData.FromString("Baz!"));

            // Set the access tier for all three blobs at once
            BlobBatchClient batch = blobServiceClient.GetBlobBatchClient();
            var res = batch.SetBlobsAccessTier(new Uri[] { foo.Uri, bar.Uri, baz.Uri }, AccessTier.Cool);

            return new Tuple<bool, object>(true, res);
        }
        catch (Exception e)
        {
            Console.WriteLine(service + ": Fail -- Batch access tiers are not set. Error: " + e.Message);
            return new Tuple<bool, object>(false, e);
        }
    }


}
