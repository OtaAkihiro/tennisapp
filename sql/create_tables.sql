drop table if exists entries;

create table users (
	username varchar(20) primary key,
	firstname varchar(20), 
	lastname varchar(20),
	password varchar(256),
	email varchar(40)
)