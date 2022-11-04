/* INNER JOIN of two tables will return only data that belongs in both tables. */
SELECT
    p.ProductKey,
    TotalSales = SUM(s.SalesAmount)
FROM DimProduct p
INNER JOIN FactSales s
ON p.ProductKey = s.ProductKey
GROUP BY p.ProductKey;


/* Multiple tables with LEFT JOIN. */
SELECT 
    pc.ProductCategoryName,
    ps.ProductSubcategoryName,
    p.ProductName,
    TotalSales = SUM(s.SalesAmount)
FROM DimProductCategory pc
LEFT JOIN DimProductSubcategory ps
ON pc.ProductCategoryKey = ps.ProductCategoryKey
LEFT JOIN DimProduct p
ON ps.ProductSubcategoryKey = p.ProductSubcategoryKey
LEFT JOIN FactSales s
ON s.ProductKey = p.ProductKey
GROUP BY pc.ProductCategoryName, ps.ProductSubcategoryName, p.ProductName;


/* UNION data from two tables. We use UNION ALL insted of UNION to import same data from 2 tables if exist. */
SELECT 
    StoreKey,
    ProductKey,
    SalesAmount
FROM FactOnlineSales

UNION ALL

SELECT 
    StoreKey,
    ProductKey,
    SalesAmount
FROM FactSales;


/*CROSS JOIN DimStore and ProductCategory will return all stores with possible product categories*/
SELECT 
    s.StoreKey,
    pc.ProductCategoryName
FROM DimProductCategory pc
CROSS JOIN DimStore s
ORDER BY s.StoreKey;







