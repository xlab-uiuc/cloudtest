using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Batch;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace DotnetOps
{
    class Program
    {
        static void Main()
        {
            MyContainerClient containerClient = new MyContainerClient();

            Tuple<bool, object> result = containerClient.DeleteBlobs();

            if (result.Item1)
            {
                Console.WriteLine("Blobs deleted successfully.");
            }
            else
            {
                Console.WriteLine("Failed to delete blobs. Error: " + result.Item2);
            }

            Tuple<bool, object> result2 = containerClient.SubmitBatch();

            if (result2.Item1)
            {
                Console.WriteLine("Batch operation submitted successfully.");
            }
            else
            {
                Console.WriteLine("Failed to submit batch operation. Error: " + result2.Item2);
            }

        }
    }
}
