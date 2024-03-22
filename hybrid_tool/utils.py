import requests, os, re
import hashlib, json
import random

# Dictionary to store random strings and their replacements
replacement_dict = {}
random.seed(0)

def set_seed(seed=0):
    random.seed(seed)

def reset_replacement_dict():
    global replacement_dict
    replacement_dict = {}
    

def hash_request(request):
    # Extract important fields from the request
    method = request.method
    url = request.pretty_url
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['content-length', 'content-md5' ,'x-ms-blob-content-md5', 'x-ms-meta-_messageId', 'user-agent', 'if-match', 'authorization', 'x-ms-client-request-id', 'x-ms-date']}
    params = request.query
    body = request.text


    # Combine all the fields into a string
    combined_data = f"{method}|{url}|{headers}|{params}|{body}"

    combined_data = mask_with_replacement_tracking(combined_data)

    # write combined data to a proxy_logs.txt
    with open("proxy_logs.txt", "a") as f:
        f.write(f"To be hashed data: {combined_data}\n\n")

    # Hash the combined data
    hash_value = hashlib.sha256(combined_data.encode()).hexdigest()
    return hash_value

# ping to one server is enough now hence removed the other two
def ping(message, type='check'):
    params = {'message': message}

    # TO-DO: Get default ports from config
    url1 = 'http://localhost:10000/'  # Replace with your server's URL

    try:
        response1 = requests.get(url1, params=params)

        if type == 'check' and response1.headers["reference-run"] == "True": 
            return "True"
        else:
            return "False"
        
    except requests.exceptions.RequestException as e:
        print(f'Ping failed! Error: {e}')


def load_config():
    with open('config.json') as f:
        config = json.load(f)
    return config

def get_hashes():
    with open('hashes.json') as f:
        hash = json.load(f)
    return hash

def get_cur_hashes():
    with open('cur_hashes.json') as f:
        hash = json.load(f)
    return hash

def save_hashes(hash):
    with open('hashes.json', 'w') as f:
        f.write(json.dumps(hash, indent=4))

def save_cur_hashes(hash):
    with open('cur_hashes.json', 'w') as f:
        f.write(json.dumps(hash, indent=4))

def load_tags():
    with open('tags.json') as f:
        tags = json.load(f)
    return tags

def save_tags(tags):
    with open('tags.json', 'w') as f:
        f.write(json.dumps(tags, indent=4))

def save_results(results):
    with open('results.json', 'w') as f:
        f.write(json.dumps(results, indent=4))
    print(json.dumps(results, indent=4))


def get_replacement(pattern, replacement, match):

    global replacement_dict
    
    original_text = match.group(0)
    if original_text in replacement_dict:
        return replacement_dict[original_text]
    else:
        # random int
        replacement_text = replacement + str(random.randint(0, 100000))
        replacement_dict[original_text] = replacement_text
        return replacement_text
        

def mask_with_replacement_tracking(data_):
    
    patterns = [
        (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z', 'TIMESTAMP'),
        (r'\b\d+ms\b', 'U_AGENT'),
        (r'\b\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d{3}\b', 'TIMESTAMP'),
        (r'\b\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d{3}-\d{1}\b', 'TIMESTAMP'),
        (r'\b\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d{3}-\d{2}\b', 'TIMESTAMP'),
        (r'\b\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d{3}-\d{3}\b', 'TIMESTAMP'),
        (r'\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d+', 'TIME'),
        (r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', 'UUID'),
        (r'\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} GMT', 'HTTP_DATE'),
        (r'devstoreaccount1:[A-Za-z0-9+/]+={0,2}', 'KEY_REMOVED'),
        (r'"lastModifiedInMS":\d+', ''),
        (r'"user-agent":"[^"]*"', 'U_AGENT'),
        (r'TotalTimeInMS=\d+\s', 'U_AGENT'),
        (r'\b[0-9a-fA-F]{32}\b', 'TOKEN_REMOVED'),
        (r'offset:\d+\s', 'OFFSET'),
        (r'popreceipt=.*?(?=(?:\s|$))', 'POP'),
        (r'sr=c&si=test-policy&sig=[^&]+', 'CONN'),
        (r'sr=[^&]+&sig=[^&]+&st=[^&]+&se=[^&]+&sp=[^&]+', 'CONN2'),
        (r'snowmakertest\d+', 'NAME'),
        (r'"if-match":"[^"]*"', 'IF'),
        (r'IF0x[0-9A-Fa-f]+', 'IF'),
        (r"(sig',\s*')[^']+", 'SIG'),
        (r"PartitionKey='[^']+'", 'PartitionKey'),
        (r"RowKey='[^']+'", 'RowKey'),
        (r'\b[A-Z]_[a-zA-Z0-9]*\b', 'KEY'),
        (r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}', 'UUID'),
        (r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', 'UUID'),
        (r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}-[a-fA-F0-9]{1}', 'UUID_EXT'),
        (r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}-[a-fA-F0-9]{2}', 'UUID_EXT'),
        (r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{3}-[a-fA-F0-9]{12}-[a-fA-F0-9]{3}', 'UUID_EXT'),
        (r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{3}-[a-fA-F0-9]{12}-[a-fA-F0-9]{4}', 'UUID_EXT'),
        (r'\d{4}-\d{2}-\d{2}T\d{2}%3A\d{2}%3A\d{2}\.\d+Z', 'DT'),
        (r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+\sGMT', 'TIME'),
        (r'\d{2}:\d{2}:\d{2}\sUTC', 'TIME'),
        (r'"Port":"[^"]+"|"Generation":"[^"]+"|"PartitionKey":"[^"]+"|"RowKey":"[^"]+"|"ProxyPort":"[^"]+"|"Data":"[^"]+"|"StringData":"[^"]+"|"TableName":"[^"]+"|"D":"[^"]+"|"E":"[^"]+"', 'JSON'),
        (r"Tables\('([^']+?)'\)", 'TABLE'),
        (r'/t[\w]+\(PartitionKey,RowKey\)', 'TABLE_STRUCTURE'),
        (r'devstoreaccount1/t[\w]+\?\$format', 'TABLE_FORMAT'),
        (r'devstoreaccount1/t[\w]+/TimerExecutionService', 'TABLE_SERVICE'),
        (r'devstoreaccount1/t[\w]+\(\)\?\$format=application', 'TABLE_FORMAT_APP'),
        (r'devstoreaccount1/t[\w]+\?restype=container', 'TABLE_CONTAINER'),
        (r'devstoreaccount1/t[\w]+\?comp=list', 'TABLE_LIST'),
        (r'devstoreaccount1/t[\w]+/some-lease', 'TABLE_LEASE'),
        (r'devstoreaccount1/t[\w]+/[\d]+', 'TABLE_COUNT'),
        (r'&NextTableName=.*?-', 'TABLE_NEXT'),
        (r"\('NextTableName',.*?\)", 'TABLE_NEXT_SPEC'),
        (r"PartitionKey%20eq%20%27[^%]+", 'PartitionKeyEQ'),
        (r"PartitionKey%20lt%20%27[^%]+", 'PartitionKeyLT'),
        (r"PartitionKey%20le%20%27[^%]+", 'PartitionKeyLE'),
        (r"PartitionKey%20gt%20%27[^%]+", 'PartitionKeyGT'),
        (r"PartitionKey%20ge%20%27[^%]+", 'PartitionKeyGE'),
        (r"\(PartitionKey eq '.*?'\)", 'PartitionKey_SPEC_EQ'),
        (r"\(PartitionKey lt '.*?'\)", 'PartitionKey_SPEC_LT'),
        (r"\(PartitionKey le '.*?'\)", 'PartitionKey_SPEC_LE'),
        (r"\(PartitionKey gt '.*?'\)", 'PartitionKey_SPEC_GT'),
        (r"\(PartitionKey ge '.*?'\)", 'PartitionKey_SPEC_GE'),
        (r"RowKey%20eq%20%27[^%]+", 'RowKeyEQ'),
        (r"RowKey%20lt%20%27[^%]+", 'RowKeyLT'),
        (r"RowKey%20le%20%27[^%]+", 'RowKeyLE'),
        (r"RowKey%20gt%20%27[^%]+", 'RowKeyGT'),
        (r"RowKey%20ge%20%27[^%]+", 'RowKeyGE'),
        (r"\(RowKey eq '.*?'\)", 'RowKey_SPEC_EQ'),
        (r"\(RowKey lt '.*?'\)", 'RowKey_SPEC_LT'),
        (r"\(RowKey le '.*?'\)", 'RowKey_SPEC_LE'),
        (r"\(RowKey gt '.*?'\)", 'RowKey_SPEC_GT'),
        (r"\(RowKey ge '.*?'\)", 'RowKey_SPEC_GE'),
        (r'<MessageText>.*?</MessageText>', 'MSG_TEXT'),
        (r'Streams[a-fA-F0-9]{32}', 'STREAM_ID'),
        (r'\'popreceipt\',\s*\'[a-zA-Z0-9]+\'', 'POP_RECEIPT'),
        (r'"popreceipt",\s*"[a-zA-Z0-9]+"', 'POP_RECEIPT'),
        (r'"SuspectingSilos":"[^"]+"', 'SUSPECTING_SILOS'),
        (r'"ClaimValue":"[^"]+"', 'CLAIM_VALUE'),
        (r'"RoleName":"[^"]+"', 'ROLE_NAME'),
        (r'"Name":"[^"]+"', 'NAME'),
        (r'"NormalizedName":"[^"]+"', 'NORMALIZED_NAME'),
        (r'"ConcurrencyStamp":"[^"]+"', 'CONCURRENCY_STAMP'),
        (r'"SecurityStamp":"[^"]+"', 'SECURITY_STAMP'),
        (r'devstoreaccount1/.+-.+-\d{2}', "RESOURCE"),
        (r"('Content-MD5':\s*'.*?'),?", 'CONTENT_MD5'),

    ]
    
    
    # Process each pattern
    for pattern, replacement in patterns:
        data_ = re.sub(pattern, lambda match: get_replacement(pattern, replacement, match), data_)
    
    # Handling specific fields to remove
    fields_to_remove = ['NormalizedEmail', 'PasswordHash', 'SecurityStamp', 'PhoneNumber']
    for field in fields_to_remove:
        data_ = re.sub(rf'"{field}":\s*"[^"]*"', f'"{field}": ""', data_)

    return data_

