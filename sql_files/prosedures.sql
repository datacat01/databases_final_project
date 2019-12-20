-- DROP PROCEDURE IF EXISTS create_reservation;
DROP PROCEDURE IF EXISTS add_client;
-- DROP PROCEDURE IF EXISTS client_arrived;
DELIMITER //
CREATE PROCEDURE add_client(
in usr_id bigint,
in client_name varchar(20),
in client_phone varchar(13),
out client_id int
)
BEGIN
    IF EXISTS (SELECT id from `client` WHERE (`client`.usr_id = usr_id) AND (`client`.phone = client_phone)) THEN
		BEGIN
			SET client_id =(SELECT id from `client` WHERE (`client`.usr_id = usr_id COLLATE utf8_unicode_ci) AND (`client`.phone = client_phone));
		END;
		ELSE
		BEGIN
			INSERT INTO `client`(usr_id, `name`, phone)
			VALUES (usr_id, client_name, client_phone);
			SET client_id = @@identity;
		END;
		END IF;
END //



CREATE PROCEDURE add_client_in(
in usr_id bigint,
in client_name varchar(20),
in client_phone varchar(13)
)
BEGIN
    IF NOT EXISTS (SELECT id from `client` WHERE (`client`.usr_id = usr_id) AND (`client`.phone = client_phone)) THEN
		BEGIN
			INSERT INTO `client`(usr_id, `name`, phone)
			VALUES (usr_id, client_name, client_phone);
		END;
	END IF;
END //



CREATE PROCEDURE create_reservation(
in usr_id bigint,
in client_name varchar(20),
in client_phone varchar(13),
in pers_count smallint,
in time_from timestamp,
in time_to timestamp
)

BEGIN
    DECLARE client_id int;
    DECLARE available_table_id int;
	CALL add_client(usr_id, client_name, client_phone, client_id);
    SET 
		available_table_id = (
		SELECT`table`.id
		FROM reservation
		RIGHT JOIN `table` ON `table`.id = reservation.table_id
		WHERE
			(IFNULL(reservation.time_from, '1999-10-14 20:00') <= time_to) AND (IFNULL(reservation.time_to, '2055-10-14 20:00') >= time_from) AND
			(`table`.pers_count BETWEEN pers_count AND (pers_count+2)) AND (`table`.usr_id = usr_id)
		ORDER BY `table`.pers_count
		LIMIT 1);
    IF available_table_id is not NULL THEN
		BEGIN
			INSERT INTO reservation(usr_id, table_id, client_id, time_from, time_to)
			VALUES (usr_id, available_table_id, client_id, time_from, time_to);
		END;
	END IF;
END //



CREATE PROCEDURE client_arrived(
in usr_id bigint,
in reserv_id int,
in arrival_time timestamp
)
BEGIN
	UPDATE reservation
    SET
		cli_arrived = arrival_time
	WHERE
		(reservation.id = reserv_id) AND (reservation.usr_id = usr_id);
END //
 
 

CREATE PROCEDURE delete_reservation(
in usr_id bigint,
in reserv_id int
)
BEGIN
	DELETE FROM reservation
	WHERE
		(reservation.id = reserv_id) AND (reservation.usr_id = usr_id);
END //



CREATE PROCEDURE add_order(
	in usr_id bigint,
	in reservation_id int,
    in price decimal(7,2),
    in order_time timestamp,
    in payment_time timestamp
)
BEGIN
	INSERT INTO `order`(usr_id, reservation_id, price, order_time, payment_time)
	VALUES
		(usr_id, reservation_id, price, order_time, payment_time);
END //


CREATE PROCEDURE add_order_not_reserved(
	in usr_id bigint,
    in price decimal(7,2),
    in order_time timestamp,
    in payment_time timestamp
)
BEGIN
	INSERT INTO `order`(usr_id, price, order_time, payment_time)
	VALUES
		(usr_id, price, order_time, payment_time);
END //



CREATE PROCEDURE add_order_item(
	in usr_id bigint,
	in order_id int,
	in dish_id int,
    in amount int
)
BEGIN
	INSERT INTO order_item(usr_id, dish_id, order_id, amount)
	VALUES
		(usr_id, dish_id, order_id, amount);
END //



CREATE PROCEDURE remove_order_item(
	in usr_id bigint,
	in order_id int,
	in dish_id int
)
BEGIN
	DELETE FROM order_item
	WHERE
		(order_item.dish_id = dish_id) AND (order_item.order_id = order_id) AND (order_item.usr_id = usr_id);
END //



CREATE PROCEDURE remove_order(
	in id int
)
BEGIN
	DELETE FROM order_item
    WHERE
		order_item.order_id = id;
	DELETE FROM `order`
	WHERE
		`order`.id = id;
END //


DELIMITER //
CREATE PROCEDURE add_user(
-- email, name, organization_name, password
in email varchar(30),
in `name` varchar(30),
in org_name varchar(50),
in `password-hash` varchar(200)
)
BEGIN
    IF NOT EXISTS (SELECT id from users WHERE users.`e-mail` = email) THEN
		BEGIN
            INSERT INTO users(`e-mail`, `name`, org_name, `password-hash`)
			VALUES (email, `name`, org_name, `password-hash`);
		END;
		END IF;
END //



CREATE PROCEDURE add_dish(
in usr_id bigint unsigned,
in `name` varchar(50),
in cost decimal(7,2)
)
BEGIN
    IF NOT EXISTS (SELECT id from dish WHERE (dish.usr_id = usr_id) and (dish.`name` = `name`)) THEN
		BEGIN
            INSERT INTO dish(usr_id, `name`, cost)
			VALUES (usr_id, `name`, cost);
		END;
		END IF;
END //


CREATE PROCEDURE rm_tbl(
in usr_id bigint,
in tbl_id smallint
)
BEGIN
    DELETE FROM `table` WHERE (usr_id=usr_id AND id=tbl_id);
END //



CREATE PROCEDURE rm_reservation(
	`usr_id` bigint,
    `res_id` smallint
)
BEGIN
    DELETE FROM `reservation` WHERE (id=res_id AND usr_id=usr_id);
END //



CREATE PROCEDURE get_ord_itm_dish_name(
	u bigint,
    o int
)
BEGIN
    SELECT `name`, `amount`
	FROM `order_item` 
	LEFT JOIN dish on (dish.id=order_item.dish_id)
	WHERE order_item.`usr_id`=u AND `order_id`=o;
END //



DELIMITER ;