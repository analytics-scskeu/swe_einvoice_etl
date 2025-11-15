import pandas as pd
from datetime import datetime
import os

def convert_csv_2_json(csv_invoice):

    """
    Convert csv-format invoice into json 
    """
    # Read csv file
    df = pd.read_csv(csv_invoice)

    # Map columns
    phone_number = os.environ['SWE_PHONE_NUMBER']

    company_name = df['CompanyName'].unique()[0]
    office = df['OfficeName'].unique()[0]
    address = df['OfficeAddress'].unique()[0]
    phone_number = phone_number   
    client_name = df['ClientName'].unique()[0]
    clieint_country = 'Belgium'
    client_addrss1 = 'FOTOGRAFIELAAN 37-39'
    client_postcode = 'BE-2610' 
    client_county = 'Antwerp'
    invoice_number = df['SeikyuNo'].unique()[0]
    invoice_date = df['SeikyuDate'].unique()[0]
    due_date = df['Paykijitu'].unique()[0]
    date_obj = datetime.strptime(invoice_date, "%d/%m/%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")`

    # Line items
    invoice_lines = []
    for i in range(len(df)):

        dic = {
            "name": df['SeikyuItemName'][i],
            "amountExcludingVat": float(df['Amount'][i]),
            "itemPrice" : float(df['SalesTanka'][i]),
            "quantity" : float(df['Qty'][i]),
            "tax": {
                "percentage": 0,
                "category": "zero_rated",
                "country": "BE"
                }
            }
        invoice_lines.append(dic)

        # Numerical columns
        net_sales = float(sum(df['VATBasis']))
        vat_amount = float(sum(df['VATAmount']))
        total_sales = float(sum(df['Total']))
        doc_currency = df['SeikyuCurrency'].unique()[0]

        invoice_json = {
            "legalEntityId": 376972,
            "routing": {
            "emails": [
                "sayaka.yanagi@scskeu.com"
            ],
            "eIdentifiers": [
                {
                "scheme": "GB:VAT",
                "id": "GB577487969"
                }
            ]
            },
            "document": {
            "documentType": "invoice",
            "invoice": {
                "invoiceNumber":invoice_number,
                "issueDate": formatted_date,
                "documentCurrencyCode": doc_currency,
                "taxSystem": "tax_line_percentages",
                "note" : "50 CART (AUTO PARTS) \n AUTO PARTS \n 153000.00 GW /  150000.00 NW /  226.875 M3",
                "paymentTerms" : {
                "note" : "Conditions: \n All our transactions are subject to the Belgian Freight Forwarding Standard Trading Conditions 2005. The text of those Conditions has been published under number 05090237 in the Annexe as Moniteur Belge dated June 24th, 2005, and is available free of charge upon request."
                },
                "accountingCustomerParty": {
                "party": {
                    "companyName": client_name,
                    "address": {
                    "street1": client_addrss1,
                    "zip": client_postcode,
                    "city": client_county,
                    "country": "GB"
                    }
                },
                "publicIdentifiers": [
                    {
                    "scheme": "GB:VAT",
                    "id": "GB577487969"
                    }
                ]
                },
                "accountingSupplierParty": {
                "party": {
                    "companyName": "SUMITOMO WAREHOUSE (EUROPE) GMBH",
                    "address": {
                    "street1": "Fotografielaan 37-39",
                    "zip": "B-2610",
                    "city": "Wilrijk-Antwerpen",
                    "country": "BE"
                    }
                },
                "publicIdentifiers": [
                    {
                    "scheme": "BE:EN",
                    "id": "0425855239"
                    }
                ]
                },
                "invoiceLines": invoice_lines,
                "taxSubtotals": [
                {
                    "percentage": 0,
                    "category": "zero_rated",
                    "country": "BE",
                    "taxableAmount": net_sales,
                    "taxAmount": vat_amount
                }
                ],
                "paymentMeansArray": [
                    {
                    "code": "sepa_credit_transfer",
                    "account": "BE69 3200 5611 5378",
                    "branche_code": "BBRUBEBB"
                    },
                    {
                    "code": "credit_transfer",
                    "account": "189-2870370-51"
                    }
                ],
                "amountIncludingVat": total_sales
            }
            }
        }

    return invoice_json
    
