-- Geographic & Market Analysis
-- Generate a dataset that shows, for each country and city:
-- Country
-- City
-- Total rentals
-- Total revenue
-- Number of unique customers
-- Most popular film category

WITH TopCategory AS (

SELECT
	country.country,
	city.city,
	category.name AS category,
	COUNT(*) AS rentals,
	ROW_NUMBER() OVER(
	PARTITION BY country.country,city.city

ORDER BY COUNT(*) DESC

) AS rn

FROM rental 
JOIN customer ON rental.customer_id=customer.customer_id
JOIN address ON customer.address_id = address.address_id
JOIN city ON address.city_id = city.city_id
JOIN country ON city.country_id = country.country_id
JOIN inventory ON rental.inventory_id = inventory.inventory_id
JOIN film_category ON inventory.film_id = film_category.film_id
JOIN category ON film_category.category_id = category.category_id

GROUP BY
	country.country,
	city.city,
	category.name
)

SELECT
	country.country_id,
	country.country,
	city.city,
	COUNT(rental.rental_id) AS total_geo_rent,
	ROUND(SUM(payment.amount),2) AS total_geo_revenue,
	COUNT(DISTINCT customer.customer_id) AS unique_customers,
	TopCategory.category AS top_category
	
FROM customer 
JOIN address ON customer.address_id = address.address_id
JOIN city ON address.city_id = city.city_id
JOIN country ON city.country_id = country.country_id
LEFT JOIN rental ON customer.customer_id = rental.customer_id
LEFT JOIN payment ON rental.rental_id = payment.rental_id

LEFT JOIN TopCategory ON country.country = TopCategory.country
AND city.city = TopCategory.city
AND TopCategory.rn = 1

GROUP BY
	country.country_id,
	country.country,
	city.city,
	TopCategory.category

ORDER BY total_geo_revenue DESC;