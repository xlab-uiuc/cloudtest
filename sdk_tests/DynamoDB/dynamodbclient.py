import datetime
import boto3, random



# dynamodb client class
class DynamoDBClient:
    def __init__(self, table_name=None, emulator=True):
        
        if table_name is None:
            self.table_name = f'table{random.randint(1, 1000000000)}'
        else:
            self.table_name = table_name

        # connection string
        if not emulator:
            self.service = 'AWS'
            AWS_PROFILE = 'aws'
            url = 'https://dynamodb.us-east-2.amazonaws.com'
        else:
            self.service = 'EMULATOR'
            AWS_PROFILE = 'localstack'
            url = 'http://localhost:4566'


        AWS_REGION = 'us-east-2'
        boto3.setup_default_session(profile_name=AWS_PROFILE)
        self.client = boto3.client('dynamodb', endpoint_url=url, region_name=AWS_REGION)
        
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


    # # create table with try except
    # def dynamo_create_table(self, table_name=None, key_schema=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     if key_schema is None:
    #         key_schema = [
    #             {
    #                 'AttributeName': 'username',
    #                 'KeyType': 'HASH'
    #             },
    #             {
    #                 'AttributeName': 'last_name',
    #                 'KeyType': 'RANGE'
    #             }
    #         ]
    #     try:
    #         self.client.create_table(
    #             TableName=table_name,
    #             KeySchema=key_schema,
    #             AttributeDefinitions=[
    #                 {
    #                     'AttributeName': 'username',
    #                     'AttributeType': 'S'
    #                 },
    #                 {
    #                     'AttributeName': 'last_name',
    #                     'AttributeType': 'S'
    #                 },
    #             ],
    #             ProvisionedThroughput={
    #                 'ReadCapacityUnits': 5,
    #                 'WriteCapacityUnits': 5
    #             }
    #         )
    #         print(self.service, ': Table created')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Table creation failed; error: ', e)
    #         return False

    # batch execute statement with try except
    def dynamo_batch_execute_statement(self, statement=None):
        if statement is None:
            statement = [
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
                            'NULL': True|False,
                            'BOOL': True|False
                        },
                    ],
                    'ConsistentRead': True|False
                },
        ]
        try:
            self.client.batch_execute_statement(
                Statements=statement
            )
            print(self.service, ': Batch execute statement succeeded')
            return True
        except Exception as e:
            print(self.service, ': Batch execute statement failed; error: ', e)
            return False

    # batch get item with try except
    def dynamo_batch_get_item(self, keys=None):
        if keys is None:
            keys = [
                {
                    'username': {
                        'S': 'johndoe'
                    },
                    'last_name': {
                        'S': 'doe'
                    }
                },
            ]
        try:
            self.client.batch_get_item(
                RequestItems={
                    self.table_name: {
                        'Keys': keys,
                        'AttributesToGet': [
                            'string',
                        ],
                        'ConsistentRead': True
                    }
                }
            )
            print(self.service, ': Batch get item succeeded')
            return True
        except Exception as e:
            print(self.service, ': Batch get item failed; error: ', e)
            return False
    
    # batch write item with try except
    def dynamo_batch_write_item(self, items=None):
        if items is None:
            items = [
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
            ]
        try:
            self.client.batch_write_item(
                RequestItems={
                    self.table_name: items
                }
            )
            print(self.service, ': Batch write item succeeded')
            return True
        except Exception as e:
            print(self.service, ': Batch write item failed; error: ', e)
            return False



    # can paginate with try except
    def dynamo_can_paginate(self, operation_name=None):
        if operation_name is None:
            operation_name = 'list_tables'
        try:
            self.client.can_paginate(operation_name)
            print(self.service, ': Can paginate succeeded')
            return True
        except Exception as e:
            print(self.service, ': Can paginate failed; error: ', e)
            return False
        

    ##!! Emulator: Unknown operation
    # # create backup with try except
    # def dynamo_create_backup(self, table_name=None, backup_name=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     if backup_name is None:
    #         backup_name = 'backup'
    #     try:
    #         self.client.create_backup(
    #             TableName=table_name,
    #             BackupName=backup_name
    #         )
    #         print(self.service, ': Create backup succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Create backup failed; error: ', e)
    #         return False
        

    # create global table with try except
    def dynamo_create_global_table(self, global_table_name=None):
        if global_table_name is None:
            global_table_name = self.table_name
        try:
            self.client.create_global_table(
                GlobalTableName=global_table_name,
                ReplicationGroup=[
                    {
                        'RegionName': 'us-east-1'
                    },
                ]
            )
            print(self.service, ': Create global table succeeded')
            return True
        except Exception as e:
            print(self.service, ': Create global table failed; error: ', e)
            return False
    

    ##!! Emulator: Unknown operation
    # # delete backup with try except
    # def dynamo_delete_backup(self, backup_arn=None):
    #     if backup_arn is None:
    #         backup_arn = 'arn:aws:dynamodb:us-east-1:123456789012:table/mytable/backup/01548148148148148148'
    #     try:
    #         self.client.delete_backup(
    #             BackupArn=backup_arn
    #         )
    #         print(self.service, ': Delete backup succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Delete backup failed; error: ', e)
    #         return False


    # delete item with try except
    def dynamo_delete_item(self, key=None):
        if key is None:
            key = {
                'username': {
                    'S': 'johndoe'
                },
                'last_name': {
                    'S': 'doe'
                }
            }
        try:
            self.client.delete_item(
                TableName=self.table_name,
                Key=key
            )
            print(self.service, ': Delete item succeeded')
            return True
        except Exception as e:
            print(self.service, ': Delete item failed; error: ', e)
            return False
        

    # # delete table with try except
    # def dynamo_delete_table(self):
    #     try:
    #         self.client.delete_table(
    #             TableName=self.table_name
    #         )
    #         print(self.service, ': Delete table succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Delete table failed; error: ', e)
    #         return False



    # #!! Emulator: Unknown operation
    # # describe backup with try except
    # def dynamo_describe_backup(self, backup_arn=None):
    #     if backup_arn is None:
    #         backup_arn = 'arn:aws:dynamodb:us-east-1:123456789012:table/mytable/backup/01548148148148148148'
    #     try:
    #         self.client.describe_backup(
    #             BackupArn=backup_arn
    #         )
    #         print(self.service, ': Describe backup succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Describe backup failed; error: ', e)
    #         return False
        
    
    # describe continuous backups with try except
    def dynamo_describe_continuous_backups(self, table_name=None):
        if table_name is None:
            table_name = self.table_name
        try:
            self.client.describe_continuous_backups(
                TableName=table_name
            )
            print(self.service, ': Describe continuous backups succeeded')
            return True
        except Exception as e:
            print(self.service, ': Describe continuous backups failed; error: ', e)
            return False
        
    # describe global table with try except
    def dynamo_describe_global_table(self, global_table_name=None):
        if global_table_name is None:
            global_table_name = self.table_name
        try:
            self.client.describe_global_table(
                GlobalTableName=global_table_name
            )
            print(self.service, ': Describe global table succeeded')
            return True
        except Exception as e:
            print(self.service, ': Describe global table failed; error: ', e)
            return False

    
    # #!! Emulator: Unknown operation   
    # # describe global table settings with try except
    # def dynamo_describe_global_table_settings(self, global_table_name=None):
    #     if global_table_name is None:
    #         global_table_name = self.table_name
    #     try:
    #         self.client.describe_global_table_settings(
    #             GlobalTableName=global_table_name
    #         )
    #         print(self.service, ': Describe global table settings succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Describe global table settings failed; error: ', e)
    #         return False

    # #!! Emulator: Unknown operation
    # # describe import with try except
    # def dynamo_describe_import(self, import_task_id=None):
    #     if import_task_id is None:
    #         import_task_id = 'import-task-id-12121-1-21-21-12-12-12-12-23-23-1-2'
    #     try:
    #         self.client.describe_import(
    #             ImportArn=import_task_id
    #         )
    #         print(self.service, ': Describe import succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Describe import failed; error: ', e)
    #         return False
        
    # decribe kinesis streaming destination with try except
    def dynamo_describe_kinesis_streaming_destination(self, table_name=None):
        if table_name is None:
            table_name = self.table_name
        try:
            self.client.describe_kinesis_streaming_destination(
                TableName=table_name
            )
            print(self.service, ': Describe kinesis streaming destination succeeded')
            return True
        except Exception as e:
            print(self.service, ': Describe kinesis streaming destination failed; error: ', e)
            return False
        

    # describe limits with try except
    def dynamo_describe_limits(self):
        try:
            self.client.describe_limits()
            print(self.service, ': Describe limits succeeded')
            return True
        except Exception as e:
            print(self.service, ': Describe limits failed; error: ', e)
            return False
        
    
    # describe table with try except
    def dynamo_describe_table(self, table_name=None):
        if table_name is None:
            table_name = self.table_name
        try:
            self.client.describe_table(
                TableName=table_name
            )
            print(self.service, ': Describe table succeeded')
            return True
        except Exception as e:
            print(self.service, ': Describe table failed; error: ', e)
            return False



    # #!! Emulator: Unknown operation
    # # describe table replication auto scaling with try except
    # def dynamo_describe_table_replication_auto_scaling(self):
    #     try:
    #         self.client.describe_table_replica_auto_scaling(
    #             TableName=self.table_name
    #         )
    #         print(self.service, ': Describe table replication auto scaling succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Describe table replication auto scaling failed; error: ', e)
    #         return False
        

    # describe time to live with try except
    def dynamo_describe_time_to_live(self, table_name=None):
        if table_name is None:
            table_name = self.table_name
        try:
            self.client.describe_time_to_live(
                TableName=table_name
            )
            print(self.service, ': Describe time to live succeeded')
            return True
        except Exception as e:
            print(self.service, ': Describe time to live failed; error: ', e)
            return False

    

    # execute statement with try except
    def dynamo_execute_statement(self, statement=None):
        if statement is None:
            statement = 'SELECT * FROM ' + self.table_name
        try:
            self.client.execute_statement(
                Statement=statement
            )
            print(self.service, ': Execute statement succeeded')
            return True
        except Exception as e:
            print(self.service, ': Execute statement failed; error: ', e)
            return False
    

    # # execute transaction with try except
    # def dynamo_execute_transaction(self, transaction_items=None):
    #     if transaction_items is None:
    #         transaction_items = [ 
    #         { 
    #             "Parameters": [ 
    #                 { 
    #                 "B": 'GhpcyB0ZXh0IGlzIGJhc2U2NC1l',
    #                 "BOOL": True,
    #                 "BS": [ 'GhpcyB0ZXh0IGlzIGJhc2U2NC1l' ],
    #                 "L": [ 
                       
    #                 ],
    #                 "M": { 
    #                    },
    #                 "N": "8",
    #                 "NS": [ "10" ],
    #                 "NULL": True,
    #                 "S": "string",
    #                 "SS": [ "string" ]
    #                 }
    #             ],
    #             "Statement": "SELECT * FROM " + self.table_name,
    #         }
    #     ]
    #     try:
    #         self.client.execute_transaction(
    #             TransactStatements=transaction_items,
          
    #         )
    #         print(self.service, ': Execute transaction succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Execute transaction failed; error: ', e)
    #         return False
        


    #!! Emulator: Unknown operation
    # # export table to point in time with try except
    # def dynamo_export_table_to_point_in_time(self, table_arn=None):
    #     if table_arn is None:
    #         table_arn = 'arn:aws:dynamodb:us-east-1:123456789012:table/mytable/backup/01548148148148148148'
    #     try:
    #         self.client.export_table_to_point_in_time(
    #             TableArn=table_arn,
    #             S3Bucket='string'
    #         )
    #         print(self.service, ': Export table to point in time succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Export table to point in time failed; error: ', e)
    #         return False
        


    # get item with try except
    def dynamo_get_item(self, key=None):
        if key is None:
            key = {
                'username': {
                    'S': 'johndoe'
                },
                'last_name': {
                    'S': 'doe'
                }
            }
        try:
            self.client.get_item(
                TableName=self.table_name,
                Key=key
            )
            print(self.service, ': Get item succeeded')
            return True
        except Exception as e:
            print(self.service, ': Get item failed; error: ', e)
            return False
        

    # get paginator with try except
    def dynamo_get_paginator(self, operation_name=None):
        if operation_name is None:
            operation_name = 'ListTables'
        try:
            self.client.get_paginator(
                operation_name
            )
            print(self.service, ': Get paginator succeeded')
            return True
        except Exception as e:
            print(self.service, ': Get paginator failed; error: ', e)
            return False
        

    # get waiters with try except
    def dynamo_get_waiter(self, waiter_name=None):
        if waiter_name is None:
            waiter_name = 'TableExists'
        try:
            self.client.get_waiter(
                waiter_name
            )
            print(self.service, ': Get waiter succeeded')
            return True
        except Exception as e:
            print(self.service, ': Get waiter failed; error: ', e)
            return False
        

    #!! Emulator: Unknown operation
    # # import table with try except
    # def dynamo_import_table(self, table_name=None, s3_bucket=None, s3_prefix=None, s3_bucket_owner=None, s3_object_version=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     try:
    #         self.client.import_table(
    #             S3BucketSource={
    #             'S3Bucket' : 'string',
    #             },
    #             InputFormat='DYNAMODB_JSON',
    #             TableCreationParameters={
    #             'TableName': table_name ,
    #             'AttributeDefinitions':[
    #             {
    #                 'AttributeName': 'username',
    #                 'AttributeType': 'S'
    #             },
    #             {
    #                 'AttributeName': 'last_name',
    #                 'AttributeType': 'S'
    #             },
    #             ],

    #             'KeySchema': [
    #             {
    #                 'AttributeName': 'username',
    #                 'KeyType': 'HASH'
    #             },
    #             {
    #                 'AttributeName': 'last_name',
    #                 'KeyType': 'RANGE'
    #             }
    #             ]

    #             }
    #         )
    #         print(self.service, ': Import table succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Import table failed; error: ', e)
    #         return False
        
    
    # #!! Emulator: Unknown operation
    # # list backups with try except
    # def dynamo_list_backups(self, table_name=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     try:
    #         self.client.list_backups(
    #             TableName=table_name
    #         )
    #         print(self.service, ': List backups succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': List backups failed; error: ', e)
    #         return False


    # #!! Emulator: Unknown operation
    # # list contributor insights with try except
    # def dynamo_list_contributor_insights(self, table_name=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     try:
    #         self.client.list_contributor_insights(
    #             TableName=table_name
    #         )
    #         print(self.service, ': List contributor insights succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': List contributor insights failed; error: ', e)
    #         return False
        

    # #!! Emulator: Unknown operation
    # # list exports with try except
    # def dynamo_list_exports(self, table_name=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     try:
    #         self.client.list_exports(
    #             TableArn='string'
    #         )
    #         print(self.service, ': List exports succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': List exports failed; error: ', e)
    #         return False


    # list global tables with try except
    def dynamo_list_global_tables(self):
        try:
            self.client.list_global_tables()
            print(self.service, ': List global tables succeeded')
            return True
        except Exception as e:
            print(self.service, ': List global tables failed; error: ', e)
            return False
        
    
    # #!! Emulator: Unknown operation
    # # list imports with try except
    # def dynamo_list_imports(self):
    #     try:
    #         self.client.list_imports()
    #         print(self.service, ': List imports succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': List imports failed; error: ', e)
    #         return False

    # list tables with try except
    def dynamo_list_tables(self):
        try:
            self.client.list_tables()
            print(self.service, ': List tables succeeded')
            return True
        except Exception as e:
            print(self.service, ': List tables failed; error: ', e)
            return False

    # list tags of resource with try except
    def dynamo_list_tags_of_resource(self, table_name=None):
        if table_name is None:
            table_name = self.table_name
        try:
            self.client.list_tags_of_resource(
                ResourceArn='arn:aws:dynamodb:us-east-1:123456789012:table/' + table_name
            )
            print(self.service, ': List tags of resource succeeded')
            return True
        except Exception as e:
            print(self.service, ': List tags of resource failed; error: ', e)
            return False


    # # put item with try except
    # def dynamo_put_item(self, table_name=None, item=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     if item is None:
    #         item = {
    #             'string': {
    #                 'S': 'string',
    #                 'N': '1',
    #                 'B': b'bytes',
    #                 'SS': [
    #                     'string',
    #                 ],
    #                 'NS': [
    #                     '1',
    #                 ],
    #                 'BS': [
    #                     b'bytes',
    #                 ],
    #                 'M': {
    #                     'string': {}
    #                 },
    #                 'L': [
    #                     {},
    #                 ],
    #                 'NULL': True|False,
    #                 'BOOL': True|False
    #             }
    #         }
    #     try:
    #         self.client.put_item(
    #             TableName=table_name,
    #             Item=item
    #         )
    #         print(self.service, ': Item put succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Item put failed; error: ', e)
    #         return False
        

    # # query table with try except
    # def dynamo_query(self, table_name=None, key_condition_expression=None, expression_attribute_values=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     if key_condition_expression is None:
    #         key_condition=


    # #!! Emulator: Unknown operation
    # # restore table from backup with try except
    # def dynamo_restore_table_from_backup(self, table_name=None, backup_arn=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     if backup_arn is None:
    #         backup_arn = 'arn:aws:dynamodb:us-east-1:123456789012:table/' + self.table_name
    #         table_name + '/backup/0000000000000000'
    #     try:
    #         self.client.restore_table_from_backup(
    #             TargetTableName=table_name,
    #             BackupArn=backup_arn
    #         )
    #         print(self.service, ': Restore table from backup succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Restore table from backup failed; error: ', e)
    #         return False
        
    # #!! Emulator: Unknown operation
    # # restore table to point in time with try except
    # def dynamo_restore_table_to_point_in_time(self, table_name=None, target_table_name_prefix=None, use_latest_restorable_time=None, restore_date=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     if target_table_name_prefix is None:
    #         target_table_name_prefix = 'string'
    #     if use_latest_restorable_time is None:
    #         use_latest_restorable_time = True
    #     if restore_date is None:
    #         restore_date = datetime.datetime(2015, 1, 1)
    #     try:
    #         self.client.restore_table_to_point_in_time(
    #             SourceTableName=table_name,
    #             TargetTableName=target_table_name_prefix,
    #             UseLatestRestorableTime=use_latest_restorable_time,
    #             RestoreDateTime=restore_date
    #         )
    #         print(self.service, ': Restore table to point in time succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Restore table to point in time failed; error: ', e)
    #         return False
    

    # # scan table with try except
    # def dynamo_scan(self, table_name=None, filter_expression=None, expression_attribute_values=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     if filter_expression is None:
    #         filter_expression = 'string'
    #     if expression_attribute_values is None:
    #         expression_attribute_values = {
    #             ':val': {
    #                 'S': 'string',
    #                 'N': '1',
    #                 'B': b'bytes',
    #                 'SS': [
    #                     'string',
    #                 ],
    #                 'NS': [
    #                     '1',
    #                 ],
    #                 'BS': [
    #                     b'bytes',
    #                 ],
    #                 'M': {
    #                     'string': {}
    #                 },
    #                 'L': [
    #                     {},
    #                 ],
    #                 'NULL': True|False,
    #                 'BOOL': True|False
    #             }
    #         }
    #     try:
    #         self.client.scan(
    #             TableName=table_name,
    #             FilterExpression=filter_expression,
    #             ExpressionAttributeValues=expression_attribute_values
    #         )
    #         print(self.service, ': Scan succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Scan failed; error: ', e)
    #         return False
    
    # tag resource with try except
    def dynamo_tag_resource(self, resource_arn=None, tags=None):
        if resource_arn is None:
            resource_arn = 'arn:aws:dynamodb:us-east-1:123456789012:table/' + self.table_name
        if tags is None:
            tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        try:
            self.client.tag_resource(
                ResourceArn=resource_arn,
                Tags=tags
            )
            print(self.service, ': Tag resource succeeded')
            return True
        except Exception as e:
            print(self.service, ': Tag resource failed; error: ', e)
            return False
        
    # # transact get items with try except
    # def dynamo_transact_get_items(self, transact_items=None):
    #     if transact_items is None:
    #         transact_items=[
    #             {
    #                 'Get': {
    #                     'Key': {
    #                         'string': {
    #                             'S': 'string',
    #                             'N': '1',
    #                             'B': b'bytes',
    #                             'SS': [
    #                                 'string',
    #                             ],
    #                             'NS': [
    #                                 '1',
    #                             ],
    #                             'BS': [
    #                                 b'bytes',
    #                             ],
    #                             'M': {
    #                                 'string': {}
    #                             },
    #                             'L': [
    #                                 {},
    #                             ],
    #                             'NULL': True|False,
    #                             'BOOL': True|False
    #                         }
    #                     },
    #                     'TableName': self.table_name,
    #                     'ProjectionExpression': 'string',
    #                     'ExpressionAttributeNames': {
    #                         'string': 'string'
    #                     }
    #                 }
    #             },
    #         ]

    #     try:
    #         self.client.transact_get_items(TransactItems=transact_items)
    #         print(self.service, ': Transact get items succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Transact get items failed; error: ', e)
    #         return False


    # transact write items with try except
    # def dynamo_transact_write_items(self, transact_items=None):
    #     if transact_items is None:
    #         transact_items=[
    #             {
    #                 'Put': {
    #                     'Item': {
    #                         'string': {
    #                             'S': 'string',
    #                             'N': '1',
    #                             'B': b'bytes',
    #                             'SS': [
    #                                 'string',
    #                             ],
    #                             'NS': [
    #                                 '1',
    #                             ],
    #                             'BS': [
    #                                 b'bytes',
    #                             ],
    #                             'M': {
    #                                 'string': {}
    #                             },
    #                             'L': [
    #                                 {},
    #                             ],
    #                             'NULL': True|False,
    #                             'BOOL': True|False
    #                         }
    #                     },
    #                     'TableName': self.table_name,
    #                     'ConditionExpression': 'string',
    #                     'ExpressionAttributeNames': {
    #                         'string': 'string'
    #                     },
    #                     'ExpressionAttributeValues': {
    #                         'string': {
    #                             'S': 'string',
    #                             'N': '1',
    #                             'B': b'bytes',
    #                             'SS': [
    #                                 'string',
    #                             ],
    #                             'NS': [
    #                                 '1',
    #                             ],
    #                             'BS': [
    #                                 b'bytes',
    #                             ],
    #                             'M': {
    #                                 'string': {}
    #                             },
    #                             'L': [
    #                                 {},
    #                             ],
    #                             'NULL': True|False,
    #                             'BOOL': True|False
    #                         }
    #                     },
    #                     'ReturnValuesOnConditionCheckFailure': 'ALL_OLD'|'NONE'
    #                 }
    #             },
    #         ]
    #     try:
    #         self.client.transact_write_items(TransactItems=transact_items)
    #         print(self.service, ': Transact write items succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Transact write items failed; error: ', e)
    #         return False



    # untag resource with try except
    def dynamo_untag_resource(self, resource_arn=None, tag_keys=None):
        if resource_arn is None:
            resource_arn = 'arn:aws:dynamodb:us-east-1:123456789012:table/' + self.table_name
        if tag_keys is None:
            tag_keys=[
                'string',
            ]
        try:
            self.client.untag_resource(
                ResourceArn=resource_arn,
                TagKeys=tag_keys
            )
            print(self.service, ': Untag resource succeeded')
            return True
        except Exception as e:
            print(self.service, ': Untag resource failed; error: ', e)
            return False
        

    # update continuous backups with try except
    def dynamo_update_continuous_backups(self, point_in_time_recovery_specification=None):
        if point_in_time_recovery_specification is None:
            point_in_time_recovery_specification={
                'PointInTimeRecoveryEnabled': True|False
            }
        try:
            self.client.update_continuous_backups(
                TableName=self.table_name,
                PointInTimeRecoverySpecification=point_in_time_recovery_specification
            )
            print(self.service, ': Update continuous backups succeeded')
            return True
        except Exception as e:
            print(self.service, ': Update continuous backups failed; error: ', e)
            return False
        

    # #!! Emulator: Unknown operation
    # # update contributor insights with try except
    # def dynamo_update_contributor_insights(self, index_name=None, contributor_insights_action=None):
    #     if index_name is None:
    #         index_name = 'index_name'
    #     if contributor_insights_action is None:
    #         contributor_insights_action= 'ENABLE'
    #     try:
    #         self.client.update_contributor_insights(
    #             TableName=self.table_name,
    #             IndexName=index_name,
    #             ContributorInsightsAction=contributor_insights_action
    #         )
    #         print(self.service, ': Update contributor insights succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Update contributor insights failed; error: ', e)
    #         return False
        

    # update global table with try except
    def dynamo_update_global_table(self, global_table_name=None, replica_updates=None):
        if global_table_name is None:
            global_table_name = self.table_name
        if replica_updates is None:
            replica_updates=[
                {
                    'Create': {
                        'RegionName': 'us-east-1'
                    }
                },
            ]
        try:
            self.client.update_global_table(
                GlobalTableName=global_table_name,
                ReplicaUpdates=replica_updates
            )
            print(self.service, ': Update global table succeeded')
            return True
        except Exception as e:
            print(self.service, ': Update global table failed; error: ', e)
            return False
        
    # #!! Emulator: Unknown operation
    # # update global table settings with try except
    # def dynamo_update_global_table_settings(self, global_table_name=None):
    #     if global_table_name is None:
    #         global_table_name = self.table_name
        
    #     try:
    #         self.client.update_global_table_settings(
    #             GlobalTableName=global_table_name,
    #             GlobalTableBillingMode='PROVISIONED',
    #             GlobalTableProvisionedWriteCapacityUnits=123,
    #             GlobalTableProvisionedWriteCapacityAutoScalingSettingsUpdate={
    #                 'MinimumUnits': 123,
    #                 'MaximumUnits': 123,
    #                 'AutoScalingDisabled': True,
    #                 'AutoScalingRoleArn': 'string',
    #                 'ScalingPolicyUpdate': {
    #                     'PolicyName': 'string',
    #                     'TargetTrackingScalingPolicyConfiguration': {
    #                         'DisableScaleIn': True,
    #                         'ScaleInCooldown': 123,
    #                         'ScaleOutCooldown': 123,
    #                         'TargetValue': 123.0
    #                     }
    #                 }
    #             },
    #             GlobalTableGlobalSecondaryIndexSettingsUpdate=[
    #                 {
    #                     'IndexName': 'string',
    #                     'ProvisionedWriteCapacityUnits': 123,
    #                     'ProvisionedWriteCapacityAutoScalingSettingsUpdate': {
    #                         'MinimumUnits': 123,
    #                         'MaximumUnits': 123,
    #                         'AutoScalingDisabled': True,
    #                         'AutoScalingRoleArn': 'string',
    #                         'ScalingPolicyUpdate': {
    #                             'PolicyName': 'string',
    #                             'TargetTrackingScalingPolicyConfiguration': {
    #                                 'DisableScaleIn': True,
    #                                 'ScaleInCooldown': 123,
    #                                 'ScaleOutCooldown': 123,
    #                                 'TargetValue': 123.0
    #                             }
    #                         }
    #                     }
    #                 },
    #             ]
    #         )
    #         print(self.service, ': Update global table settings succeeded')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Update global table settings failed; error: ', e)
    #         return False
        

    # # update item with try except
    # def dynamo_update_item(self):
    #     try:
    #         self.client.update_item(
    #             TableName=self.table_name,
    #             Key={
    #                 'username': {
    #                     'S': 'johndoe'
    #                 },
    #                 'last_name': {
    #                     'S': 'doe'
    #                 }
    #             },
    #             UpdateExpression='SET age = :val1',
    #             ExpressionAttributeValues={
    #                 ':val1': {
    #                     'N': '30'
    #                 }
    #             }
    #         )
    #         print(self.service, ': Item updated')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Item update failed; error: ', e)
    #         return False
        

    # # update table with try except
    # def dynamo_update_table(self, table_name=None):
    #     if table_name is None:
    #         table_name = self.table_name
    #     try:
    #         self.client.update_table(
    #             TableName=table_name,
    #             ProvisionedThroughput={
    #                 'ReadCapacityUnits': 10,
    #                 'WriteCapacityUnits': 10
    #             }
    #         )
    #         print(self.service, ': Table updated')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Table update failed; error: ', e)
    #         return False
        

    
    # #!! Emulator: Unknown operation    
    # # update table replica autoscaling with try except
    # def dynamo_update_replica_autoscaling(self):
    #     try:
    #         self.client.update_table_replica_auto_scaling(
    #             TableName=self.table_name,
    #             GlobalSecondaryIndexUpdates=[
    #                 {
    #                         'IndexName': 'index1',
    #                         'ProvisionedWriteCapacityAutoScalingUpdate': {
    #                             'AutoScalingDisabled': False,
    #                             'AutoScalingRoleArn': 'arn:aws:iam::123456789012:role/DynamoDBAutoscaleRole',
    #                             'ScalingPolicyUpdate': {
    #                                 'PolicyName': 'WriteCapacityUnitsScalingPolicy',
    #                                 'TargetTrackingScalingPolicyConfiguration': {
    #                                     'DisableScaleIn': False,
    #                                     'ScaleInCooldown': 300,
    #                                     'ScaleOutCooldown': 300,
    #                                     'TargetValue': 70.0
    #                                 }
    #                             }
    #                         }
    #                 },
    #             ]
    #         )
    #         print(self.service, ': Replica autoscaling updated')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': Replica autoscaling update failed; error: ', e)
    #         return False
        


    # # update time to live with try except
    # def dynamo_update_ttl(self):
    #     try:
    #         self.client.update_time_to_live(
    #             TableName=self.table_name,
    #             TimeToLiveSpecification={
    #                 'AttributeName': 'ttl',
    #                 'Enabled': True
    #             }
    #         )
    #         print(self.service, ': TTL updated')
    #         return True
    #     except Exception as e:
    #         print(self.service, ': TTL update failed; error: ', e)
    #         return False



if __name__ == '__main__':


    # create blob client
    table_client = DynamoDBClient()
    # get all methods
    methods = [getattr(DynamoDBClient, attr) for attr in dir(DynamoDBClient) if callable(getattr(DynamoDBClient, attr)) and not attr.startswith("__")]

    for i in methods:
        print(i.__name__)
        i(table_client)