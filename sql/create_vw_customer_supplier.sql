CREATE OR REPLACE VIEW vw_customer_supplier AS
SELECT 
    company_code,
    branch_code,
    vat_id,
    customer_code AS code,
    customer_name AS name,
    b2x,
    country_code,
    peppol_scheme,
    peppol_id,
    sending_method,
    peppol_available,
    last_peppol_check,
    primary_email_address,
    secondary_email_addresses,
    0 AS supplier_flag
FROM customer

UNION ALL

SELECT
    company_code,
    branch_code,
    vat_id,
    supplier_code AS code,
    supplier_name AS name,
    b2x,
    country_code,
    peppol_scheme,
    peppol_id,
    sending_method,
    peppol_available,
    last_peppol_check,
    primary_email_address,
    secondary_email_addresses,
    1 AS supplier_flag
FROM supplier;
