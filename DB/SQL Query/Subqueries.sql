/* Using Subqueries to get AVG Unit Price and AVG Unit Price for all rows where UnitPrice is bigger than AVG UnitPrice*/
SELECT 
SalesKey,
UnitPrice,
AvgUnitPrice = (SELECT AVG(UnitPrice) FROM FactSales),
AvgUnitPriceDiff = UnitPrice - (SELECT AVG(UnitPrice) FROM FactSales)
FROM FactSales
WHERE UnitPrice > (SELECT AVG(UnitPrice) FROM FactSales);

/* Correlated Subquerie to get all Stores with quantity order bigger than 100. */
SELECT 
st.StoreName,
BigQuantityOrders = 
(
    SELECT COUNT(*) FROM FactSales AS s
    WHERE s.StoreKey = st.StoreKey
    AND s.SalesQuantity > 100
)
FROM DimStore st
ORDER BY st.StoreName;


/* Get all stores where there is a product with UnitPrice bigger than 1000. */
SELECT 
st.StoreName,
st.SellingAreaSize
FROM DimStore st
WHERE EXISTS(
    SELECT 1
    FROM FactSales s
    WHERE s.UnitPrice > 1000
    AND st.StoreKey = s.StoreKey
)
ORDER BY st.SellingAreaSize DESC;


/* Pivot table by Category and SubCategory with Total SalesAmount. */
SELECT
*
FROM
(
    SELECT 
    ProductCategory = pc.ProductCategoryName,
    ProductSubcategory = ps.ProductSubcategoryName,
    s.SalesAmount
    FROM DimProductCategory pc
    LEFT JOIN DimProductSubcategory ps
    ON pc.ProductCategoryKey = ps.ProductCategoryKey
    LEFT JOIN DimProduct p
    ON ps.ProductSubcategoryKey = p.ProductSubcategoryKey
    LEFT JOIN FactSales s
    ON s.ProductKey = p.ProductKey
) A
PIVOT(
    SUM(SalesAmount)
    FOR ProductCategory IN([Audio], [Computers])
) B
ORDER BY 1



