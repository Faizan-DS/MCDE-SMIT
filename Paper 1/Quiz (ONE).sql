use
BikeStores
GO



--Task 1 — Build the Sales Detail Dataset 
SELECT
    o.order_id,
    o.order_date,
    c.first_name+ ' '+ c.last_name AS customer_full_name,
    s.store_name,
    st.first_name+ ' '+ st.last_name AS staff_full_name,
    p.product_name,
    ct.category_name,
    b.brand_name,
    oi.quantity,
    oi.list_price,
    oi.discount,
    oi.quantity * oi.list_price * (1 - oi.discount)
        AS netLineRevenue
FROM sales.orders AS o
INNER JOIN sales.order_items AS oi
    ON o.order_id = oi.order_id
INNER JOIN sales.customers AS c
    ON o.customer_id = c.customer_id
INNER JOIN sales.stores as s
    ON o.store_id = s.store_id
INNER JOIN sales.staffs AS st
    on o.staff_id = st.staff_id
INNER JOIN production.products AS p
    ON oi.product_id = p.product_id
INNER JOIN production.categories AS ct
    ON p.category_id = ct.category_id
INNER JOIN production.brands AS b
    ON p.brand_id = b.brand_id
WHERE o.order_status = 4
ORDER BY o.order_date DESC, o.order_id DESC;



--Task 2 — Store Performance Summary 
SELECT
    s.store_name,
    COUNT(DISTINCT o.order_id) AS distinct_orders,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.quantity * oi.list_price * (1 - oi.discount))
        AS total_net_revenue,
    SUM(oi.quantity * oi.list_price * (1 - oi.discount)) / COUNT(Distinct o.order_id)
        AS average_order_value
FROM sales.stores AS s
LEFT JOIN sales.orders AS o
    ON s.store_id = o.store_id
    AND o.order_status = 4
LEFT JOIN sales.order_items AS oi
    ON o.order_id = oi.order_id
GROUP BY s.store_id, s.store_name
ORDER BY total_net_revenue DESC;


--Task 3 — High-Value Customers 

WITH CustomerSpending AS
(
    SELECT
        c.customer_id,
        c.first_name+ ' '+ c.last_name AS customer_name,
        COUNT(DISTINCT o.order_id) AS completed_order_count,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_spending
    FROM sales.customers AS c
    INNER JOIN sales.orders AS o
        ON c.customer_id = o.customer_id
    INNER JOIN sales.order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 4
    GROUP BY
        c.customer_id, c.first_name, c.last_name
)
SELECT
    customer_id,
    customer_name,
    completed_order_count,
    total_spending
FROM CustomerSpending
WHERE total_spending >
(
    SELECT AVG(total_spending)
    FROM CustomerSpending
)
ORDER BY total_spending DESC;


--Task 4 — Inventory Risk Report 

SELECT
    p.product_name,
    s.store_name,
    st.quantity AS current_quantity,
    c.category_name,
    b.brand_name
FROM production.stocks AS st
INNER JOIN production.products AS p
    ON st.product_id = p.product_id
INNER JOIN sales.stores AS s
    ON st.store_id = s.store_id
INNER JOIN production.categories AS c
    ON p.category_id = c.category_id
INNER JOIN production.brands AS b
    ON p.brand_id = b.brand_id
WHERE st.quantity < 5
order by st.quantity ASC;

--Task 5 — Top Products Within Each Category

WITH product_information as(
SELECT
      c.category_name,
      p.product_id,
      p.product_name,
      SUM(oi.quantity) AS total_units_sold,
      SUM(oi.quantity * oi.list_price * (1 - oi.discount))  as total_net_revenue
    FROM sales.orders AS o
    INNER JOIN sales.order_items AS oi
        ON o.order_id = oi.order_id
    INNER JOIN production.products AS p
        ON oi.product_id = p.product_id
    INNER JOIN production.categories AS c
        ON p.category_id = c.category_id
    WHERE o.order_status = 4
    GROUP BY c.category_name, p.product_id, p.product_name),
ranked AS(
SELECT  
        DENSE_RANK() OVER(
        PARTITION BY category_name 
        ORDER BY total_units_sold DESC
        ) as Ranking,
        category_name,
        product_name,
        total_units_sold,
        total_net_revenue
        FROM product_information) 

SELECT TOP 3 * FROM ranked;


--Task 6 — Monthly Sales Trend 

WITH MonthlySales AS
(
    SELECT
        YEAR(o.order_date) AS sales_year,
        MONTH(o.order_date) AS sales_month,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount))
            AS total_net_revenue
    FROM sales.orders AS o
    INNER JOIN sales.order_items as oi
        ON o.order_id = oi.order_id
    where o.order_status = 4
    GROUP BY
        YEAR(o.order_date),
        MONTH(o.order_date)
),
SalesWithPrevious AS
(
    SELECT
        sales_year,
        sales_month,
        total_net_revenue,
        LAG(total_net_revenue) OVER
        (
            ORDER BY sales_year, sales_month
        ) AS previous_month_revenue
    FROM MonthlySales
)
SELECT
    sales_year,
    sales_month,
    total_net_revenue,
    previous_month_revenue,
    total_net_revenue - previous_month_revenue
        AS revenue_change
FROM SalesWithPrevious
ORDER BY sales_year, total_net_revenue;


--Task 7 — Reusable Reporting View --
CREATE OR ALTER VIEW sales.vw_customer_sales_summary
AS
SELECT
    c.customer_id,
    c.first_name+ ' '+ c.last_name AS customer_full_name,
    COUNT(DISTINCT o.order_id) AS completed_order_count,
    COALESCE(SUM(oi.quantity), 0) AS total_units_purchased,
    COALESCE(
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)),
        0
    ) AS total_net_revenue,
    MAX(o.order_date) AS recent_completed_order_date
FROM sales.customers AS c
LEFT JOIN sales.orders AS o
    ON c.customer_id = o.customer_id
    AND o.order_status = 4
LEFT JOIN sales.order_items AS oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name;
GO



select * from sales.vw_customer_sales_summary;


--Task 8 — Safe Data Modification---
BEGIN TRANSACTION;

UPDATE sales.customers
SET phone = '(999) 555-0101'
WHERE customer_id = 1;

SELECT
    customer_id,
    first_name,
    last_name,
    phone
FROM sales.customers
WHERE customer_id = 1;
ROLLBACK TRANSACTION;


-- TASK 9 — STORE SALES PROCEDURE 
CREATE PROCEDURE sales.usp_store_sales_report
    @store_id INT,
    @start_date DATE,
    @end_date DATE
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        IF @start_date > @end_date
        BEGIN
            THROW 50001,
                'Invalid date range: start date must not be later than end date.',
                1;
        END;

        SELECT
            p.product_name,
            SUM(oi.quantity) AS total_units_sold,
            SUM(oi.quantity * oi.list_price * (1 - oi.discount))
                AS total_net_revenue
        FROM sales.orders AS o
        INNER JOIN sales.order_items AS oi
            ON o.order_id = oi.order_id
        INNER JOIN production.products AS p
            ON oi.product_id = p.product_id
        WHERE
            o.store_id = @store_id
            AND o.order_status = 4
            AND o.order_date >= @start_date
            AND o.order_date < DATEADD(DAY, 1, @end_date)
        GROUP BY
            p.product_id,
            p.product_name
        ORDER BY
            total_net_revenue DESC,
            p.product_name ASC;
    END TRY
    BEGIN CATCH
        SELECT
            ERROR_NUMBER() AS error_number,
            ERROR_MESSAGE() AS error_message,
            ERROR_LINE() AS error_line;
    END CATCH;
END;
GO

EXEC sales.usp_store_sales_report
    @store_id = 1,
    @start_date = '2015-01-01',
    @end_date = '2016-12-31';

-- TASK 10 — MANAGEMENT INSIGHT QUERY (3 MARKS)

SELECT
    s.store_name,
    c.category_name,
    COUNT(DISTINCT o.order_id) AS completed_orders,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.quantity * oi.list_price * (1 - oi.discount))
        AS total_net_revenue
FROM sales.stores AS s
INNER JOIN sales.orders AS o
    ON s.store_id = o.store_id
INNER JOIN sales.order_items AS oi
    ON o.order_id = oi.order_id
INNER JOIN production.products AS p
    ON oi.product_id = p.product_id
INNER JOIN production.categories AS c
    ON p.category_id = c.category_id
WHERE o.order_status = 4
GROUP BY s.store_id, s.store_name, c.category_id, c.category_name
ORDER BY
    total_net_revenue DESC;
