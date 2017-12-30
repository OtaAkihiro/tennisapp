drop table if exists Users;
drop table if exists Friends;
drop table if exists Photos;
drop table if exists Play;
drop table if exists Results;

create table Users (
	user_id int primary key auto_increment,
	username varchar(20),
	firstname varchar(20), 
	lastname varchar(20),
	password varchar(256),
	email varchar(40),
	rating varchar(3),
	city varchar(20),
	state varchar(20)
);

create table Friends (
	friend_id int primary key auto_increment,
	user_id_1 int not null,
	user_id_2 int not null,
	foreign key (user_id_1) references Users(user_id),
	foreign key (user_id_2) references Users(user_id),
	`date` timestamp default current_timestamp
);

create table Photos (
	pic_id int primary key auto_increment,
	user_id int not null,
	foreign key (user_id) references Users(user_id),
	caption varchar(255),
	profile boolean,
	format char(3),
	`date` timestamp default current_timestamp
);

create table Play (
	style_id int primary key auto_increment,
	user_id int not null,
	foreign key (user_id) references Users(user_id),
	hand ENUM('righty', 'lefty') not null,
	#Following are rated from 1-10, 10 being the best
	forehand int not null,
	backhand int not null,
	volley int not null,
	serve int not null,
	return_serve int not null
);

create table Results (
	match_id int primary key auto_increment,

	user_id_1 int not null,
	user_id_2 int not null,
	user_id_3 int,
	user_id_4 int,
	foreign key (user_id_1) references Users(user_id),
	foreign key (user_id_2) references Users(user_id),
	foreign key (user_id_3) references Users(user_id),
	foreign key (user_id_4) references Users(user_id),
	score varchar (20),
	`date` timestamp default current_timestamp,
	indoor boolean
);

/* The table that will store strategies given players strengths and opponnents weaknesses
create table Strategies (


);

*/
