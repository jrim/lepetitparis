drop table if exists entries;
create table entries(
	id integer primary key autoincrement,
	title string not null,
	text string not null
);
drop table if exists userinfo;
create table userinfo(
	id integer primary key autoincrement,
	username string not null,
	s1 integer,
	s2 integer,
	s3 integer,
	trend string
);
