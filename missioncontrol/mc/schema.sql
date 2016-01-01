drop table if exists answers;
create table answers (
    id integer primary key autoincrement,
    team_id integer not null,
    mission_id integer not null,
    answer_text text not null,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

drop table if exists questions;
create table questions (
    id integer primary key autoincrement,
    mission_id integer not null,
    question_text text not null,
    answer_text text not null,
    photo_path text not null
);

drop table if exists sample_types;
create table sample_types (
    id integer primary key autoincrement,
    min float not null,
    max float not null,
    name text not null
);

drop table if exists samples;
create table samples (
    id integer primary key autoincrement,
    team_id integer not null,
    type_id integer not null,
    x integer not null,
    y integer not null,
    value float not null,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

drop table if exists photos;
create table photos (
    id integer primary key autoincrement,
    team_id integer not null,
    x integer not null,
    y integer not null,
    path text not null,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

drop table if exists schools;
create table schools (
    id integer primary key autoincrement,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    points integer default 0,
    name text not null
);

drop table if exists teams;
create table teams (
    id integer primary key autoincrement,
    points integer default 0,
    name text not null
);
