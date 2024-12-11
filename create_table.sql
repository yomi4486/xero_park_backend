CREATE TABLE pages (
    id SERIAL,
    title varchar(64) NOT NULL,
    datail varchar(2048) NOT NULL,
    author varchar(32) NOT NULL,
    firsttime TIMESTAMP,
    lastedit date,
    tags varchar(4096),
    PRIMARY KEY (id)
);