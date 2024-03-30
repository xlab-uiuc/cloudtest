import datetime
from azure.data.tables import TableClient, TableServiceClient, UpdateMode, TableAccessPolicy, TableSasPermissions
from uuid import uuid4
from azure.identity import DefaultAzureCredential
import random, json

# Point to certificates
# os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

credential = DefaultAzureCredential()
config = json.loads(open('config.json').read())

class MyTableClient():

    def __init__(self, emulator=True, table_name=None):

        # randomize seed
        random.seed(datetime.datetime.now())

        # table name
        if table_name is None:
            self.table_name = f'table{random.randint(1, 1000000000)}'
        else:
            self.table_name = table_name

        global config
        self.account_name = config['cloud_account_name']

        # connection string
        if emulator:
            self.connection_string = config['emulator_connection_string']
            self.service = "**EMULATOR**"
        else:
            self.connection_string = config['cloud_connection_string']
            self.service = '**AZURE**'

        # credential
        global credential

        try:
            # service client
            self.table_service_client = TableServiceClient.from_connection_string(self.connection_string)
            # create table client
            self.table_client = TableClient.from_connection_string(self.connection_string, self.table_name)
        except Exception as e:
            print('Table client creation failed; error: ', e)

        try:
            self.table_client.create_table()
        except Exception as e:
            print('Table creation failed; error: ', e)


        
    # creat entity with default table name as none with try except
    def table_create_entity(self, args):
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
            res = self.table_client.create_entity(args[0])
            print(self.service, ': Success -- Entity created')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Entity creation failed; error: ', e)
            return False, e
        
    # delete entity with default entity none with try except
    def table_delete_entity(self, args):
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
            res = self.table_client.delete_entity(row_key=args[0], partition_key=args[1])
            print(self.service, ': Success -- Entity deleted')
            # create entity again
            self.table_create_entity([])
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Entity deletion failed; error: ', e)
            return False, e
        

    # delete table with default table name as none with try except
    def table_delete_table(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append(self.table_name)

        try:
            res = self.table_client.delete_table()
            print(self.service, ': Success -- Table deleted with name: ', args[0])

            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Table deletion failed with name: ', args[0], ' and error: ', e)
            return False, e
        

    # get entity with default entity none with try except
    def table_get_entity(self, args):
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
            res = self.table_client.get_entity(row_key=args[0], partition_key=args[1])
            print(self.service, ': Success -- Entity retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Entity retrieval failed; error: ', e)
            return False, e
        

    # get table access policy with try except
    def table_get_table_access_policy(self, args):
        args = list(args)
        tab = f'table{random.randint(1, 1000000000)}'
        table_client = TableClient.from_connection_string(self.connection_string, tab)
        table_client.create_table()
        try:
            res = table_client.get_table_access_policy()
            print(self.service, ': Success -- Table access policy retrieved')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Table access policy retrieval failed; error: ', e)
            return False, e
        

    # list entities in the table with try except
    def table_list_entities(self, args):
        args = list(args)
        try:
            res = self.table_client.list_entities()
            print(self.service, ': Success -- Entities listed')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Entities listing failed; error: ', e)
            return False, e
        

    # query entities with default query filter none with try except
    def table_query_entities(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append("PartitionKey eq 'color'")

        try:
            res = self.table_client.query_entities(args[0])
            print(self.service, ': Success -- Entities queried')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Entities query failed; error: ', e)
            return False, e
        

    # set table access policy default policy none with try except
    def table_set_table_access_policy(self, args):
        args = list(args)
        if not len(args) > 0:
            access_policy = TableAccessPolicy()
            access_policy.start = datetime.datetime(2011, 10, 11)
            access_policy.expiry = datetime.datetime(2025, 10, 12)
            access_policy.permission = TableSasPermissions(read=True)
            identifiers = {'testid': access_policy}
            args.append(identifiers)
        try:
            res = self.table_client.set_table_access_policy(signed_identifiers=args[0])
            print(self.service, ': Success -- Table access policy set')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Table access policy set failed; error: ', e)
            return False, e
        

    # submit transaction with default transaction none with try except
    def table_submit_transaction(self, args):
        args = list(args)
        if not len(args) > 0:
            args.append([
            ('upsert', {'PartitionKey': 'color3', 'RowKey': 'brand3'}, {'mode': UpdateMode.REPLACE}),
            ])

        try:
            # create entity and then update it
            self.table_create_entity([])

            res = self.table_client.submit_transaction(args[0])
            print(self.service, ': Success -- Transaction submitted')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Transaction submission failed; error: ', e)
            return False, e
        

    # update entity with default entity none with try except
    def table_update_entity(self, args):
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
            # create entity and then update it
            self.table_create_entity([])

            res = self.table_client.update_entity(entity=args[0], mode=args[1])
            print(self.service, ': Success -- Entity updated')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Entity update failed; error: ', e)
            return False, e
        

    # upsert entity with default entity none with try except
    def table_upsert_entity(self, args):
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
            res = self.table_client.upsert_entity(entity=args[0], mode=args[1])
            print(self.service, ': Success -- Entity upserted')
            return True, res
        except Exception as e:
            print(self.service, ': Fail -- Entity upsert failed; error: ', e)
            return False, e
        
        
    # garbage collection
    def __cleanup__(self):

        try:
            tables = self.table_service_client.list_tables()
            # list tables 
            for table in tables:
                try:
                    self.table_service_client.delete_table(table.name)
                    print(f'Table deleted in GC -- {self.service}')
                except:
                    print(f'Table deletion failed in GC -- {self.service}')

        except Exception as e:

            print(f'Tables could not be listed in GC -- {self.service}')
    