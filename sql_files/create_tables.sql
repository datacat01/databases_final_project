CREATE TABLE `ingredient`(
	`id` int unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `name` varchar(20) NOT NULL,
    `net_cost_kg` decimal(7,2) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name_idx` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `dish`(
	`id` int unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `name` varchar(50),
    `cost` decimal(7,2) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `dish_ingredient`(
	`id` int unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `dish_id` int unsigned NOT NULL,
    `ingredient_id` int unsigned NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`dish_id`) REFERENCES `dish` (`id`),
    FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `table`(
	`id` smallint unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `pers_count` smallint unsigned NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `client`(
	`id` int unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `name` varchar(20),
    `phone` varchar(13),
    PRIMARY KEY (`id`),
    UNIQUE KEY `phone_idx` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `reservation`(
	`id` int unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `table_id` smallint unsigned NOT NULL,
    `client_id` int unsigned NOT NULL,
    `time_from` timestamp NULL DEFAULT NULL,
    `time_to` timestamp NULL DEFAULT NULL,
    -- `cli_arrived` timestamp,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`table_id`) REFERENCES `table` (`id`),
    FOREIGN KEY (`client_id`) REFERENCES `client` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- DROP TABLE IF EXISTS `sales_log`;
-- DROP TABLE IF EXISTS `order_item`;
-- DROP TABLE IF EXISTS `order`;
CREATE TABLE `order`(
	`id` int unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `reservation_id` int unsigned,
    `price` decimal(7,2) NOT NULL,
    `order_time` timestamp NULL DEFAULT NULL,
    `payment_time` timestamp NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`reservation_id`) REFERENCES `reservation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `order_item`(
	`id` int unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `dish_id` int unsigned NOT NULL,
    `order_id` int unsigned NOT NULL,
    `amount` smallint unsigned NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`dish_id`) REFERENCES `dish` (`id`),
    FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `sales_log`(
	`id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `usr_id` bigint unsigned NOT NULL,
    `order_id` int unsigned NOT NULL,
    `order_time` timestamp NULL DEFAULT NULL,
    `payment_time` timestamp NULL DEFAULT NULL,
    `price` decimal(7,2),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE users(
	`id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `e-mail` varchar(30) NOT NULL,
    `name` varchar(30),
    `org_name` varchar(50),
    `password-hash` varchar(200) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;






