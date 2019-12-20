-- DELIMITER //

-- CREATE FUNCTION income_time_period(time_from timestamp, time_to timestamp)
-- RETURNS decimal(14,2)
-- READS SQL DATA
-- DETERMINISTIC
-- BEGIN
-- 	DECLARE income decimal(14,2);
-- 	SET income = (SELECT SUM(price)
--     FROM `order`
--     WHERE `order`.payment_time BETWEEN time_from AND time_to);
--     RETURN income;
-- END //

-- DELIMITER ;


DELIMITER //

CREATE FUNCTION income_total(usr_id int)
RETURNS decimal(20,2)
READS SQL DATA
DETERMINISTIC
BEGIN
	DECLARE income decimal(20,2);
	SET income = (SELECT SUM(price)
    FROM `order`
    WHERE `order`.usr_id = usr_id);
    RETURN income;
END //

DELIMITER ;