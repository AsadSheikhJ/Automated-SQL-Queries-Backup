# Automated SQL Procedures and Views Backup Script

This script can automatically back up queries for procedures or views from a SQL Server database into a GitHub repository. The script connects to the database or local database, retrieves the queries for procedures and views, saves them as `.sql` files, and commits these files to the repository. This can be scheduled to run periodically using GitHub Actions. or it can be run locally

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AsadSheikhJ/Automated-SQL-Queries-Backup.git
cd your-repository
```
### 2. Set Up Environment Variables (This is only if you are running Locally)

Create a `.env` file in the root directory of the project with the following content:

```env
DB_SERVER=your_server_name_or_ip
DB_NAME=your_database_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
```

- `DB_SERVER`: The server name or IP address of your SQL Server instance.
- `DB_NAME`: The name of the database from which to back up procedures and views.
- `DB_USER`: The username to connect to the database.
- `DB_PASSWORD`: The password to connect to the database.

### 3. Modify the Python Script (If Needed)

The script is already configured to run either locally or in GitHub Actions. However, if you need to adjust the list of stored procedures and views, you can modify the `procedure_names` and `view_names` variables in the `get_procedures_and_views` function.

### 4. Create a Dummy View (Optional)

If you're testing locally and don’t have existing views, you can create a simple view using the following SQL command:

```sql
CREATE TABLE dbo.Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Department NVARCHAR(50),
    HireDate DATE
);

-- some dummy data
INSERT INTO dbo.Employees (EmployeeID, FirstName, LastName, Department, HireDate)
VALUES 
(1, 'John', 'Doe', 'Engineering', '2020-01-15'),
(2, 'Jane', 'Smith', 'Marketing', '2019-07-30'),
(3, 'Sam', 'Wilson', 'Sales', '2021-03-22')

CREATE VIEW dbo.temp_mnh_01_qr AS
SELECT 
    EmployeeID,
    FirstName,
    LastName,
    Department,
    HireDate
FROM 
    dbo.Employees;
```

### 5. Run the Script

You can run the script manually by executing:

```bash
python automated_procedures_backup.py
```

This will connect to the database, back up the stored procedures and views, and commit them to the repository.

## Automating with GitHub Actions

### 1. Configure GitHub Actions

The repository includes a `.github/workflows/update_query_files.yml` file that defines the workflow for GitHub Actions. 

### 2. Set Up Secrets in GitHub

Go to your repository on GitHub and navigate to `Settings > Secrets and variables > Actions`. Add the following secrets:

- `DB_SERVER`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `GITHUB_TOKEN` (No Need to setup this since it get's pick automatically from the environment)

These secrets will be used by GitHub Actions to run the script.

### 3. Run the Workflow Manually (For Testing)

To manually trigger the workflow, go to the `Actions` tab in your repository, select the workflow, and click `Run workflow`.

### 4. Grant Workflow the Permission

The workflow requires permission to read and write permission on repository. so you need to go to `Settings > Actions > General > Workflow permissions`. There select the "Read and write permissions" and save. This will allow workflow to automatically save changes in the repository.

## Troubleshooting

- **Error (Server denied):**: This may occur if the connection to the database fails. Ensure your connection string is correct and that your database is running.

- **Git push errors**: Ensure that your GitHub token has the necessary permissions to push to the repository.

## Contributing

Feel free to submit issues or pull requests to contribute to this project.
