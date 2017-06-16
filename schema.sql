drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    station_id integer not null,
    vote_url text not null,
    public_key text not null
);
