DELIMITER //

CREATE TRIGGER order_AFTER_INSERT
AFTER INSERT
ON `order`
FOR EACH ROW
BEGIN
	INSERT INTO sales_log(order_id, usr_id, order_time, payment_time, price)
	VALUES
		(NEW.id, NEW.usr_id, NEW.order_time, NEW.payment_time, NEW.price);
END //

DELIMITER ;
