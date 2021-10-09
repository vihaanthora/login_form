create database if not exists logindb;
use logindb;
create table if not exists user_data (
	sr_no int primary key auto_increment,
    user_id varchar(30) not null,
    password varchar(30) not null,
    mobile_no varchar(10) not null
);
select * from user_data;
delete from user_data;
drop table user_data;