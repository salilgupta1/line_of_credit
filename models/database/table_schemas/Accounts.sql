--Table Structure for Accounts

CREATE TABLE IF NOT EXISTS accounts(
	account_id serial Primary Key,
	user_name varchar(64) REFERENCES "users"(username)
		ON DELETE CASCADE,
	credit_limit NUMERIC(8,2) NOT NULL,
	apr NUMERIC(3,2) NOT NULL,
	principal NUMERIC(8,2) NOT NULL DEFAULT 0.00,
	interest NUMERIC(8,2) NOT NULL DEFAULT 0.00
);