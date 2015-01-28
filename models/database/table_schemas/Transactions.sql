--Table Structure for Transactions

CREATE TYPE transaction_type AS ENUM ('draw', 'payment');

CREATE TABLE IF NOT EXISTS transactions(
	transaction_id serial Primary Key,
	accountid INT REFERENCES "accounts"(account_id)
		ON DELETE CASCADE,
	transaction_day INT NOT NULL,
	amount NUMERIC(8,2) NOT NULL,
	trans_type transaction_type NOT NULL,
	principal_after_trans NUMERIC(8,2) NOT NULL
);

CREATE TRIGGER principal_after_trans
	AFTER INSERT on transactions
	FOR EACH ROW
	WHEN (NEW.principal_after_trans < 0.00)
	EXECUTE PROCEDURE set_principal_after_trans();

CREATE FUNCTION set_principal_after_trans() RETURNS TRIGGER AS $zero_principal$
    BEGIN
    	UPDATE transactions set principal_after_trans=0.0 where transaction_id=new.transaction_id;
        RETURN NEW;
    END;
$zero_principal$ LANGUAGE plpgsql;