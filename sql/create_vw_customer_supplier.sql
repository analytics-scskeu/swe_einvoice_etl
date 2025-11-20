CREATE OR REPLACE VIEW vw_customer_supplier AS
SELECT 
    company_code,
    branch_code,
    vat_id,
    code,
    name,
    b2x,
    country_code,
    peppol_scheme,
    peppol_id,
    sending_method,
    peppol_available,
    last_peppol_check,
    primary_email_address,
    secondary_email_addresses,
    supplier_flag
FROM customer_supplier