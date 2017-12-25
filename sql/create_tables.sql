drop table if exists entries;

create table users (
	user_id int primary key auto_increment,
	username varchar(20),
	firstname varchar(20), 
	lastname varchar(20),
	password varchar(256),
	email varchar(40)
)