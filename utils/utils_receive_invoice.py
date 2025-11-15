from utils.utils import get_engine, get_storecove_credentials
from sqlalchemy import text
import requests
import json

def get_received_invoice_json(guid, branch_code):

    api_key, _ = get_storecove_credentials(branch_code)

    # Request body
    api_url = 'https://api.storecove.com/api/v2'
    headers_receive = {
        "Authorization": f"Bearer {api_key}"
    }
    endpoint = api_url + f'/received_documents/{guid}/json'

    # Send Request
    response = requests.get(endpoint, headers=headers_receive)

    # Return invoice json
    print(response.status_code)
    if response.status_code == 200:
        response_json = response.json()['document']
    else:
        print(response.content)
        raise

    return response_json

def load_received_invoice_db(engine, guid, branch_code, received_invoice_time):

    """
    Load the document UID of the received invoice
    """
    # Get json format invoice
    invoice_json = get_received_invoice_json(guid, branch_code)
    invoice_json_dumps = json.dumps(invoice_json)

    # Insert document UID and received time into the table 'received_invoice'
    insert_query = text("""
        INSERT INTO received_invoice (document_uid, branch_code, json_data, received_time)
        VALUES (:uid, :branch_code, :json, :received_time)
    """)

    try:
        with engine.begin() as conn:
            conn.execute(insert_query, {
                "uid": guid,
                "branch_code" : branch_code,
                "json" : invoice_json_dumps,
                "received_time": received_invoice_time
            })
        return True
    except Exception as e:
        raise 
    finally:
        engine.dispose()

