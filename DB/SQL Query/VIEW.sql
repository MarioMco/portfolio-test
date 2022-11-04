/* Create View for Total Sales by Store */
CREATE VIEW TotalSalesByStore

AS

SELECT
    st.StoreName,
    TotalSales = SUM(s.SalesAmount)
FROM DimStore st
INNER JOIN FactSales s
ON st.StoreKey = s.StoreKey
GROUP BY st.StoreName;

SELECT * FROM TotalSalesByStore;