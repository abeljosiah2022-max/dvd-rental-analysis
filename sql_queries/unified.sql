-- unified dataset

SELECT 
	rental.rental_id,
	CAST(rental.rental_date AS DATE),
	TO_CHAR(DATE_TRUNC('month', rental.rental_date), 'Month') AS rental_month,
	customer.customer_id,
	customer.first_name || ' ' || customer.last_name AS customer_name,
	COUNT(rental.rental_id) AS total_rents,
	customer.active,
	city.city,
	country.country,
	film.film_id,
	film.title AS film_title,
	category.name AS category,
	film.length,
	inventory.inventory_id,
	staff.store_id,
	staff.staff_id,
	staff.first_name || ' ' || staff.last_name AS staff_name,
	COALESCE(payment.amount, 0.00) AS payment_amount,
	CAST(payment.payment_date AS DATE) AS payment_date,
	film.rental_duration

FROM film 
JOIN film_category  ON film.film_id = film_category.film_id
JOIN category ON film_category.category_id = category.category_id
JOIN inventory ON film.film_id = inventory.film_id
JOIN rental  ON inventory.inventory_id = rental.inventory_id
LEFT JOIN payment ON rental.rental_id = payment.rental_id
JOIN customer ON customer.customer_id = rental.customer_id
JOIN address ON customer.address_id = address.address_id
JOIN city ON address.city_id = city.city_id
JOIN country ON city.country_id = country.country_id
JOIN staff ON rental.staff_id = staff.staff_id

GROUP BY rental.rental_id, inventory.inventory_id, payment.amount, payment.payment_date, staff.staff_id, film.film_id, category.name, country.country, city.city, customer.customer_id

ORDER BY rental_id;

