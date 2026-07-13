-- Store & Staff Performance
-- Generate a dataset that shows, for each store and staff member:

-- Store ID
-- Staff name
-- Total rentals processed
-- Total revenue collected
-- Number of unique customers served
-- Average rentals per day

SELECT
	store.store_id,
	staff.staff_id,
	staff.first_name || ' ' || staff.last_name AS staff_name,
	COUNT(rental.rental_id) AS total_rentals_processed,
	ROUND(SUM(payment.amount), 2) AS total_revenue_collected,
	COUNT(DISTINCT rental.customer_id) AS unique_customers_served,
	ROUND(COUNT(rental.rental_id)::numeric / COUNT(DATE(rental.rental_date)), 0) AS average_daily_rent

FROM staff 
JOIN store 
ON staff.store_id=store.store_id
JOIN payment 
ON staff.staff_id=payment.staff_id
JOIN rental
ON payment.rental_id=rental.rental_id

GROUP BY
store.store_id,
staff.staff_id,
staff_name

ORDER BY staff_id;