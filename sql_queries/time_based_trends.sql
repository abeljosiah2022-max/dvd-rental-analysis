-- Time-Based Business Trends
-- Generate a dataset that shows, for each month:
-- Year and month
-- Total rentals
-- Total revenue
-- Number of unique customers
-- Average revenue per rental

SELECT 
	TO_CHAR(rental.rental_date, 'YYYY') AS year,
	TO_CHAR(DATE_TRUNC('month', rental.rental_date), 'Month') AS month, 
    COUNT(rental.rental_id) AS total_rentals, 
    ROUND(SUM(payment.amount), 2) AS total_revenue, 
    COUNT(DISTINCT rental.customer_id) AS unique_customers, 
    ROUND(AVG(payment.amount), 2) AS average_rental_revenue 
FROM rental 
JOIN payment ON rental.rental_id = payment.rental_id 
GROUP BY TO_CHAR(rental.rental_date, 'YYYY'), DATE_TRUNC('month', rental.rental_date);