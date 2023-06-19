import datetime
from azure.data.tables import TableClient, TableServiceClient, UpdateMode
import random
from uuid import uuid4


class MyTableClient():

    def __init__(self, emulator=True, table_name=None):

        # table name
        if table_name is None:
            self.table_name = f'table{random.randint(1, 1000000000)}'
        else:
            self.table_name = table_name

        self.account_name = 'sdkfuzz'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=sdkfuzz;AccountKey=KPh28d77wMJA1De3IsRObHapOtxJU01LTaFnrDCkqnyiLh564NEAb1IipT+mG7scISEEobMOqTj2+AStAVeigA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'

        try:
            # service client
            self.table_service_client = TableServiceClient.from_connection_string(self.connection_string)
            # create table client
            self.table_client = TableClient.from_connection_string(self.connection_string, self.table_name)
        except Exception as e:
            print('Table client creation failed; error: ', e)

        try:
            self.table_client.create_table()
        except:
            pass


        
    # creat entity with default table name as none with try except
    def table_create_entity(self, *args):
        args = list(args)

        if not len(args) > 0:
            self.entity = {
            "PartitionKey": "color",
            "RowKey": "brand",
            "text": "Marker",
            "color": "Purple",
            "price": 4.99,
            "last_updated": datetime.datetime.today(),
            "product_id": uuid4(),
            "inventory_count": 42,
            "barcode": b"135aefg8oj0ld58" # cspell:disable-line
            }
            args.append(self.entity)

        try:
            self.table_client.create_entity(args[0])
            print(self.service, ': Entity created')
            return True
        except Exception as e:
            print(self.service, ': Entity creation failed; error: ', e)
            return False
        
    # delete entity with default entity none with try except
    def table_delete_entity(self, *args):
        args = list(args)
        try:
            self.table_client.create_entity({
            "PartitionKey": "colortwo",
            "RowKey": "brandtwo",
            "text": "Marker",
            "color": "Purple",
            "price": 4.99,
            "last_updated": datetime.datetime.today(),
            "product_id": uuid4(),
            "inventory_count": 42,
            "barcode": b"135aefg8oj0ld58" # cspell:disable-line
        })
        except Exception as e:
            print("Entity already exists!", e)

        if not len(args) > 0:
            args.append('brandtwo')
        if not len(args) > 1:
            args.append('colortwo')

        try:
            self.table_client.delete_entity(row_key=args[0], partition_key=args[1])
            print(self.service, ': Entity deleted')
            # create entity again
            self.table_create_entity()
            return True
        except Exception as e:
            print(self.service, ': Entity deletion failed; error: ', e)
            return False
        

    # delete table with default table name as none with try except
    def table_delete_table(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.table_name)

        try:
            self.table_client.delete_table()
            print(self.service, ': Table deleted with name: ', args[0])
            # create table again
            self.table_client.create_table()
            return True
        except Exception as e:
            print(self.service, ': Table deletion failed with name: ', args[0], ' and error: ', e)
            return False
        

    # get entity with default entity none with try except
    def table_get_entity(self, *args):
        args = list(args)
        try:
            self.table_client.create_entity(entity={
            "PartitionKey": "colorthree",
            "RowKey": "brandthree",
            "text": "Marker",
            "color": "Purple",
            "price": 4.99,
            "last_updated": datetime.datetime.today(),
            "product_id": uuid4(),
            "inventory_count": 42,
            "barcode": b"135aefg8oj0ld58" # cspell:disable-line
        })
        except Exception as e:
            print("Entity already exists!", e)

        if not len(args) > 0:
            args.append("brandthree")
        if not len(args) > 1:
            args.append("colorthree")

        try:
            self.table_client.get_entity(row_key=args[0], partition_key=args[1])
            print(self.service, ': Entity retrieved')
            return True
        except Exception as e:
            print(self.service, ': Entity retrieval failed; error: ', e)
            return False
        

    # get table access policy with try except
    def table_get_table_access_policy(self, *args):
        args = list(args)
        tab = f'table{random.randint(1, 1000000000)}'
        table_client = TableClient.from_connection_string(self.connection_string, tab)
        table_client.create_table()
        try:
            table_client.get_table_access_policy()
            print(self.service, ': Table access policy retrieved')
            return True
        except Exception as e:
            print(self.service, ': Table access policy retrieval failed; error: ', e)
            return False
        

    # list entities in the table with try except
    def table_list_entities(self, *args):
        args = list(args)
        try:
            self.table_client.list_entities()
            print(self.service, ': Entities listed')
            return True
        except Exception as e:
            print(self.service, ': Entities listing failed; error: ', e)
            return False
        

    # query entities with default query filter none with try except
    def table_query_entities(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append("PartitionKey eq 'color'")

        try:
            self.table_client.query_entities(args[0])
            print(self.service, ': Entities queried')
            return True
        except Exception as e:
            print(self.service, ': Entities query failed; error: ', e)
            return False
        

    # set table access policy default policy none with try except
    def table_set_table_access_policy(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append({})
        try:
            self.table_client.set_table_access_policy(signed_identifiers=args[0])
            print(self.service, ': Table access policy set')
            return True
        except Exception as e:
            print(self.service, ': Table access policy set failed; error: ', e)
            return False
        

    # submit transaction with default transaction none with try except
    def table_submit_transaction(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append([
                {
                    "UpdateEntity": {
                        "PartitionKey": "color",
                        "RowKey": "brand",
                        "text": "Marker",
                        "color": "Purple",
                        "price": 4.99,
                        "last_updated": datetime.datetime.today(),
                        "product_id": uuid4(),
                        "inventory_count": 42,
                        "barcode": b"135aefg8oj0ld58" # cspell:disable-line
                    }
                }
            ])

        try:
            self.table_client.submit_transaction(args[0])
            print(self.service, ': Transaction submitted')
            return True
        except Exception as e:
            print(self.service, ': Transaction submission failed; error: ', e)
            return False
        

    # update entity with default entity none with try except
    def table_update_entity(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append({
                "PartitionKey": "color",
                "RowKey": "brand",
                "text": "Marker",
                "color": "Purple",
                "price": 4.99,
                "last_updated": datetime.datetime.today(),
                "product_id": uuid4(),
                "inventory_count": 42,
                "barcode": b"135aefg8oj0ld58" # cspell:disable-line
            })
        if not len(args) > 1:
            args.append(UpdateMode.MERGE)

        try:
            self.table_client.update_entity(entity=args[0], mode=args[1])
            print(self.service, ': Entity updated')
            return True
        except Exception as e:
            print(self.service, ': Entity update failed; error: ', e)
            return False
        

    # upsert entity with default entity none with try except
    def table_upsert_entity(self, *args):
        args = list(args)
        if not len(args) > 0:
            args.append({
                "PartitionKey": "color",
                "RowKey": "brand",
                "text": "Marker",
                "color": "Purple",
                "price": 4.99,
                "last_updated": datetime.datetime.today(),
                "product_id": uuid4(),
                "inventory_count": 42,
                "barcode": b"135aefg8oj0ld58" # cspell:disable-line
            })
        if not len(args) > 1:
            args.append(UpdateMode.MERGE)
        try:
            self.table_client.upsert_entity(entity=args[0], mode=args[1])
            print(self.service, ': Entity upserted')
            return True
        except Exception as e:
            print(self.service, ': Entity upsert failed; error: ', e)
            return False
        
        
    # garbage collection
    def __cleanup__(self):

        try:
            tables = self.table_service_client.list_tables()
            # list tables 
            for table in tables:
                try:
                    self.table_service_client.delete_table(table.name)
                    print('Table deleted: ', table.name)
                except:
                    print('Table deletion failed: ', table.name)

        except Exception as e:

            print('Tables could not be listed: ', e)
    