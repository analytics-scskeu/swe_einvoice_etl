CREATE TABLE customer (
    company_code VARCHAR(5),
    branch_code VARCHAR(5) NOT NULL,
    vat_id VARCHAR(30) NOT NULL,
    customer_code CHAR(3) NOT NULL,
    customer_name VARCHAR(100),
    country_code CHAR(2),
    peppol_id VARCHAR(30),
    sending_method VARCHAR(20),
    peppol_available CHAR(1),
    last_peppol_check TIMESTAMP,
    primary_email_address VARCHAR(300),
    secondary_email_addresses TEXT,
    last_update TIMESTAMP NOT NULL,
    b2x CHAR(1),
    peppol_scheme VARCHAR(15),
    PRIMARY KEY (branch_code, vat_id, customer_code)
);

