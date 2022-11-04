/* Single row insert into StoreInfo table. */
INSERT INTO StoreInfo (StoreKey, StoreType, StoreName, StoreStatus)
VALUES (400, 'Online', 'New Contoso Store', 'On')

/* Multiple row insert into StoreInfo table. */
INSERT INTO StoreInfo (StoreKey, StoreType, StoreName, StoreStatus)
SELECT StoreKey, StoreType, StoreName, [Status] 
FROM DimStore


/* Multiple row insert into TotalSales table. */
INSERT INTO TotalSales(StoreKey, TotalCost, TotalSalesAmount)
SELECT
    StoreKey,
    TotalCostSum = SUM(TotalCost),
    TotalSalesAmount = SUM(SalesAmount)
FROM FactSales
GROUP BY StoreKey

/* Update StoreType in StoreInfo filtering by StoreKey.*/
UPDATE StoreInfo
SET StoreType = 'Store'
WHERE StoreKey = 400


/* Join StoreInfo and TotalSales tables. */
SELECT 
    si.StoreName, 
    ts.TotalCost, 
    ts.TotalSalesAmount 
FROM StoreInfo AS si
LEFT JOIN TotalSales AS ts
ON si.StoreKey = ts. StoreKey



