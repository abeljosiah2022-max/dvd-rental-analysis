-- Customer Behavior & Retention
-- Generate a dataset that shows, for every customer:
-- Full name
-- Country and city
-- Total amount spent
-- Total number of rentals
-- First rental date
-- Most recent rental date
-- Number of rental months


SELECT
	customer.customer_id,
    customer.first_name || ' ' || customer.last_name AS customer_name,
    customer.active,
	country.country_id,
	country.country,
    city.city,
	customer.store_id,
    COALESCE(ROUND(SUM(payment.amount), 2), 0.00) AS total_spent,
    COUNT(rental.rental_id) AS total_rents,
    MIN(rental.rental_date)::DATE AS first_rental_date,
    MAX(rental.rental_date)::DATE AS recent_rental_date,
	CEIL((EXTRACT(EPOCH FROM (MAX(rental.rental_date) - MIN(rental.rental_date))) / 86400) / 30.0) AS rental_months

FROM customer 
JOIN address ON customer.address_id = address.address_id
JOIN city ON address.city_id = city.city_id
JOIN country ON city.country_id = country.country_id
JOIN rental ON customer.customer_id = rental.customer_id
JOIN payment ON rental.rental_id = payment.rental_id

GROUP BY
customer.customer_id,
customer_name,
country.country_id,
country.country,
city.city

