from sqlalchemy import create_engine
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()



def get_engine(user, password, database, host, port):

    """
    Connect to SQLServer database
    """

    connect_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user,password,host,port,database)
    print(connect_string)
    try:
        engine = create_engine(connect_string, echo=False)
        print(f'Connected to {host}:{database}')
        return engine
    except Exception as e:
        print(f'Failed to connect {host}:{database}')
        raise

def get_storecove_credentials(branch_code):

    """
    Get Legal Entity ID and API Key of Storecove API
    """
    load_dotenv()

    try:
        api_key = os.environ[f'API_KEY_{branch_code}']
        legal_entity_id = os.environ[f'LEGAL_ENTITY_ID_{branch_code}']
        return api_key, legal_entity_id
    except Exception as e:
        print(f'{type(e)} : {e}')
        raise

def get_customer_peppol_id(engine, branch_code, customer_supplier_code, vat_id):

    """
    Get PEPPOL scheme and id for a customer
    """
    target_table = 'customer'

    try:
        df = pd.read_sql(f'''SELECT peppol_scheme, peppol_id 
                        FROM {target_table} 
                        WHERE branch_code = '{branch_code}, {target_table}_code = {customer_supplier_code} AND vat_id = {vat_id}'''
                        , con=engine)
    except Exception as e:
        print(f'{type(e) : {e}}')
        raise
    
    if len(df) == 0:
        print('There is no customer/supplier')
        raise
    else:
        peppol_scheme = df['peppol_scheme'][0]
        peppol_id = df['peppol_id'][0]

    return peppol_scheme, peppol_id




# def get_container_client(connection_string, container):
    
#     """Get container client of Azure blob storage"""

#     # Connect to Azure blob storage account
#     try:
#         blob_service_client = BlobServiceClient.from_connection_string(
#             connection_string
#         )
#     except Exception as e:
#         logging.error(f"Issue in connection string of Azure storage. {type(e)} {e}")
#         raise

#     container_client = blob_service_client.get_container_client(container)

#     return container_client