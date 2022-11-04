/* Create Calendar Table */
CREATE TABLE ContosoRetailDW.dbo.Calendar (
    DateValue DATE,
    DayOfWeekNumber INT,
    DayOfWeekName VARCHAR(32),
    DayOfMonthNumber INT,
    MonthNumber INT,
    YearNumber INT,
    WeekendFlag TINYINT,
    HolidayFlag TINYINT
);

/* Insert data into between Start and End date into Calendar table */
WITH Dates AS
(
        SELECT 
            CAST('2007-01-01' AS DATE) AS MyDate

    UNION ALL

    SELECT
    DATEADD(DAY, 1, MyDate)
    FROM Dates
    WHERE MyDate < CAST('2009-12-31' AS DATE)
)


INSERT INTO ContosoRetailDW.dbo.Calendar (
    DateValue
)
SELECT
MyDate
FROM
Dates
OPTION (MAXRECURSION 10000)



/* Update NULL with relevant values. */
UPDATE ContosoRetailDW.dbo.Calendar
SET
    DayOfWeekNumber = DATEPART(WEEKDAY, DateValue),
    DayOfWeekName = FORMAT(DateValue, 'dddd'),
    DayOfMonthNumber = DAY(DateValue),
    MonthNumber = MONTH(DateValue),
    YearNumber = YEAR(DateValue)

UPDATE ContosoRetailDW.dbo.Calendar
SET WeekendFlag = 
    CASE
        WHEN DayOfWeekName IN ('Saturday', 'Sunday') THEN 1
        ELSE 0
    END

