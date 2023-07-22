CREATE TABLE IF NOT EXISTS users(
    id serial primary key,
    username VARCHAR,
    urlPic VARCHAR,
    address VARCHAR);

CREATE TABLE IF NOT EXISTS users_token(
    user_id serial primary key,
    access_token VARCHAR,
    expire_date timestamp);

CREATE TABLE iF NOT EXISTS subscriptions(
    reader_id INTEGER,
    author_id INTEGER
);

CREATE TABLE IF NOT EXISTS papers(
    id serial primary key,
    publicDate timestamp,
    user_id INTEGER
);

CREATE TABLE IF NOT EXISTS cuts(
    id serial primary key,
    fileUrl VARCHAR,
    authorId INTEGER,
    publicDate timestamp,
    paid bool
)