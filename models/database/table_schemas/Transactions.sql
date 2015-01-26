--Table Structure for Transactions

CREATE TYPE transaction_type AS ENUM ('draw', 'payment');

CREATE TABLE IF NOT EXISTS transactions(
	transaction_id serial Primary Key,
	accountid INT REFERENCES "accounts"(account_id)
		ON DELETE CASCADE,
	date_of_transaction timestamp NOT NULL,
	amount NUMERIC NOT NULL,
	trans_type transaction_type NOT NULL 
);