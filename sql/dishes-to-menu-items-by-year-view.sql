SELECT dbo.Dish.id AS dish_id, dbo.Dish.name AS dish_name, YEAR(dbo.Menu.date) AS menu_date, ROUND(AVG(dbo.MenuItem.price), 2) AS average_price, ROUND(STDEV(dbo.MenuItem.price), 2) AS stdv_price
FROM   dbo.Dish INNER JOIN
             dbo.MenuItem ON dbo.Dish.id = dbo.MenuItem.dish_id INNER JOIN
             dbo.MenuPage ON dbo.MenuItem.menu_page_id = dbo.MenuPage.id INNER JOIN
             dbo.Menu ON dbo.MenuPage.menu_id = dbo.Menu.id
WHERE (dbo.MenuItem.price IS NOT NULL) AND (dbo.Menu.date IS NOT NULL) AND (dbo.Dish.menus_appeared > 5)
GROUP BY dbo.Dish.id, dbo.Dish.name, YEAR(dbo.Menu.date)
HAVING (COUNT(dbo.MenuItem.dish_id) > 2) AND (STDEV(dbo.MenuItem.price) < AVG(dbo.MenuItem.price))