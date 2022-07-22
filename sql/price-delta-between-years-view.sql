SELECT
    [dish_id],
    [dish_name],
    [menu_date],
    [average_price],
    (LAG(average_price, 1, [average_price]) OVER (PARTITION BY dish_id ORDER BY menu_date) - average_price) AS delta
FROM [nypl-menu].[dbo].[dishes-to-menu-items-by-year-view]