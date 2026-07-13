-- Revenue & Film Performance

-- Generate a dataset that shows, for every film:
-- Film title
-- Category
-- Total rental revenue
-- Total number of rentals
-- Average revenue per rental
-- Last rental date

SELECT 
    film.film_id,
	film.title AS film,
	film.length,
	category.category_id,
    category.name AS category,
    COALESCE(SUM(payment.amount), 0.00) AS total_revenue,
    COUNT(rental.rental_id) AS total_rent,
    COALESCE(ROUND(AVG(payment.amount), 2), 0.00) AS average_rental_revenue,
    MAX(rental.rental_date):: DATE AS last_rental_date
FROM film 
JOIN film_category  ON film.film_id = film_category.film_id
JOIN category ON film_category.category_id = category.category_id
LEFT JOIN inventory ON film.film_id = inventory.film_id
LEFT JOIN rental  ON inventory.inventory_id = rental.inventory_id
LEFT JOIN payment ON rental.rental_id = payment.rental_id
GROUP BY 
    film.title, 
    category.category_id,
	category.name,
	film.film_id
ORDER BY film;
