import json
import requests
from utils.utils import get_storecove_credentials, get_customer_peppol_id
api_url = 'https://api.storecove.com/api/v2'

def check_peppol_availablity(engine, branch_code, customer_supplier_code, vat_id, api_url):

    """
    Check PEPPOL availablity of customer/supplier
    """

    api_key, _ = get_storecove_credentials(branch_code)

    # Get customer/supplier's PEPPOL info
    peppol_scheme, peppol_id = get_customer_peppol_id(engine, branch_code, customer_supplier_code, vat_id)

    # Request
    api_url_check_identifier = api_url + '/discovery/receives'
    headers_send = {
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
    response = requests.post(api_url_check_identifier, headers=headers_send, json=payload)

    print(response.status_code)
    print(response.json()) 