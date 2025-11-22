from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
import os
import urllib
import json
from utils.utils_receive_invoice import load_received_invoice_db
from utils.utils_customer_master import update_db_from_ui
from utils.utils import get_engine
from datetime import datetime

app = FastAPI()

user = os.environ['DB_USER']
password = urllib.parse.quote_plus(os.environ['DB_PASSWORD'])
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
database = os.environ['DB_DATABASE']

class CustomerListItem(BaseModel):
    branch_code : str
    code : str
    vat_id : str
    supplier_flag : str
    b2x : str
    peppol_scheme : str
    peppol_id : str
    sending_method : str
    secondary_email_addresses : list[str] = []

class CustomerUpdateRequest(BaseModel):
    updates : List[CustomerListItem]

class ReceiveInvoiceWebhookListItem(BaseModel):
    event_type : Optional[str] = None
    event_group : Optional[str] = None
    event : str
    receive_guid : Optional[str] = None
    document_guid : str
    processing_notes : List[str]
    tenant_id : str
    parseable : bool

@app.post('/update_customer_supplier_db')
def update_customer_supplier_db(request : CustomerUpdateRequest):

    engine = get_engine(user, password, database, host, port)
    
    success = update_db_from_ui(engine, request.updates)
    if success:
        return {'message' : 'success'}
    else:
        raise HTTPException(status_code=500, detail='Internal Server error')

@app.post('/storecove_webhook_receive_document/DE')
async def webhook_receive_document_dusseldolf(request: ReceiveInvoiceWebhookListItem):
    return await storecove_webhook_receive_document(request, '10')

@app.post('/storecove_webhook_receive_document/GB')
async def webhook_receive_document_london(request: ReceiveInvoiceWebhookListItem):
    return await storecove_webhook_receive_document(request, '11')

@app.post('/storecove_webhook_receive_document/BE')
async def webhook_receive_document_antwerp(request: ReceiveInvoiceWebhookListItem):
    return await storecove_webhook_receive_document(request, '12')

async def storecove_webhook_receive_document(request: ReceiveInvoiceWebhookListItem,
                                             branch_code: str):
                                            #  authorization: str = Header(None)):

    # storecove_webhook_user = os.getenv("STORECOVE_WEBHOOK_USER")
    # storecove_webhook_pass = os.getenv("STORECOVE_WEBHOOK_PASSWORD")


    # if storecove_webhook_user and storecove_webhook_pass:
    #     if not authorization or not authorization.startswith("Basic "):
    #         raise HTTPException(status_code=401, detail='Auth required')

    #     import base64
    #     encoded = authorization.split(" ")[1]
    #     decoded = base64.b64decode(encoded).decode()
    #     user, password = decoded.split(":", 1)

    #     if user != storecove_webhook_user or password != storecove_webhook_pass:
    #         raise HTTPException(status_code=403, detail='Invalid credentials')

    received_time = datetime.now()
    uid = request.document_guid
    with open('/home/sayaka_yanagi/projects/swe_einvoice_etl/data.json', 'w') as f:
        json.dump(request.dict(), f, indent=4)    
    engine = get_engine(user, password, database, host, port)
    res = load_received_invoice_db(engine, uid, branch_code, received_time)
    if res:
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=500, detail='Internal Server error')


