--Table structure for User

CREATE TABLE IF NOT EXISTS "users"(
	username varchar(64) PRIMARY KEY, 
	password char(40) NOT NULL,
	password_salt char(25) NOT NULL,
	date_joined timestamp NOT NULL
);
