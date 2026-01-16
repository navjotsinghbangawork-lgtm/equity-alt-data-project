-- Step 1: Create monthly stock prices

DROP TABLE IF EXISTS monthly_prices;

CREATE TABLE monthly_prices AS
SELECT
    strftime('%Y-%m-01', Date) AS month,
    AVG(AAPL) AS aapl_price,
    AVG(MSFT) AS msft_price,
    AVG(SPY)  AS spy_price
FROM raw_prices
GROUP BY strftime('%Y-%m', Date);
-- Step 2: Calculate monthly returns

DROP TABLE IF EXISTS monthly_returns;

CREATE TABLE monthly_returns AS
SELECT
    month,
    (aapl_price - LAG(aapl_price) OVER (ORDER BY month)) / LAG(aapl_price) OVER (ORDER BY month) AS aapl_return,
    (msft_price - LAG(msft_price) OVER (ORDER BY month)) / LAG(msft_price) OVER (ORDER BY month) AS msft_return,
    (spy_price  - LAG(spy_price)  OVER (ORDER BY month)) / LAG(spy_price)  OVER (ORDER BY month) AS spy_return
FROM monthly_prices;

-- Step 3: Monthly macro data with forward fill

DROP TABLE IF EXISTS monthly_macro;

CREATE TABLE monthly_macro AS
SELECT
    strftime('%Y-%m-01', date) AS month,
    MAX(cpi) AS cpi,
    MAX(unemployment) AS unemployment,
    MAX(interest_rate) AS interest_rate,
    AVG(vix) AS vix
FROM raw_macro
GROUP BY strftime('%Y-%m', date);

-- Step 4: Final feature table

DROP TABLE IF EXISTS final_dataset;

CREATE TABLE final_dataset AS
SELECT
    r.month,
    r.aapl_return,
    r.msft_return,
    r.spy_return,
    m.cpi,
    m.unemployment,
    m.interest_rate,
    m.vix
FROM monthly_returns r
LEFT JOIN monthly_macro m
ON r.month = m.month;

