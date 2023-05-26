#!/usr/bin/env python3

import afl, json
import sys, os
sys.path.append('Azure Storage/')
from blobclient import BlobClient


'''Command: py-afl-fuzz -i in/ -o out/ --  ./fuzz.py'''

'''Add a txt file in the in/ directory which contains the seed input for the fuzzing process.'''


def fuzz_blob_client(data):
    
    blob_client = BlobClient(emulator=True)

    # Check the return value of the abort_copy() method.
    blob_client.abort_copy(data['copy_id'])

    

if __name__ == '__main__':

    # Fuzzing loop
    while afl.loop():
        # Read the input from AFL
        data = sys.stdin.read()

        data = json.loads(data)

        # Call the fuzzing harness function
        fuzz_blob_client(data)
        
    os._exit(0)