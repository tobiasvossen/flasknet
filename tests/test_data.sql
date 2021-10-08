DROP TABLE IF EXISTS user; 
CREATE TABLE user (
  username TEXT UNIQUE NOT NULL,
  prename TEXT NOT NULL,
  surname TEXT NOT NULL
);

INSERT INTO user (username, prename, surname) VALUES ("max.mustermann", "Max", "Mustermann");
INSERT INTO user (username, prename, surname) VALUES ("mara.musterfrau", "Mara", "Musterfrau");

DROP TABLE IF EXISTS messages; 
CREATE TABLE messages (
  sender TEXT NOT NULL,
  receiver TEXT NOT NULL,
  content TEXT NOT NULL
);

INSERT INTO messages (sender, receiver, content) VALUES ("max.mustermann", "mara.musterfrau", "Hello Mara.");
INSERT INTO messages (sender, receiver, content) VALUES ("mara.musterfrau", "max.mustermann", "Hello Max.");
