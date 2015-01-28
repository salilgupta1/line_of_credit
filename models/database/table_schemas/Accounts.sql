--Table Structure for Accounts

CREATE TABLE IF NOT EXISTS accounts(
	account_id serial Primary Key,
	user_name varchar(64) REFERENCES "users"(username)
		ON DELETE CASCADE,
	credit_limit NUMERIC(8,2) NOT NULL,
	apr NUMERIC(3,2) NOT NULL,
	principal NUMERIC(8,2) NOT NULL DEFAULT 0.00,
	interest NUMERIC(8,2) NOT NULL DEFAULT 0.00,

	constraint positive_credit check (credit_limit >=0.00),
	constraint postive_interest check (interest >=0.00)
);

CREATE TRIGGER check_principal
	AFTER UPDATE OF principal on accounts
	FOR EACH ROW
	WHEN (NEW.principal < 0.00)
	EXECUTE PROCEDURE set_principal();

CREATE FUNCTION set_principal() RETURNS TRIGGER AS $zero_principal$
    BEGIN
    	UPDATE accounts set principal=0.0, credit_limit=new.credit_limit where account_id=new.account_id;
        RETURN NEW;
    END;
$zero_principal$ LANGUAGE plpgsql;