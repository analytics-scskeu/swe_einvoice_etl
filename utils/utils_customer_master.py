import json
import requests
from sqlalchemy import text
from utils.utils import get_storecove_credentials, get_customer_peppol_id
api_url = 'https://api.storecove.com/api/v2'

def check_peppol_availablity(engine, branch_code, customer_supplier_code, vat_id, supplier_flag, api_url):

    """
    Check PEPPOL availablity of customer/supplier
    """

    api_key, _ = get_storecove_credentials(branch_code)

    # Get customer/supplier's PEPPOL info
    peppol_scheme, peppol_id = get_customer_peppol_id(engine, branch_code, customer_supplier_code, vat_id, supplier_flag)

    # Request
    api_url_check_identifier = api_url + '/discovery/receives'
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "documentTypes": "invoice",
        "network": "peppol",
        "metaScheme": "iso6523-actorid-upis",
        "scheme": peppol_scheme,
        "identifier": peppol_id
    }
    # Load JSON data from file
    with open("invoices/discovery.json", "r") as file:
        payload = json.load(file)  # Load JSON from file

    # Send Request
    response = requests.post(api_url_check_identifier, headers=headers, json=payload)

    print(response.status_code)
    print(response.json()) 


def update_db_from_ui(engine, updates_li):
    """
    Update db table 'cutsomer_supplier' from Web UI.

    update_li : 'updates' parameter (list) in json
    """

    if not updates_li:
        return True

    # Extract columns to update from the list
    key_columns = ['branch_code', 'code', 'vat_id', 'supplier_flag']
    update_columns =  [
                "country_code",
                'peppol_scheme'
                "peppol_id",
                "b2x",
                "sending_method",
                "secondary_email_addresses"
    ]

    # Order of columns in VALUES
    ordered_columns = key_columns + update_columns

    # Build VALUES section
    values_rows = []
    params = {}

    for i, row in enumerate(updates_li):
        placeholder_row = []
        for col in ordered_columns:
            param_key = f"{col}"
            placeholder_row.append(f":{param_key}")
            value = row.get(col)
            params[param_key] = value if value not in ("", " ") else None
        values_rows.append("(" + ", ".join(placeholder_row) + ")")

    values_sql = ",\n".join(values_rows)

    # Build SET clause
    set_clauses = [
        f"{col} = v.{col}"
        for col in update_columns
    ]
    set_sql = ",\n    ".join(set_clauses)

    # Build JOIN condition
    join_conditions = [f"t.{col} = v.{col}" for col in key_columns]
    join_sql = " AND ".join(join_conditions)

    query = text(f"""
        UPDATE customer_supplier AS t
        SET
            {set_sql}
        FROM (VALUES
            {values_sql}
        ) AS v({", ".join(ordered_columns)})
        WHERE {join_sql};
    """)

    connection = engine.connect()
    transaction = connection.begin()
    try:
        connection.execute(query, params)
        transaction.commit()
        print("Completed updating record")
        return True
    except Exception as e:
        transaction.rollback()
        print(f"Error when updating values to DB: {e}")
        raise
    finally:
        connection.close()


    

# from utils.utils import get_engine

# li = {
#   "updates": [
#     {
#       "branch_code": "10",
#       "code": "001",
#       "vat_id": "BE123",
#       "country_code": "BE",
#       "peppol_id": "PEP001",
#       "b2x": "Y",
#       "sending_method": "email",
#       "secondary_email_addresses": "a@b.com"
#     },
#     {
#       "branch_code": "11",
#       "code": "002",
#       "vat_id": "DE456",
#       "country_code": "DE",
#       "peppol_id": "PEP002",
#       "b2x": "Y",
#       "sending_method": "api",
#       "secondary_email_addresses": ""
#     }
#   ]
# }

# import os
# from dotenv import load_dotenv
# load_dotenv()
# import urllib

# user = os.environ['DB_USER']
# password = urllib.parse.quote_plus(os.environ['DB_PASSWORD'])
# host = os.environ['DB_HOST']
# port = os.environ['DB_PORT']
# database = os.environ['DB_DATABASE']

# target_table = 'customer'
# engine = get_engine(user, password, database, host, port)
# update_db(engine, target_table, li['updates'])