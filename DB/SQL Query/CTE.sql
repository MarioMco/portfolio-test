/* CTE for Top 10 Sales by Year-Month */
WITH Sales AS
(
SELECT
    DateKey,
    SalesAmount,
    SalesMonth = DATEFROMPARTS(YEAR(DateKey), MONTH(DateKey), 1),
    OrderRank = ROW_NUMBER() OVER(PARTITION BY DATEFROMPARTS(YEAR(DateKey), MONTH(DateKey), 1) ORDER BY SalesAmount DESC)
FROM FactSales
),

Top10 AS (
SELECT
    SalesMonth,
    Top10Total = SUM(SalesAmount)
FROM Sales
WHERE OrderRank <= 10
GROUP BY SalesMonth
)

SELECT
FORMAT(A.SalesMonth, 'yyyy-MM') AS 'Year-Month',
A.Top10Total,
PrevTop10Total = B.Top10Total
FROM Top10 AS A
LEFT JOIN Top10 AS B
ON A.SalesMonth = DATEADD(MONTH,1, B.SalesMonth)
ORDER BY A.SalesMonth;


/* Use Recursive CTE to get all employees and managers they are reporting to. */

WITH EmployeeCTE AS
(
    SELECT EmployeeKey, FirstName + ' ' + LastName as Employee, ParentEmployeeKey
    FROM DimEmployee
    WHERE EmployeeKey = 1

    UNION ALL

    SELECT e.EmployeeKey, e.FirstName + ' ' + e.LastName as Employee, e.ParentEmployeeKey
    FROM DimEmployee e
    JOIN EmployeeCTE c
    ON e.EmployeeKey = c.ParentEmployeeKey
)

SELECT e1.EmployeeKey, 
        e1.FirstName + ' ' + e1.LastName as Employee, 
        ISNULL(e3.FirstName + ' ' + e3.LastName, 'CEO') as Manager
FROM DimEmployee e1
LEFT JOIN EmployeeCTE e2
ON e1.EmployeeKey = e2.ParentEmployeeKey
LEFT JOIN DimEmployee e3
ON e1.ParentEmployeeKey = e3.EmployeeKey


