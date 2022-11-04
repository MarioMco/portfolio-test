/* Create Variable to avoid repeating. */
DECLARE @AvgPrice MONEY
SET @AvgPrice = (SELECT AVG(UnitPrice) FROM FactSales)

SELECT
    DISTINCT(ProductKey),
    UnitPrice,
    AvgUnitPrice = @AvgPrice,
    AvgUnitPriceDiff = UnitPrice  - @AvgPrice
FROM FactSales
WHERE UnitPrice > @AvgPrice
ORDER BY ProductKey



/* Create Procedure that will return Top N rows of Total Sales Amount by ProductName*/
CREATE PROCEDURE dbo.SalesReport (@TopN INT)

AS

BEGIN
    SELECT
    *
    FROM
        (SELECT 
            p.ProductName,
            TotalSalesAmount = SUM(s.SalesAmount),
            TotalSalesAmountRank = DENSE_RANK() OVER(ORDER BY SUM(s.SalesAmount) DESC),
            TotalQuantity = SUM(s.SalesQuantity)
        FROM DimProduct p
        JOIN FactSales s
        ON p.ProductKey = s.ProductKey
        GROUP BY p.ProductName) X
    WHERE TotalSalesAmountRank < @TopN
    ORDER BY TotalSalesAmountRank
END


EXEC dbo.SalesReport 5





