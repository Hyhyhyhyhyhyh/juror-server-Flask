create database court_db default charset utf8;
create user `system`@'127.0.0.1' identified with mysql_native_password by "H5cT7yHB8_";
grant all privileges on court_db.* to `system`@'127.0.0.1';
flush privileges;

CREATE TABLE users (
    userid         char(11) NOT NULL,
    password       varchar(30) DEFAULT NULL,
    username       varchar(30) DEFAULT NULL,
    auth_type      int(11) NOT NULL,
    jurorid        int(11) NOT NULL,
    last_login     timestamp DEFAULT null,
    last_modified  timestamp default current_timestamp() on update current_timestamp(),
    account_status varchar(10) DEFAULT NULL,
    created        timestamp DEFAULT current_timestamp(),
    dept_id        int DEFAULT 0,
    PRIMARY KEY (userid)
);

create table cases(
    caseid         int auto_increment,
    casecode       int not null,
    dept           int not null,
    case_manager   int not null,
    status         int not null,
    jurorid        int not null,
    created        timestamp DEFAULT current_timestamp(),
    last_modified  timestamp default current_timestamp() on update current_timestamp(),
    PRIMARY KEY (caseid)
);

create table case_type(
    id   int PRIMARY KEY,
    name varchar(30)
);

create table dept(
    id      int auto_increment PRIMARY key,
    name    varchar(100),
    level   varchar(20) comment '1直属,0地方',
    city    varchar(20),
    region  varchar(20)
);

create table juror(
    id          int auto_increment PRIMARY key,
    name        varchar(20),
    sex         varchar(2),
    phone       char(11),
    dept_id     int,
    juror_type  int,
    address     varchar(1000),
    case_count  int,
    created        timestamp DEFAULT current_timestamp()
);