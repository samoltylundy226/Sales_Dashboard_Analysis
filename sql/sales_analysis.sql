-- =============================================================================
-- Project: Sales Dashboard Analysis
-- Script: sql/sales_analysis.sql
-- Author: Team Member 2 (Data Analysis)
-- Purpose: Analytical SQL queries to extract business metrics, trends, and KPIs
-- =============================================================================

/*
DESCRIPTION & USAGE INSTRUCTIONS:
---------------------------------
This file organizes the core business queries that answer key analytical questions
for the Sales Dashboard. Once the cleaned dataset from `data/processed/` is loaded
into our SQL database (e.g., PostgreSQL, SQLite, BigQuery, or MySQL), these queries
will provide:
  1. Executive KPI Summary (Total Revenue, Total Profit, Profit Margin, Total Orders)
  2. Temporal Sales Performance (Monthly trends, Year-over-Year / Month-over-Month growth)
  3. Product & Category Contribution (Pareto 80/20 analysis, Top & Bottom performers)
  4. Regional & Geographic Distribution (Sales by Region/State/City)
  5. Customer Behavior & Order Distribution (Average Order Value, Purchase Frequency)

NOTE:
Table names (`sales_data`) and column names (`order_date`, `sales_amount`, `profit`,
`category`, `customer_id`, etc.) are representative standards. They will be adjusted
to match the final schema selected during Day 2.
*/


-- -----------------------------------------------------------------------------
-- 1. Executive Summary KPIs
-- -----------------------------------------------------------------------------
-- Calculates high-level aggregate metrics for the executive dashboard overview.

SELECT
    COUNT(DISTINCT order_id)                AS total_orders,
    COUNT(DISTINCT customer_id)             AS total_customers,
    ROUND(SUM(sales_amount), 2)             AS total_revenue,
    ROUND(SUM(profit), 2)                   AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales_amount), 0)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(sales_amount), 2)             AS average_order_value
FROM sales_data;


-- -----------------------------------------------------------------------------
-- 2. Monthly Revenue Trend and Month-over-Month (MoM) Growth
-- -----------------------------------------------------------------------------
-- Analyzes sales momentum across time using Common Table Expressions (CTE)
-- and LAG window functions.

WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date)     AS sales_month,
        ROUND(SUM(sales_amount), 2)         AS monthly_revenue,
        ROUND(SUM(profit), 2)               AS monthly_profit,
        COUNT(DISTINCT order_id)            AS order_volume
    FROM sales_data
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    sales_month,
    monthly_revenue,
    monthly_profit,
    order_volume,
    LAG(monthly_revenue) OVER (ORDER BY sales_month) AS prior_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY sales_month))
        / NULLIF(LAG(monthly_revenue) OVER (ORDER BY sales_month), 0) * 100,
        2
    ) AS mom_revenue_growth_pct
FROM monthly_sales
ORDER BY sales_month;


-- -----------------------------------------------------------------------------
-- 3. Top Performing Product Categories & Sub-Categories
-- -----------------------------------------------------------------------------
-- Evaluates category revenue generation and profitability to detect loss leaders.

SELECT
    category,
    sub_category,
    ROUND(SUM(sales_amount), 2)             AS total_revenue,
    ROUND(SUM(profit), 2)                   AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales_amount), 0)) * 100, 2) AS profit_margin_pct,
    DENSE_RANK() OVER (ORDER BY SUM(sales_amount) DESC) AS revenue_rank
FROM sales_data
GROUP BY category, sub_category
ORDER BY total_revenue DESC;


-- -----------------------------------------------------------------------------
-- 4. Regional Performance Breakdown
-- -----------------------------------------------------------------------------
-- Compares sales volume, revenue, and average order value across geographical regions.

SELECT
    region,
    country_or_state,
    COUNT(DISTINCT order_id)                AS total_orders,
    ROUND(SUM(sales_amount), 2)             AS total_revenue,
    ROUND(SUM(profit), 2)                   AS total_profit,
    ROUND(AVG(sales_amount), 2)             AS avg_ticket_size
FROM sales_data
GROUP BY region, country_or_state
ORDER BY total_revenue DESC;


-- -----------------------------------------------------------------------------
-- 5. Customer Segmentation / Top Customer Contribution (Pareto Analysis)
-- -----------------------------------------------------------------------------
-- Identifies VIP customers driving the majority of sales volume.

SELECT
    customer_id,
    customer_name,
    COUNT(DISTINCT order_id)                AS total_purchases,
    ROUND(SUM(sales_amount), 2)             AS lifetime_spend,
    ROUND(SUM(profit), 2)                   AS lifetime_profit,
    ROUND(AVG(sales_amount), 2)             AS avg_order_value
FROM sales_data
GROUP BY customer_id, customer_name
ORDER BY lifetime_spend DESC
LIMIT 20;
