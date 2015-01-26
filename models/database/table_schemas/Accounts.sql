--Table Structure for Accounts

CREATE TABLE IF NOT EXISTS accounts(
	account_id serial Primary Key,
	user_name varchar(64) REFERENCES "users"(username)
		ON DELETE CASCADE,
	credit_limit NUMERIC NOT NULL,
	apr NUMERIC NOT NULL,
	principal NUMERIC NOT NULL,
	date_created timestamp NOT NULL
);