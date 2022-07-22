SELECT menu_date, SUM(delta) AS delta
FROM   dbo.[price-delta-between-years-view]
GROUP BY menu_date