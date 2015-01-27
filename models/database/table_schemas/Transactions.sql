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