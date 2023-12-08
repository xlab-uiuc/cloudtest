import requests, os, re
import hashlib, json
# import fcntl


def hash_request(request):
    # Extract important fields from the request
    method = request.method
    url = request.pretty_url
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['content-length', 'x-ms-blob-content-md5', 'x-ms-meta-_messageId', 'user-agent', 'if-match', 'authorization', 'x-ms-client-request-id', 'x-ms-date']}
    params = request.query
    body = request.text


    # Combine all the fields into a string
    combined_data = f"{method}|{url}|{headers}|{params}|{body}"

    combined_data = hash(combined_data)

    # write combined data to a proxy_logs.txt
    with open("proxy_logs.txt", "a") as f:
        f.write(f"To be hashed data: {combined_data}\n\n")

    # Hash the combined data
    hash_value = hashlib.sha256(combined_data.encode()).hexdigest()
    return hash_value


def ping(message):
    params = {'message': message}

    # TO-DO: Get default ports from config
    url1 = 'http://localhost:10000/'  # Replace with your server's URL
    url2 = 'http://localhost:10001/'  # Replace with your server's URL
    url3 = 'http://localhost:10002/'  # Replace with your server's URL

    try:
        response1 = requests.get(url1, params=params)
        response2 = requests.get(url2, params=params)
        response3 = requests.get(url3, params=params)
        # print(response.headers)
        if response1.headers["reference-run"] == "True" or response2.headers["reference-run"] == "True" or response3.headers["reference-run"] == "True":
            return "True"
        else:
            return "False"
        
    except requests.exceptions.RequestException as e:
        print(f'Ping failed! Error: {e}')


def write_env(env, rel_path):
    with open(os.path.join(rel_path, '.test_env'), 'w') as f:
        f.write(json.dumps(env, indent=4))

def load_config():
    with open('config.json') as f:
        config = json.load(f)
    return config

def load_env():
    with open('.test_env') as f:
        env = json.load(f)
    return env

def get_hashes():
    with open('hashes.json') as f:
        # fcntl.flock(f, fcntl.LOCK_EX)
        hash = json.load(f)
        # fcntl.flock(f, fcntl.LOCK_UN)
    return hash

def get_cur_hashes():
    with open('cur_hashes.json') as f:
        # fcntl.flock(f, fcntl.LOCK_EX)
        hash = json.load(f)
        # fcntl.flock(f, fcntl.LOCK_UN)
    return hash

def save_hashes(hash):
    with open('hashes.json', 'w') as f:
        # fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(hash, indent=4))
        # fcntl.flock(f, fcntl.LOCK_UN)

def save_cur_hashes(hash):
    with open('cur_hashes.json', 'w') as f:
        # fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(hash, indent=4))
        # fcntl.flock(f, fcntl.LOCK_UN)

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


def hash(data_):

    timestamp_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z'
    time_pattern1 = r'\b\d+ms\b'
    time_pattern2 = r'\b\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d{3}\b'
    time_pattern2_1 = r'\b\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d{3}-\d{1}\b'
    time_pattern2_2 = r'\b\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d{3}-\d{2}\b'
    time_pattern2_3 = r'\b\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d{3}-\d{3}\b'
    time_pattern3 = r'\d{4}-\d{2}-\d{2}t\d{2}-\d{2}-\d{2}-\d+'
    uuid_pattern = r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b'
    http_date_pattern = r'\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} GMT'
    key_pattern = r'devstoreaccount1:[A-Za-z0-9+/]+={0,2}'
    last_modified_pattern = r'"lastModifiedInMS":\d+'
    user_agent_pattern = r'"user-agent":"[^"]*"'
    pattern = r'TotalTimeInMS=\d+\s'
    token_pattern = r'\b[0-9a-fA-F]{32}\b'
    offset_pattern = r'offset:\d+\s'
    pop_receipt = r'popreceipt=.*?(?=(?:\s|$))'
    sig_token = r'sr=c&si=test-policy&sig=[^&]+'
    sig_token1 = r'sr=[^&]+&sig=[^&]+&st=[^&]+&se=[^&]+&sp=[^&]+'
    name_pattern = r'snowmakertest\d+'
    if_pattern = r'"if-match":"[^"]*"'
    ifo_pattern = r'IF0x[0-9A-Fa-f]+'
    sig_pattern = r"(sig',\s*')[^']+"
    pattern_partition_key = r"PartitionKey='[^']+'"
    pattern_row_key = r"RowKey='[^']+'"
    keys_pattern = r'\b[A-Z]_[a-zA-Z0-9]*\b'
    uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
    uuid_ext_pattern1 = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}-[a-f0-9]{1}'
    uuid_ext_pattern2 = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}-[a-f0-9]{2}'
    uuid_ext_pattern3 = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{3}-[a-f0-9]{12}-[a-f0-9]{3}'
    uuid_ext_pattern4 = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{3}-[a-f0-9]{12}-[a-f0-9]{4}'
    dt_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}%3A\d{2}%3A\d{2}\.\d+Z'
    time_pattern4 = r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+\sGMT'
    time_pattern5 = r'\d{2}:\d{2}:\d{2}\sUTC'
    json_pattern = r'"Port":"[^"]+"|"Generation":"[^"]+"|"PartitionKey":"[^"]+"|"RowKey":"[^"]+"|"ProxyPort":"[^"]+"|"Data":"[^"]+"|"StringData":"[^"]+"|"TableName":"[^"]+"|"D":"[^"]+"|"E":"[^"]+"'
    tablename_pattern = r"Tables\('([^']+?)'\)"
    tablename_pattern_1 = r'/t[\w]+\(PartitionKey,RowKey\)'
    tablename_pattern_2 = r'devstoreaccount1/t[\w]+\?\$format'
    tablename_pattern_3 = r'devstoreaccount1/t[\w]+/TimerExecutionService'
    tablename_pattern_4 = r'devstoreaccount1/t[\w]+\(\)\?\$format'
    tablename_pattern_5 = r'devstoreaccount1/t[\w]+\?restype=container'
    tablename_pattern_6 = r'devstoreaccount1/t[\w]+\?comp=list'
    tablename_pattern_7 = r'devstoreaccount1/t[\w]+/some-lease'
    tablename_pattern_8 = r'devstoreaccount1/t[\w]+/[\d]+'
    tablename_pattern_9 = r'&NextTableName=.*?-'
    tablename_pattern_10 = r"\('NextTableName',.*?\)"
    partition_key_pattern1 = r"PartitionKey%20eq%20%27[^%]+"
    partition_key_pattern2 = r"PartitionKey%20le%20%27[^%]+"
    partition_key_pattern3 = r"PartitionKey%20ge%20%27[^%]+"
    partition_key_pattern4 = r"\(PartitionKey eq '.*?'\)"
    partition_key_pattern5 = r"\(PartitionKey le '.*?'\)"
    partition_key_pattern6 = r"\(PartitionKey ge '.*?'\)"
    row_key_pattern1 = r"RowKey%20eq%20%27[^%]+"
    row_key_pattern2 = r"RowKey%20le%20%27[^%]+"
    row_key_pattern3 = r"RowKey%20ge%20%27[^%]+"
    row_key_pattern4 = r"\(RowKey eq '.*?'\)"
    row_key_pattern5 = r"\(RowKey le '.*?'\)"
    row_key_pattern6 = r"\(RowKey ge '.*?'\)"
    msg_pattern = r'<MessageText>.*?</MessageText>'
    silo_pattern = r'\d+@\d+'

    # Replace timestamps, UUIDs, and HTTP dates with a placeholder
    data_ = re.sub(timestamp_pattern, 'TIMESTAMP', data_)
    data_ = re.sub(time_pattern2, 'TIMESTAMP', data_)
    data_ = re.sub(uuid_pattern, 'UUID', data_)
    data_ = re.sub(http_date_pattern, 'HTTP_DATE', data_)
    data_ = re.sub(key_pattern, 'KEY_REMOVED', data_)
    data_ = re.sub(last_modified_pattern, '', data_)
    data_ = re.sub(user_agent_pattern, 'U_AGENT', data_)
    data_ = re.sub(pattern, 'U_AGENT', data_)
    data_ = re.sub(time_pattern1, 'U_AGENT', data_)
    data_ = re.sub(token_pattern, 'TOKEN_REMOVED', data_)
    data_ = re.sub(offset_pattern, 'OFFSET', data_)
    data_ = re.sub(pop_receipt, 'POP', data_)
    data_ = re.sub(sig_token, 'CONN', data_)
    data_ = re.sub(sig_token1, 'CONN2', data_)
    data_ = re.sub(name_pattern, 'NAME', data_)
    data_ = re.sub(if_pattern, 'IF', data_)
    data_ = re.sub(ifo_pattern, 'IF', data_)
    data_ = re.sub(sig_pattern, 'SIG', data_)
    data_ = re.sub(pattern_partition_key, 'PartitionKey', data_)
    data_ = re.sub(pattern_row_key, 'RowKey', data_)
    data_ = re.sub(keys_pattern, 'KEY', data_)
    data_ = re.sub(uuid_pattern, 'UUID', data_)
    data_ = re.sub(uuid_ext_pattern1, 'UUID', data_)
    data_ = re.sub(uuid_ext_pattern2, 'UUID', data_)
    data_ = re.sub(uuid_ext_pattern3, 'UUID', data_)
    data_ = re.sub(uuid_ext_pattern4, 'UUID', data_)
    data_ = re.sub(dt_pattern, 'DT', data_)
    data_ = re.sub(time_pattern2, 'TIME', data_)
    data_ = re.sub(time_pattern2_1, 'TIME', data_)
    data_ = re.sub(time_pattern2_2, 'TIME', data_)
    data_ = re.sub(time_pattern2_3, 'TIME', data_)
    data_ = re.sub(time_pattern3, 'TIME', data_)
    data_ = re.sub(time_pattern4, 'TIME', data_)
    data_ = re.sub(time_pattern5, 'TIME', data_)
    data_ = re.sub(json_pattern, 'JSON', data_)
    data_ = re.sub(msg_pattern, 'MSG', data_)
    data_ = re.sub(tablename_pattern, 'TABLE', data_)
    data_ = re.sub(tablename_pattern_1, 'TABLE(PartitionKey,RowKey)', data_)
    data_ = re.sub(tablename_pattern_2, 'devstoreaccount1/TABLE?$format=application', data_)
    data_ = re.sub(tablename_pattern_3, 'devstoreaccount1/TABLE/TimerExecutionService', data_)
    data_ = re.sub(tablename_pattern_4, 'devstoreaccount1/TABLE()?$format=application', data_)
    data_ = re.sub(tablename_pattern_5, 'devstoreaccount1/TABLE?restype=container', data_)
    data_ = re.sub(tablename_pattern_6, 'devstoreaccount1/TABLE?comp=list', data_)
    data_ = re.sub(tablename_pattern_7, 'devstoreaccount1/TABLE/some-lease', data_)
    data_ = re.sub(tablename_pattern_8, 'devstoreaccount1/TABLE/count', data_)
    data_ = re.sub(tablename_pattern_9, '&NextTableName=TABLE-', data_)
    data_ = re.sub(tablename_pattern_10, "('NextTableName',TABLE)", data_)
    data_ = re.sub(partition_key_pattern1, 'PartitionKeyeqkey', data_)
    data_ = re.sub(partition_key_pattern2, 'PartitionKeylekey', data_)
    data_ = re.sub(partition_key_pattern3, 'PartitionKeygekey', data_)
    data_ = re.sub(partition_key_pattern4, 'PartitionKey eq key', data_)
    data_ = re.sub(partition_key_pattern5, 'PartitionKey le key', data_)
    data_ = re.sub(partition_key_pattern6, 'PartitionKey ge key', data_)
    data_ = re.sub(row_key_pattern1, 'RowKeyeqkey', data_)
    data_ = re.sub(row_key_pattern2, 'RowKeylekey', data_)
    data_ = re.sub(row_key_pattern3, 'RowKeygekey', data_)
    data_ = re.sub(row_key_pattern4, 'RowKey eq key', data_)
    data_ = re.sub(row_key_pattern5, 'RowKey le key', data_)
    data_ = re.sub(row_key_pattern6, 'RowKey ge key', data_)
    data_ = re.sub(silo_pattern, 'SILO', data_)
    



    fields_to_remove = ['NormalizedEmail', 'PasswordHash', 'SecurityStamp', 'PhoneNumber']

    for field in fields_to_remove:
        data_ = re.sub(rf'"{field}":\s*"[^"]*"', f'"{field}": ""', data_)


    return data_

 