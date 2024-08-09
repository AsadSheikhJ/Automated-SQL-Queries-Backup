



CREATE VIEW [dbo].[customer_view] AS
SELECT 
    EmployeeID,
	CONCAT(FirstName,' ',LastName) as 'Full Name',
    Department,
    HireDate
FROM 
    dbo.Employees;
