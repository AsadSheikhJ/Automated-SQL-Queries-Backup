




CREATE VIEW [dbo].[customer_view] AS
SELECT 
    EmployeeID,
	CONCAT(FirstName,' ',LastName) as 'Full Name'
	,'TestColumn' as 'AddedColumn',
    Department,
    HireDate
FROM 
    dbo.Employees;
