from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()


class CustomerListItem(BaseModel):
    branch_code : str
    vat_id : str
    code : str
    b2x : Optional[str] = None
    peppol_scheme : Optional[str] = None
    peppol_id : Optional[str] = None
    sending_method : Optional[str] = None
    secondary_email_addresses : Optional[str] = None

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

@app.post("/update_customer_supplier_db")
def update_customer_supplier_db(request : CustomerUpdateRequest):
    return {"message" : "success"}

@app.post("/storecove_webhook_receive_document")
async def storecove_webhook_receive_document(request: ReceiveInvoiceWebhookListItem):
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


    import json
    with open('/home/sayaka_yanagi/projects/swe_einvoice_etl/data.json', 'w') as f:
        json.dump(request.dict(), f, indent=4)
    print("Storecove webhook received:")

    return {"status": "ok"}
