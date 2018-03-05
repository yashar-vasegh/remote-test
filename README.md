this app will get a url , read url, create a dict of words and insert it into db. but what is store in db is (hash) of word as primary id, so all searches will be on this hash key, (value) which will be encrypted output of words and (count) this word heppends totally in url crawls.

encryption use user key, user key validated by comparing the result of encryption(user key, public key, predefine string) with stored value of result encryption.easy!

database schema:

CREATE SCHEMA `remote_test` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;

CREATE TABLE `data` (
  `id` varchar(200) COLLATE utf8_bin NOT NULL,
  `word` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

private_key is 'hahahahahahahaha'
