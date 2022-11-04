/* Add CreatedDate and ModifiedDate columns. */
ALTER TABLE StoreInfo 
ADD CreatedDate DATETIME NOT NULL DEFAULT (GETUTCDATE()),
    ModifiedDate DATETIME NOT NULL DEFAULT(GETUTCDATE());

/* Create trigger that will update ModifedDate every time when StoreInfo table has been updated. */
CREATE TRIGGER StoreInfoModifiedDate
ON StoreInfo
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE StoreInfo
    SET ModifiedDate = GETUTCDATE()
    FROM StoreInfo s
    INNER JOIN inserted i
    ON s.StoreKey = i.StoreKey
END;


/* Update StoreType column. */
UPDATE StoreInfo
SET StoreType = 'Online'
WHERE StoreKey = 400;





