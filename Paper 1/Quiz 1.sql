Use BikeStores
Go

-- 1.  (Easy)  List every order with the customer's full name, store name, 
-- and the full name of the staff member who handled it.

select c.first_name + ' ' +c.last_name as Customer_name,
	o.order_id,
	st.first_name + ' ' +st.last_name as Staff_name,
	s.store_name

	from sales.customers as c
	inner join sales.orders as o
	on c.customer_id = o.customer_id

	inner join sales.staffs as st
	on  o.staff_id = st.staff_id

	inner join sales.stores as s
	on st.store_id = s.store_id;

	   

-- 2.  (Easy)  Show each product with its brand name 
-- and category name. Include products even 
-- if they have no brand or category assigned.


select p.product_name,
	b.brand_name,
	c.category_name 
from production.products as p
inner join production.brands as b
on p.brand_id = b.brand_id
inner join production.categories as c
on p.category_id = c.category_id;



-- 3.  (Medium)  Find all customers who have 
-- never placed an order. Return their name, city, and email.

select 
	c.first_name + ' ' +c.last_name as Customer_name,
	c.city,
	c.email,
	o.order_status
	from sales.customers as c
	full outer join sales.orders as o
	on c.customer_id = o.customer_id
	where o.order_status is NULL;


-- 4.  (Easy)  Calculate total revenue per store. 
-- Revenue = quantity * list_price * (1 - discount). 
-- Sort from highest to lowest.

select 
	  o.customer_id,
	  SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS Total_Revenue
	  from sales.orders as o
	  inner join sales.order_items as  oi
	  on o.order_id = oi.order_id
	  group by o.customer_id
	  order by total_revenue desc;


--5.  (Medium)  For each brand, show the number of products, 
--the average list price, and the highest list price. 
--Only include brands with more than 5 products.

select b.*,
	count(p.product_id) as total_products,
	avg(p.list_price) as Avg_list_per_brand,
	max(p.list_price) as Highest_list_price
	from production.brands as b
	inner join  production.products as p
	on b.brand_id = p.brand_id
	group by b.brand_name, b.brand_id 
	having count(p.product_id)> 5;


-- 6.  (Medium)  Show the number of orders and 
-- total revenue per month for the year 2017, 
-- ordered chronologically.

SELECT 
    MONTH(o.order_date) AS order_month,
    COUNT(DISTINCT o.order_id) AS Total_number_of_orders,
    SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS Total_Revenue
FROM sales.orders AS o
INNER JOIN sales.order_items AS oi
    ON o.order_id = oi.order_id
WHERE YEAR(o.order_date) = 2017
GROUP BY MONTH(o.order_date)
ORDER BY order_month;


--7.  (Medium)  Find all products priced above the 
-- average list price of their own category.
-- Hint: Use a correlated subquery.

select *
	from production.products p1
	where list_price >All (
	select avg(p2.list_price)
	from production.products p2
	where p2.category_id = p1.category_id
	group by p2.category_id) 
	order by product_name asc;
	

-- 8.  (Medium)  List the customers who have placed more 
-- orders than the average number of orders per customer.

select * from sales.customers 
where customer_id in (
select customer_id from sales.orders
group by customer_id
Having count(order_id) > (
Select AVG (order_count)
from (
select count(order_id) AS order_count
from sales.orders
group by customer_id) AS customer_order_count));


--9.  (Hard)  Using a CTE, calculate each 
--customer's total spend, then return the top 10 customers 
--with their spend and rank. Add a second CTE that 
--labels each customer as "High" 
--(above the overall average spend) or "Regular".

WITH CustomerSpend AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_spend
    FROM sales.customers AS c
    INNER JOIN sales.orders AS o
        ON c.customer_id = o.customer_id
    INNER JOIN sales.order_items AS oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.first_name, c.last_name
),
CustomerLabel AS (
    SELECT 
        customer_id,
        first_name,
        last_name,
        total_spend,
        CASE 
            WHEN total_spend > (SELECT AVG(total_spend) FROM CustomerSpend)
            THEN 'High'
            ELSE 'Regular'
        END AS spend_label
    FROM CustomerSpend
)
SELECT TOP 10
    customer_id,
    first_name,
    last_name,
    total_spend,
    spend_label
FROM CustomerLabel
ORDER BY total_spend DESC;


--10.  (Hard)  Using CTEs, find the best-selling product 
--(by quantity) in each category, and show how much of that 
--product's stock is currently available across all stores.
--Hint: Use ROW_NUMBER() or RANK() partitioned by category, 
--then join to production.stocks.

WITH ProductSales AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category_id,
        c.category_name,
        SUM(oi.quantity) AS total_quantity_sold
    FROM production.products AS p
    INNER JOIN production.categories AS c
        ON p.category_id = c.category_id
    INNER JOIN sales.order_items AS oi
        ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name, p.category_id, c.category_name
),

RankedProducts AS (
    SELECT 
        product_id,
        product_name,
        category_id,
        category_name,
        total_quantity_sold,
        ROW_NUMBER() OVER (
            PARTITION BY category_id 
            ORDER BY total_quantity_sold DESC
        ) AS sales_rank
    FROM ProductSales
)

SELECT 
    rp.category_name,
    rp.product_name,
    rp.total_quantity_sold,
    SUM(s.quantity) AS total_stock_available
FROM RankedProducts AS rp
INNER JOIN production.stocks AS s
    ON rp.product_id = s.product_id
WHERE rp.sales_rank = 1
GROUP BY rp.category_name, rp.product_name, rp.total_quantity_sold
ORDER BY rp.category_name;




--Bonus Challenges
--Rewrite Q8 using a CTE instead of a subquery and 
--compare readability.

WITH Customer_Order_Counts AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS order_count
    FROM sales.orders
    GROUP BY customer_id
),

Average_Orders AS (
    SELECT AVG(order_count) AS avg_order_count
    FROM Customer_Order_Counts
)

SELECT c.*
FROM sales.customers AS c
INNER JOIN Customer_Order_Counts AS coc
    ON c.customer_id = coc.customer_id
CROSS JOIN Average_Orders AS ao
WHERE coc.order_count > ao.avg_order_count;



--For Q4, add a column showing each store's percentage 
--share of total company revenue. 
--4.  (Easy)  Calculate total revenue per store. 
--Revenue = quantity * list_price * (1 - discount). 
--Sort from highest to lowest.

SELECT 
    s.store_id,
    s.store_name,
    SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_revenue,
    ROUND(
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) * 100.0 
        / SUM(SUM(oi.quantity * oi.list_price * (1 - oi.discount))) OVER (), 
        2
    ) AS revenue_percentage_share
FROM sales.stores AS s
INNER JOIN sales.orders AS o
    ON s.store_id = o.store_id
INNER JOIN sales.order_items AS oi
    ON o.order_id = oi.order_id
GROUP BY s.store_id, s.store_name
ORDER BY total_revenue DESC;