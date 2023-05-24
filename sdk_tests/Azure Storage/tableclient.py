import datetime
from azure.data.tables import TableClient, TableServiceClient, TableEntity, UpdateMode
import random
from uuid import uuid4


class MyTableClient():

    def __init__(self, emulator=True, table_name=None):

        # table name
        if table_name is None:
            self.table_name = f'table{random.randint(1, 1000000000)}'
        else:
            self.table_name = table_name

        self.account_name = 'restlertest1'

        # connection string
        if emulator:
            self.connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;'
            self.service = "**EMULATOR**"
        else:
            self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=restlertest1;AccountKey=En0z7F3kBwgMv8YIlU57bifLmr2Nb71m4sNVndRvtFiOlpWRNhnlOOPsJG5C7uwZgP92rkFFj4rx+AStw5Q7sA==;EndpointSuffix=core.windows.net'
            self.service = '**AZURE**'

        # create table client
        self.table_client = TableClient.from_connection_string(self.connection_string, self.table_name)
        self.table_client.create_table()


        
    # creat entity with default table name as none with try except
    def table_create_entity(self, table_entity=None):
        if table_entity is None:
            table_entity = self.entity = {
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

        try:
            self.table_client.create_entity(table_entity)
            print(self.service, ': Entity created')
            return True
        except Exception as e:
            print(self.service, ': Entity creation failed; error: ', e)
            return False
        
    # delete entity with default entity none with try except
    def table_delete_entity(self):
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

        try:
            self.table_client.delete_entity(row_key="brandtwo", partition_key="colortwo")
            print(self.service, ': Entity deleted')
            # create entity again
            self.table_create_entity()
            return True
        except Exception as e:
            print(self.service, ': Entity deletion failed; error: ', e)
            return False
        

    # delete table with default table name as none with try except
    def table_delete_table(self, table_name=None):
        if table_name is None:
            table_name = self.table_name

        try:
            self.table_client.delete_table()
            print(self.service, ': Table deleted with name: ', self.table_name)
            # create table again
            self.table_client.create_table()
            return True
        except Exception as e:
            print(self.service, ': Table deletion failed with name: ', self.table_name, ' and error: ', e)
            return False
        

    # get entity with default entity none with try except
    def table_get_entity(self):
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

        try:
            self.table_client.get_entity(row_key="brandthree", partition_key="colorthree")
            print(self.service, ': Entity retrieved')
            return True
        except Exception as e:
            print(self.service, ': Entity retrieval failed; error: ', e)
            return False
        

    # get table access policy with try except
    def table_get_table_access_policy(self):
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
    def table_list_entities(self):
        try:
            self.table_client.list_entities()
            print(self.service, ': Entities listed')
            return True
        except Exception as e:
            print(self.service, ': Entities listing failed; error: ', e)
            return False
        

    # query entities with default query filter none with try except
    def table_query_entities(self, query_filter=None):
        if query_filter is None:
            query_filter = "PartitionKey eq 'color'"

        try:
            self.table_client.query_entities(query_filter)
            print(self.service, ': Entities queried')
            return True
        except Exception as e:
            print(self.service, ': Entities query failed; error: ', e)
            return False
        

    # set table access policy default policy none with try except
    def table_set_table_access_policy(self, policy=None):
        if policy is None:
            policy = {}
        try:
            self.table_client.set_table_access_policy(signed_identifiers=policy)
            print(self.service, ': Table access policy set')
            return True
        except Exception as e:
            print(self.service, ': Table access policy set failed; error: ', e)
            return False
        

    # submit transaction with default transaction none with try except
    def table_submit_transaction(self, transaction=None):
        if transaction is None:
            transaction = [
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
            ]

        try:
            self.table_client.submit_transaction(transaction)
            print(self.service, ': Transaction submitted')
            return True
        except Exception as e:
            print(self.service, ': Transaction submission failed; error: ', e)
            return False
        

    # update entity with default entity none with try except
    def table_update_entity(self, entity=None, mode=UpdateMode.MERGE):
        if entity is None:
            entity = {
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

        try:
            self.table_client.update_entity(entity=entity, mode=mode)
            print(self.service, ': Entity updated')
            return True
        except Exception as e:
            print(self.service, ': Entity update failed; error: ', e)
            return False
        

    # upsert entity with default entity none with try except
    def table_upsert_entity(self, entity=None, mode=UpdateMode.REPLACE):
        if entity is None:
            entity = {
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

        try:
            self.table_client.upsert_entity(entity=entity, mode=mode)
            print(self.service, ': Entity upserted')
            return True
        except Exception as e:
            print(self.service, ': Entity upsert failed; error: ', e)
            return False
        

# if __name__ == '__main__':


#     # create blob client
#     table_client = MyTableClient(False)
#     # get all methods
#     methods = [getattr(MyTableClient, attr) for attr in dir(MyTableClient) if callable(getattr(MyTableClient, attr)) and not attr.startswith("__")]

#     for i in methods:
#         print(i.__name__)
#         i(table_client)
        

    