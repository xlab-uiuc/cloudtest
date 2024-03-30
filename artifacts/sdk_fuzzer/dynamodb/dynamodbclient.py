import datetime
import boto3, random



# dynamodb client class
class DynamoDBClient:
    def __init__(self, emulator=True, table_name=None):
        
        if table_name is None:
            self.table_name = f'table{random.randint(1, 1000000000)}'
        else:
            self.table_name = table_name

        # connection string
        if not emulator:
            self.service = '**AWS**'
            AWS_PROFILE = 'aws'
            self.url = 'REDACTED'
        else:
            self.service = '**EMULATOR**'
            AWS_PROFILE = 'localstack'
            self.url = 'http://localhost:4566'


        self.region = 'us-east-2'
        boto3.setup_default_session(profile_name=AWS_PROFILE)
        try:
            self.client = boto3.client('dynamodb', endpoint_url=self.url, region_name=self.region)
            print(self.service, ': DynamoDB client created')
        except Exception as e:
            print(self.service, ': DynamoDB client creation failed; error: ', e)
            return
        try:
            self.client.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'username',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'last_name',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'last_name',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            print(f'{self.service}: Table name {self.table_name} created')
        except Exception as e:
            print(self.service, ': Table creation failed; error: ', e)


    # batch execute statement
    def dynamo_batch_execute_statement(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append([
                {
                    'Statement': 'string',
                    'Parameters': [
                        {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {}
                            },
                            'L': [
                                {},
                            ],
                        },
                    ],
                    'ConsistentRead': True
                },
        ])
        try:
            res = self.client.batch_execute_statement(
                Statements=args[0]
            )
            print(self.service, ': Success -- Batch execute statement succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Batch execute statement failed; error: ', e)
            return False, e

    # batch get item
    def dynamo_batch_get_item(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append([
                {
                    'username': {
                        'S': 'johndoe'
                    },
                    'last_name': {
                        'S': 'doe'
                    }
                },
            ])
        try:
            res = self.client.batch_get_item(
                RequestItems={
                    self.table_name: {
                        'Keys': args[0],
                        'AttributesToGet': [
                            'string',
                        ],
                        'ConsistentRead': True
                    }
                }
            )
            print(self.service, ': Success -- Batch get item succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Batch get item failed; error: ', e)
            return False, e
        
    
    # batch write item
    def dynamo_batch_write_item(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append([
                {
                    'PutRequest': {
                        'Item': {
                            'username': {
                                'S': 'johndoe'
                            },
                            'last_name': {
                                'S': 'doe'
                            },
                            'age': {
                                'N': '25'
                            }
                        }
                    }
                },
            ])
        try:
            res = self.client.batch_write_item(
                RequestItems={
                    self.table_name: args[0]
                }
            )
            print(self.service, ': Success -- Batch write item succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Batch write item failed; error: ', e)
            return False, e



    # can paginate
    def dynamo_can_paginate(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('list_tables')
        try:
            res = self.client.can_paginate(args[0])
            print(self.service, ': Success -- Can paginate succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Can paginate failed; error: ', e)
            return False, e
        
    # close
    def dynamo_close(self, args):
        args = list(args)
        
        try:
            res = self.client.close()
            print(self.service, ': Success -- Close succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Close failed; error: ', e)
            return False, e

    #!! Emulator: Unknown operation
    # create backup
    def dynamo_create_backup(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append('backup')
        try:
            res = self.client.create_backup(
                TableName=args[0],
                BackupName=args[1]
            )
            print(self.service, ': Success -- Create backup succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Create backup failed; error: ', e)
            return False, e
        

    # create global table
    def dynamo_create_global_table(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.create_global_table(
                GlobalTableName=args[0],
                ReplicationGroup=[
                    {
                        'RegionName': 'us-east-2'
                    },
                ]
            )
            print(self.service, ': Success -- Create global table succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Create global table failed; error: ', e)
            return False, e
        

    # create global table with streams enabled
    def dynamo_create_global_table_v2(self, args):
        args = list(args)

        if not len(args) > 0:
            args.append(f'table{random.randint(1, 100)}')
        
        try:
            try:
                self.client.create_table(
                    TableName=args[0],
                    KeySchema=[
                        {
                            'AttributeName': 'username',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'last_name',
                            'KeyType': 'RANGE'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'username',
                            'AttributeType': 'S'
                        },
                        {
                            'AttributeName': 'last_name',
                            'AttributeType': 'S'
                        },
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    },
                    StreamSpecification={
                        'StreamEnabled': True,
                        'StreamViewType': 'NEW_AND_OLD_IMAGES'
                    }
                )
                print(f'{self.service}: Table name {args[0]} created for global table')
            except Exception as e:
                print(self.service, ': Table creation failed for global table; error: ', e)

            res = self.client.create_global_table(
                GlobalTableName=args[0],
                ReplicationGroup=[
                    {
                        'RegionName': 'us-east-2'
                    },
                ]
            )
            print(self.service, ': Success -- Create global table succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Create global table failed; error: ', e)
            return False, e
    

    # create table
    def dynamo_create_table(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'table{random.randint(1, 10000000)}')
        if not len(args) > 1:
            args.append([
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'last_name',
                    'KeyType': 'RANGE'
                }
            ])
        try:
            res = self.client.create_table(
                TableName=args[0],
                KeySchema=args[1],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'last_name',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            print(self.service, ': Success -- Table created')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Table creation failed; error: ', e)
            return False, e

    #!! Emulator: Unknown operation
    # delete backup
    def dynamo_delete_backup(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'arn:aws:dynamodb:us-east-2:818637742267:table/{self.table_name}/backup/01548148148148148148')
        try:
            res = self.client.delete_backup(
                BackupArn=args[0]
            )
            print(self.service, ': Success -- Delete backup succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Delete backup failed; error: ', e)
            return False, e


    # delete item
    def dynamo_delete_item(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append({
                'username': {
                    'S': 'johndoe'
                },
                'last_name': {
                    'S': 'doe'
                }
            })
        try:
            res = self.client.delete_item(
                TableName=self.table_name,
                Key=args[0]
            )
            print(self.service, ': Success -- Delete item succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Delete item failed; error: ', e)
            return False, e
        

    # delete table
    def dynamo_delete_table(self, args):
        args = list(args)
        
        try:
            res = self.client.delete_table(
                TableName=self.table_name
            )
            print(self.service, ': Success -- Delete table succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Delete table failed; error: ', e)
            return False, e



    #!! Emulator: Unknown operation
    # describe backup
    def dynamo_describe_backup(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'arn:aws:dynamodb:us-east-2:818637742267:table/{self.table_name}/backup/01548148148148148148')
        try:
            res = self.client.describe_backup(
                BackupArn=args[0]
            )
            print(self.service, ': Success -- Describe backup succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe backup failed; error: ', e)
            return False, e
        
    
    # describe continuous backups
    def dynamo_describe_continuous_backups(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.describe_continuous_backups(
                TableName=args[0]
            )
            print(self.service, ': Success -- Describe continuous backups succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe continuous backups failed; error: ', e)
            return False, e
        

    # describe contributor insights
    def dynamo_describe_contributor_insights(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.describe_contributor_insights(
                TableName=args[0]
            )
            print(self.service, ': Success -- Describe contributor insights succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe contributor insights failed; error: ', e)
            return False, e
        
    # deccribe endpoints
    def dynamo_describe_endpoints(self, args):
        args = list(args)
        
        try:
            res = self.client.describe_endpoints()
            print(self.service, ': Success -- Describe endpoints succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe endpoints failed; error: ', e)
            return False, e
        
    # describe exports
    def dynamo_describe_export(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'arn:aws:dynamodb:us-east-2:818637742267:table/{self.table_name}')
        try:
            res = self.client.describe_export(
                ExportArn=args[0]
            )
            print(self.service, ': Success -- Describe exports succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe exports failed; error: ', e)
            return False, e
        
    # describe global table
    def dynamo_describe_global_table(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            # self.dynamo_create_global_table_v2(args)
            res = self.client.describe_global_table(
                GlobalTableName=args[0]
            )
            print(self.service, ': Success -- Describe global table succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe global table failed; error: ', e)
            return False, e
        

    #!! Emulator: Unknown operation   
    # describe global table settings
    def dynamo_describe_global_table_settings(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.describe_global_table_settings(
                GlobalTableName=args[0]
            )
            print(self.service, ': Success -- Describe global table settings succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe global table settings failed; error: ', e)
            return False, e

    #!! Emulator: Unknown operation
    # describe import
    def dynamo_describe_import(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('import-task-id-12121-1-21-21-12-12-12-12-23-23-1-2')
        try:
            res = self.client.describe_import(
                ImportArn=args[0]
            )
            print(self.service, ': Success -- Describe import succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe import failed; error: ', e)
            return False, e
        
    # decribe kinesis streaming destination
    def dynamo_describe_kinesis_streaming_destination(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.describe_kinesis_streaming_destination(
                TableName=args[0]
            )
            print(self.service, ': Success -- Describe kinesis streaming destination succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe kinesis streaming destination failed; error: ', e)
            return False, e
        

    # describe limits
    def dynamo_describe_limits(self, args):
        args = list(args)
        
        try:
            res = self.client.describe_limits()
            print(self.service, ': Success -- Describe limits succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe limits failed; error: ', e)
            return False, e
        
    
    # describe table
    def dynamo_describe_table(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.describe_table(
                TableName=args[0]
            )
            print(self.service, ': Success -- Describe table succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe table failed; error: ', e)
            return False, e



    #!! Emulator: Unknown operation
    # describe table replication auto scaling
    def dynamo_describe_table_replication_auto_scaling(self, args):
        args = list(args)
        
        try:
            res = self.client.describe_table_replica_auto_scaling(
                TableName=self.table_name
            )
            print(self.service, ': Success -- Describe table replication auto scaling succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe table replication auto scaling failed; error: ', e)
            return False, e
        

    # describe time to live
    def dynamo_describe_time_to_live(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.describe_time_to_live(
                TableName=args[0]
            )
            print(self.service, ': Success -- Describe time to live succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Describe time to live failed; error: ', e)
            return False, e

    # disable kinesis streaming destination
    def dynamo_disable_kinesis_streaming_destination(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append('arn:aws:kinesis:us-east-2:818637742267:stream/my_stream')
        try:
            res = self.client.disable_kinesis_streaming_destination(
                TableName=args[0],
                StreamArn=args[1]
            )
            print(self.service, ': Success -- Disable kinesis streaming destination succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Disable kinesis streaming destination failed; error: ', e)
            return False, e
        
    # enable kinesis streaming destination
    def dynamo_enable_kinesis_streaming_destination(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append('arn:aws:kinesis:us-east-2:818637742267:stream/my_stream')
        try:
            res = self.client.enable_kinesis_streaming_destination(
                TableName=args[0],
                StreamArn=args[1]
            )
            print(self.service, ': Success -- Enable kinesis streaming destination succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Enable kinesis streaming destination failed; error: ', e)
            return False, e
    

    # execute statement
    def dynamo_execute_statement(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('SELECT * FROM ' + self.table_name)
        try:
            res = self.client.execute_statement(
                Statement=args[0]
            )
            print(self.service, ': Success -- Execute statement succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Execute statement failed; error: ', e)
            return False, e
    

    # # execute transaction
    def dynamo_execute_transaction(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append([ 
            { 
                "Parameters": [ 
                    { 
                    "B": 'GhpcyB0ZXh0IGlzIGJhc2U2NC1l',
                    "BOOL": True,
                    "BS": [ 'GhpcyB0ZXh0IGlzIGJhc2U2NC1l' ],
                    "L": [ 
                       
                    ],
                    "M": { 
                       },
                    "N": "8",
                    "NS": [ "10" ],
                    "S": "string",
                    "SS": [ "string" ]
                    }
                ],
                "Statement": "SELECT * FROM " + self.table_name,
            }
        ])
        try:
            res = self.client.execute_transaction(
                TransactStatements=args[0],
          
            )
            print(self.service, ': Success -- Execute transaction succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Execute transaction failed; error: ', e)
            return False, e
        


    #!! Emulator: Unknown operation
    # export table to point in time
    def dynamo_export_table_to_point_in_time(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(f'arn:aws:dynamodb:us-east-2:818637742267:table/{self.table_name}/backup/01548148148148148148')
        try:
            res = self.client.export_table_to_point_in_time(
                TableArn=args[0],
                S3Bucket='string'
            )
            print(self.service, ': Success -- Export table to point in time succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Export table to point in time failed; error: ', e)
            return False, e
        


    # get item
    def dynamo_get_item(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append({
                'username': {
                    'S': 'johndoe'
                },
                'last_name': {
                    'S': 'doe'
                }
            })
        try:
            res = self.client.get_item(
                TableName=self.table_name,
                Key=args[0]
            )
            print(self.service, ': Success -- Get item succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Get item failed; error: ', e)
            return False, e
        

    # get paginator
    def dynamo_get_paginator(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('list_tables')
        try:
            res = self.client.get_paginator(
                args[0]
            )
            print(self.service, ': Success -- Get paginator succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Get paginator failed; error: ', e)
            return False, e
        

    # get waiters
    def dynamo_get_waiter(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('table_exists')
        try:
            res = self.client.get_waiter(
                args[0]
            )
            print(self.service, ': Success -- Get waiter succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Get waiter failed; error: ', e)
            return False, e
        

    # !! Emulator: Unknown operation
    # import table
    def dynamo_import_table(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.import_table(
                S3BucketSource={
                'S3Bucket' : 'string',
                },
                InputFormat='DYNAMODB_JSON',
                TableCreationParameters={
                'TableName': args[0] ,
                'AttributeDefinitions':[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'last_name',
                    'AttributeType': 'S'
                },
                ],

                'KeySchema': [
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'last_name',
                    'KeyType': 'RANGE'
                }
                ],

                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                },

                }
            )
            print(self.service, ': Success -- Import table succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Import table failed; error: ', e)
            return False, e
        
    
    #!! Emulator: Unknown operation
    # list backups
    def dynamo_list_backups(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.list_backups(
                TableName=args[0]
            )
            print(self.service, ': Success -- List backups succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- List backups failed; error: ', e)
            return False, e


    #!! Emulator: Unknown operation
    # list contributor insights
    def dynamo_list_contributor_insights(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.list_contributor_insights(
                TableName=args[0]
            )
            print(self.service, ': Success -- List contributor insights succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- List contributor insights failed; error: ', e)
            return False, e
        

    #!! Emulator: Unknown operation
    # list exports
    def dynamo_list_exports(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.list_exports(
                TableArn='string'
            )
            print(self.service, ': Success -- List exports succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- List exports failed; error: ', e)
            return False, e


    # list global tables
    def dynamo_list_global_tables(self, args):
        args = list(args)
        
        try:
            self.dynamo_create_global_table_v2(args)
            res = self.client.list_global_tables()
            print(self.service, ': Success -- List global tables succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- List global tables failed; error: ', e)
            return False, e
        
    
    #!! Emulator: Unknown operation
    # list imports
    def dynamo_list_imports(self, args):
        args = list(args)
        
        try:
            res = self.client.list_imports()
            print(self.service, ': Success -- List imports succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- List imports failed; error: ', e)
            return False, e

    # list tables
    def dynamo_list_tables(self, args):
        args = list(args)
        
        try:
            res = self.client.list_tables()
            print(self.service, ': Success -- List tables succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- List tables failed; error: ', e)
            return False, e

    # list tags of resource
    def dynamo_list_tags_of_resource(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        try:
            res = self.client.list_tags_of_resource(
                ResourceArn='arn:aws:dynamodb:us-east-2:818637742267:table/' + args[0]
            )
            print(self.service, ': Success -- List tags of resource succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- List tags of resource failed; error: ', e)
            return False, e


    # put item
    def dynamo_put_item(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append({
                    'username': {
                        'S': 'johndoe'
                    },
                    'last_name': {
                        'S': 'doe'
                    }
                })
        try:
            res = self.client.put_item(
                TableName=args[0],
                Item=args[1]
            )
            print(self.service, ': Success -- Item put succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Item put failed; error: ', e)
            return False, e
        

    # query table
    def dynamo_query(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append('last_name = :v1')
        try:
            res = self.client.query(
                TableName=args[0],
                KeyConditionExpression=args[1]
            )
            print(self.service, ': Success -- Query succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Query failed; error: ', e)
            return False, e


    #!! Emulator: Unknown operation
    # restore table from backup
    def dynamo_restore_table_from_backup(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append('arn:aws:dynamodb:us-east-2:818637742267:table/' + args[0] + '/backup/0000000000000000')
        try:
            res = self.client.restore_table_from_backup(
                TargetTableName=args[0],
                BackupArn=args[1]
            )
            print(self.service, ': Success -- Restore table from backup succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Restore table from backup failed; error: ', e)
            return False, e
        
    #!! Emulator: Unknown operation
    # restore table to point in time
    def dynamo_restore_table_to_point_in_time(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append('string')
        if not len(args) > 2:
            args.append(True)
        if not len(args) > 3:
            args.append(datetime.datetime(2015, 1, 1))
        try:
            res = self.client.restore_table_to_point_in_time(
                SourceTableName=args[0],
                TargetTableName=args[1],
                UseLatestRestorableTime=args[2]
            )
            print(self.service, ': Success -- Restore table to point in time succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Restore table to point in time failed; error: ', e)
            return False, e
    

    # scan table
    def dynamo_scan(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append('string')
        if not len(args) > 2:
            args.append({
                ':val': {
                    'S': 'string',
                    'N': '1',
                    'B': b'bytes',
                    'SS': [
                        'string',
                    ],
                    'NS': [
                        '1',
                    ],
                    'BS': [
                        b'bytes',
                    ],
                    'M': {
                        'string': {}
                    },
                    'L': [
                        {},
                    ],
                }
            })
        try:
            res = self.client.scan(
                TableName=args[0],
                FilterExpression=args[1],
                ExpressionAttributeValues=args[2]
            )
            print(self.service, ': Success -- Scan succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Scan failed; error: ', e)
            return False, e
    
    # tag resource
    def dynamo_tag_resource(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('arn:aws:dynamodb:us-east-2:818637742267:table/' + self.table_name)
        if not len(args) > 1:
            args.append([
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ])
        try:
            res = self.client.tag_resource(
                ResourceArn=args[0],
                Tags=args[1]
            )
            print(self.service, ': Success -- Tag resource succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Tag resource failed; error: ', e)
            return False, e
        
    # transact get items
    def dynamo_transact_get_items(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append([
                {
                    'Get': {
                        'Key': {
                            'string': {
                                'S': 'string',
                                'N': '1',
                                'B': b'bytes',
                                'SS': [
                                    'string',
                                ],
                                'NS': [
                                    '1',
                                ],
                                'BS': [
                                    b'bytes',
                                ],
                                'M': {
                                    'string': {}
                                },
                                'L': [
                                    {},
                                ],
                            }
                        },
                        'TableName': self.table_name,
                        'ProjectionExpression': 'last_name',
                        'ExpressionAttributeNames': {
                            'string': 'string'
                        }
                    }
                },
            ])

        try:
            res = self.client.transact_get_items(TransactItems=args[0])
            print(self.service, ': Success -- Transact get items succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Transact get items failed; error: ', e)
            return False, e


    # transact write items
    def dynamo_transact_write_items(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append([{
        'Put': {
            'TableName': self.table_name,
            'Item': {
                'username': {
                    'S': "item000"
                },
                'last_name': {
                    'S': 'someData'
                }
            },
            'ConditionExpression': 'attribute_not_exists(itemId)',
            'ReturnValuesOnConditionCheckFailure': 'ALL_OLD'
        }
    }])
        try:
            res = self.client.transact_write_items(TransactItems=args[0])
            print(self.service, ': Success -- Transact write items succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Transact write items failed; error: ', e)
            return False, e



    # untag resource
    def dynamo_untag_resource(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('arn:aws:dynamodb:us-east-2:818637742267:table/' + self.table_name)
        if not len(args) > 1:
            args.append([
                'string',
            ])
        try:
            res = self.client.untag_resource(
                ResourceArn=args[0],
                TagKeys=args[1]
            )
            print(self.service, ': Success -- Untag resource succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Untag resource failed; error: ', e)
            return False, e
        

    # update continuous backups
    def dynamo_update_continuous_backups(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append({
                'PointInTimeRecoveryEnabled': True
            })
        try:
            res = self.client.update_continuous_backups(
                TableName=self.table_name,
                PointInTimeRecoverySpecification=args[0]
            )
            print(self.service, ': Success -- Update continuous backups succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Update continuous backups failed; error: ', e)
            return False, e
        

    #!! Emulator: Unknown operation
    # update contributor insights
    def dynamo_update_contributor_insights(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append('last_name')
        if not len(args) > 1:
            args.append('ENABLE')
        try:
            res = self.client.update_contributor_insights(
                TableName=self.table_name,
                IndexName=args[0],
                ContributorInsightsAction=args[1]
            )
            print(self.service, ': Success -- Update contributor insights succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Update contributor insights failed; error: ', e)
            return False, e
        

    # update global table
    def dynamo_update_global_table(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.table_name)
        if not len(args) > 1:
            args.append([
                {
                    'Create': {
                        'RegionName': 'us-east-2'
                    }
                },
            ])

        self.dynamo_create_global_table_v2(args)

        try:
            res = self.client.update_global_table(
                GlobalTableName=args[0],
                ReplicaUpdates=args[1]
            )
            print(self.service, ': Success -- Update global table succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Update global table failed; error: ', e)
            return False, e
        
    #!! Emulator: Unknown operation
    # update global table settings
    def dynamo_update_global_table_settings(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)
        
        try:
            res =self.client.update_global_table_settings(
                GlobalTableName=args[0],
                GlobalTableBillingMode='PROVISIONED',
                GlobalTableProvisionedWriteCapacityUnits=123,
                GlobalTableProvisionedWriteCapacityAutoScalingSettingsUpdate={
                    'MinimumUnits': 123,
                    'MaximumUnits': 123,
                    'AutoScalingRoleArn': 'string',
                    'ScalingPolicyUpdate': {
                        'PolicyName': 'string',
                        'TargetTrackingScalingPolicyConfiguration': {
                            'DisableScaleIn': True,
                            'ScaleInCooldown': 123,
                            'ScaleOutCooldown': 123,
                            'TargetValue': 123.0
                        }
                    }
                },
                GlobalTableGlobalSecondaryIndexSettingsUpdate=[
                    {
                        'IndexName': 'string',
                        'ProvisionedWriteCapacityUnits': 123,
                        'ProvisionedWriteCapacityAutoScalingSettingsUpdate': {
                            'MinimumUnits': 123,
                            'MaximumUnits': 123,
                            'AutoScalingDisabled': True,
                            'AutoScalingRoleArn': 'string',
                            'ScalingPolicyUpdate': {
                                'PolicyName': 'string',
                                'TargetTrackingScalingPolicyConfiguration': {
                                    'DisableScaleIn': True,
                                    'ScaleInCooldown': 123,
                                    'ScaleOutCooldown': 123,
                                    'TargetValue': 123.0
                                }
                            }
                        }
                    },
                ]
            )
            print(self.service, ': Success -- Update global table settings succeeded')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Update global table settings failed; error: ', e)
            return False, e
        

    # update item
    def dynamo_update_item(self, args):
        args = list(args)
        
        try:
            res = self.client.update_item(
                TableName=self.table_name,
                Key={
                    'username': {
                        'S': 'johndoe'
                    },
                    'last_name': {
                        'S': 'doe'
                    }
                },
                UpdateExpression='SET age = :val1',
                ExpressionAttributeValues={
                    ':val1': {
                        'N': '30'
                    }
                }
            )
            print(self.service, ': Success -- Item updated')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Item update failed; error: ', e)
            return False, e
        

    # update table
    def dynamo_update_table(self, args):
        args = list(args)
        
        if not len(args) > 0:
            args.append(self.table_name)

        try:
            res = self.client.update_table(
                TableName=args[0],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            print(self.service, ': Success -- Table updated')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Table update failed; error: ', e)
            return False, e
        

    
    #!! Emulator: Unknown operation    
    # update table replica autoscaling
    def dynamo_update_replica_autoscaling(self, args):
        args = list(args)
        
        try:
            res = self.client.update_table_replica_auto_scaling(
                TableName=self.table_name,
                GlobalSecondaryIndexUpdates=[
                    {
                            'IndexName': 'index1',
                            'ProvisionedWriteCapacityAutoScalingUpdate': {
                                'MinimumUnits': 123,
                                'MaximumUnits': 123,
                                'AutoScalingDisabled': False,
                                'AutoScalingRoleArn': 'arn:aws:iam::818637742267:role/DynamoDBAutoscaleRole',
                                'ScalingPolicyUpdate': {
                                    'PolicyName': 'WriteCapacityUnitsScalingPolicy',
                                    'TargetTrackingScalingPolicyConfiguration': {
                                        'DisableScaleIn': False,
                                        'ScaleInCooldown': 300,
                                        'ScaleOutCooldown': 300,
                                        'TargetValue': 70.0
                                    }
                                }
                            }
                    },
                ]
            )
            print(self.service, ': Success -- Replica autoscaling updated')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Replica autoscaling update failed; error: ', e)
            return False, e
        


    # update time to live
    def dynamo_update_ttl(self, args):
        args = list(args)
        
        try:
            res = self.client.update_time_to_live(
                TableName=self.table_name,
                TimeToLiveSpecification={
                    'AttributeName': 'ttl',
                    'Enabled': True
                }
            )
            print(self.service, ': Success -- TTL updated')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- TTL update failed; error: ', e)
            return False, e
        

    def __cleanup__(self):
        try:
            # list tables
            tables = self.client.list_tables()
            # delete tables
            for table in tables['TableNames']:
                try:
                    self.client.delete_table(TableName=table)
                    print('Success -- Table deleted: ', table)
                except Exception as e:
                    print('Fail -- Table delete failed; error: ', e)
        except Exception as e:
            print('Fail -- Tables listing for deletion failed; error: ', e)
        

