/*Select all data from the DimStore table.*/
SELECT *
FROM DimStore;

/*Get all stores from the DimStore table whose StoreType is "Reseller".*/
SELECT * FROM DimStore
WHERE StoreType LIKE 'Reseller';


/*Get all stores from the DimStore table whose StoreType is "Reseller" and ZipCode is 56535.*/
SELECT * FROM DimStore
WHERE StoreType LIKE 'Reseller'
AND ZipCode = 56535;

/*Get all stores from the DimStore table whose StoreType is either "Reseller" or "Online".*/
SELECT * FROM DimStore
WHERE StoreType IN ('Reseller', 'Online');


/*Get all stores from the DimStore table whose StoreType is not  "Reseller" or "Online".*/
SELECT * FROM DimStore
WHERE StoreType NOT IN ('Reseller', 'Online');


/*Get all stores from the DimStore table whose StoreType is "Reseller" and StoreManager is 35 or 233.*/

SELECT * FROM DimStore
WHERE StoreType = 'Reseller'
AND (StoreManager = 35 OR StoreManager = 233);

/*Get all stores from the DimStore table whose StoreName starts with "Contoso Seattle" and then followed by any character after.*/
SELECT * FROM DimStore
WHERE StoreName LIKE 'Contoso Seattle%';


/*Get all stores from the DimStore table whose StoreName starts with any character before "Seattle" and then followed by any character after.*/
SELECT * FROM DimStore
WHERE StoreName LIKE '%Seattle%';


/*Get all stores from the DimStore table whose OpenDate was in year 2004 and month 03.*/
SELECT * FROM DimStore
WHERE YEAR(OpenDate) = 2004
AND MONTH(OpenDate) = 3;


/*Get all stores from the DimStore table whose StoreKey is between 135 and 150.*/
SELECT * FROM DimStore
WHERE StoreKey BETWEEN 135 AND 150;


/*Get all stores from the DimStore table whose SellingAreaSize is bigger than 1000.*/
SELECT * FROM DimStore
WHERE SellingAreaSize > 1000;


/*Get an unique list of StoreType from DimStore table. */
SELECT DISTINCT StoreType
FROM DimStore;


/*Number of Stores in DimStore table. */
SELECT COUNT(*)
FROM DimStore;

/*Number of Stores grouped by StoreType in DimStore table. */
SELECT 
StoreTypeNo = COUNT(*)
FROM DimStore
GROUP BY StoreType;

/*Get 10 biggest stores by SellingAreaSize from DimStore table. */
SELECT TOP 10 *
FROM DimStore
ORDER BY SellingAreaSize DESC;

/*Get all stores from DimStore table whose CloseDate is not null. */
SELECT * 
FROM DimStore
WHERE CloseDate IS NOT NULL;







