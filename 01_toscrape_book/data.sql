CREATE DATABASE IF NOT EXISTS scrapy_db CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

CREATE TABLE `books` (
  `upc` char(16) NOT NULL,
  `name` varchar(256) NOT NULL,
  `price` varchar(16) NOT NULL,
  `review_rating` int(11) DEFAULT NULL,
  `review_num` int(11) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  PRIMARY KEY (`upc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
