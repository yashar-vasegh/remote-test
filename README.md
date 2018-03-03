database schema:

CREATE SCHEMA `remote_test` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
CREATE TABLE `data` (
  `id` varchar(200) COLLATE utf8_bin NOT NULL,
  `word` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


private_key is 'hahahahahahahaha'