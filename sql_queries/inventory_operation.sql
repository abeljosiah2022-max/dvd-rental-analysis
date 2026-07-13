-- Inventory & Operations
-- Generate a dataset that shows, for every film:
-- Film title
-- Category
-- Inventory count
-- Total rentals
-- Total revenue
-- Last rental date
-- Average rental duration


SELECT
	film.film_id,
	film.title AS film_title,
	category.category_id,
	category.name AS category,
	inventory.store_id,
	COUNT(DISTINCT inventory.inventory_id) AS inventory_count,
	COUNT(rental.rental_id) AS total_rent,
	ROUND(SUM(payment.amount), 2) AS total_revenue,
	MAX(rental.rental_date)::DATE AS last_rental_date,
	ROUND(AVG(film.rental_duration), 0) AS average_rental_duration

FROM film
LEFT JOIN film_category ON film.film_id = film_category.film_id
LEFT JOIN category ON film_category.category_id = category.category_id
LEFT JOIN inventory ON film.film_id = inventory.film_id
LEFT JOIN rental ON inventory.inventory_id = rental.inventory_id
LEFT JOIN payment ON rental.rental_id = payment.rental_id

GROUP BY
	film.film_id,
	film.title,
	inventory.store_id,
	category.category_id,
	category.name

ORDER BY total_rent DESC;