CREATE TABLE `history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` varchar(20) NOT NULL DEFAULT '',
  `status` varchar(10) NOT NULL DEFAULT '',
  `result` int(11) NOT NULL DEFAULT 0,
  `machine_id` varchar(10) NOT NULL DEFAULT '',
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
);

alter table imgs add constraint history_id foreign key(history_id) references history(id);

CREATE TABLE `test2`.`imgs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
	`txt` varchar(255) NOT NULL DEFAULT '',
  `img` varchar(255) NOT NULL DEFAULT '',
  `img1` varchar(255) NOT NULL DEFAULT '',
	`img2` varchar(255) NOT NULL DEFAULT '',
	`img3` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
);