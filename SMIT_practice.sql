use BikeStores;
Go

select * from sales.customers;

select * from sales.customers where state != 'TX' ;

select count(first_name) as not_give from sales.customers where phone is not null;
select count(first_name) as give from sales.customers where phone is null;

select top 5 *  from sales.customers where customer_id between 100 and 150
order by city, state desc;

select top 15 first_name +  ' ' + last_name AS full_name
from sales.customers;

select * from production.categories;
--order by products_id desc;

select top 10 * from sales.customers
order by state;

SELECT *
FROM sales.customers
ORDER BY zip_code desc
OFFSET 0 ROWS FETCH NEXT 6 ROWS ONLY;

select top 10 * from sales.customers 
where phone is not null
order by 4 desc;



-- QUERYING
-----------

-- select all columsn and rows
SELECT * FROM sales.customers;

-- select specific columns and all rows
SELECT customer_id, first_name, last_name FROM sales.customers;

-- select specific column first and then all coumns and rows
SELECT phone, * FROM sales.customers;

-- QUERYING & FILTERING
-----------------------

-- select all columsn and rows where states is NY
SELECT * FROM sales.customers WHERE state = 'NY';

-- select all columsn and rows where states is NY or TX
SELECT * FROM sales.customers WHERE state = 'NY' or state = 'TX';

-- select all columsn and rows where states is NY and first_name is Garry
SELECT * FROM sales.customers WHERE first_name = 'Garry' and state = 'TX';

-- select all columsn and rows where states is NOT CA
SELECT min(phone) 
FROM sales.customers 
WHERE state != 'NY' and state != 'TX' and phone is not null;

-- select all columsn and rows where phne number isnt been provided
SELECT * FROM sales.customers WHERE phone IS NULL;

-- select all columsn and rows where customer have provided phone number
SELECT * FROM sales.customers WHERE phone IS NOT NULL;

-- all customers  betwee id 5 to 56
SELECT * FROM sales.customers WHERE customer_id BETWEEN 5 AND 56;

-- OTHERS
---------

-- ALIAS
SELECT
	first_name + ' ' + last_name AS full_name
FROM sales.customers;

SELECT
	last_name AS full_name
FROM sales.customers;

-- LIMITING ROWS
SELECT top 15 * FROM sales.customers;

-- ORDER BY
SELECT *
FROM sales.customers
ORDER BY first_name;

SELECT *
FROM sales.customers
ORDER BY first_name DESC;

SELECT *
FROM sales.customers
ORDER BY state ASC, first_name DESC;

SELECT *
FROM sales.customers
ORDER BY first_name DESC, state ASC;

-- qasim --> CA
-- qasim --> NY

SELECT *
FROM sales.customers
ORDER BY state ASC, first_name DESC;

SELECT *
FROM sales.customers
ORDER BY first_name ASC, last_name DESC;

SELECT *
FROM sales.customers
ORDER BY 8, 2;

-- how to apply limitng on order by using ?
SELECT TOP 10 * FROM sales.customers
ORDER BY first_name;

SELECT
    product_name,
    category_id,
    list_price
FROM production.products
WHERE list_price BETWEEN 300 AND 3000
  AND category_id IN (1, 6)
  AND product_name NOT LIKE '%Frame%'
ORDER BY list_price DESC
OFFSET 3 ROWS FETCH NEXT 10 ROWS ONLY;


-- offset (no of rows skip)
-- fetch (no of rows in output)

select * from sales.customers
where zip_code %2 ! =0 and zip_code >= 10301 and zip_code <= 10500 
order by customer_id;

SELECT product_name, category_id FROM production.products
order by category_id;

SELECT category_id, category_name FROM production.categories;

SELECT top 5
    p.product_name,
    c.category_name,
    p.list_price
FROM production.products AS p
INNER JOIN production.categories AS c
    ON p.category_id = c.category_id;

SELECT product_name, category_id FROM production.products;

SELECT 
    p.product_name,
    c.category_name,
    p.list_price
FROM production.products AS p
INNER JOIN production.categories AS c
    ON p.category_id = c.category_id;

select top 5
    s.store_id,
    p.product_name,
    s.quantity
from production.products as p
inner join production.stocks as s
on p.product_id = s.product_id
where s.store_id in (3)
order by s.store_id  desc;


SELECT
    o.order_id,
    o.order_date,
    s.store_name,
    s.city
FROM sales.orders AS o
INNER JOIN sales.stores AS s
    ON o.store_id = s.store_id
WHERE o.order_id IN (1, 2, 3,5);


SELECT
    *
FROM production.products AS p
LEFT JOIN sales.order_items AS oi
    ON p.product_id = oi.product_id
WHERE oi.order_id IS not NULL
order by oi.order_id desc;


select 
    (s.first_name + ' ' + s.last_name) as full_name,
    so.order_id,
    so.staff_id,
    so.customer_id,
    so.order_date
    from sales.orders as so
left join sales.staffs as s
on so.staff_id = s.staff_id
where order_status is not null
order by order_date desc;


select 
   s.staff_id,
   (s.first_name + ' ' + s.last_name) as full_name,
   st.store_id,
   s.email
from sales.staffs as s
inner join sales.stores as st
on s.store_id = st.store_id
order by staff_id desc;

---- Q No: 1----
select 
    p.product_id,
    p.product_name,
    b.brand_name
from production.products as p
inner join production.brands as b
on p.brand_id = b.brand_id;


---- Q No: 2-----
select
   (s.first_name + ' ' + s.last_name) as full_name,
    s.staff_id,
    st.store_id,
    s.active
from  sales.stores as st
left join sales.staffs as s
on st.store_id = s.store_id
where s.active is null;


-- Q NO: 03 --

SELECT p.product_name, s.quantity
FROM production.products AS p
LEFT JOIN production.stocks AS s
    ON p.product_id = s.product_id AND s.quantity < 5 AND s.store_id = 1
   where quantity is not null;

   -- full outer join
   SELECT
    p.product_name,
    s.quantity
FROM production.products AS p
FULL OUTER JOIN production.stocks AS s
    ON p.product_id = s.product_id AND s.store_id = 1
    where  s.quantity is not null AND p.product_name is not null
    order by s.quantity desc;

select * from production.products
cross join production.stocks
where quantity = 0
order by store_id ASC , brand_id DESC;

SELECT s.store_name, c.category_name
FROM production.stores s
CROSS JOIN production.categories c;

SELECT b.brand_name, cat.category_name
FROM production.brands b
CROSS JOIN production.categories cat;

--------------------------------- Q NO: 04-----------------------------------
--Write a self join on sales.staffs that lists every manager along with 
--a count placeholder column showing 1 for each employee they manage 
--(you will replace this with a real COUNT in Chapter 6); 
--for now, just produce one row per employee-manager pair.
--------------------------------------------------------------------

SELECT 
    m.staff_id AS manager_id,
    m.first_name + ' ' + m.last_name AS manager_name,
    e.staff_id AS employee_id,
    e.first_name + ' ' + e.last_name AS employee_name,
    1 AS placeholder_count
FROM sales.staffs e
JOIN sales.staffs m 
    ON e.manager_id = m.staff_id;


select * from sales.staffs;

