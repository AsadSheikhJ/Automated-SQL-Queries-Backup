import os
import pymssql
from datetime import datetime, timedelta, timezone
from git import Repo
from git.exc import GitCommandError

# Libraries for Local SQL Server Connection
import urllib
from sqlalchemy import create_engine, text

# For GitHub Codespace -------------------------------------------------
# from dotenv import load_dotenv
# # Load environment variables from .env file
# load_dotenv()

# Load environment variables
db_server = os.getenv('DB_SERVER')  
db_name = os.getenv('DB_NAME') 
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
github_token = os.getenv('GITHUB_TOKEN')

# Checking if it's github Environment or Local Environment
environ_Git = 'GITHUB_USER' in os.environ

# Separate Funtion to execute query For Any Environment Connection
def executeQuery(db_server, db_name, db_user, db_pw, query, connection = None):

    try:
        if not environ_Git:
            params = urllib.parse.quote_plus(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_server};DATABASE={db_name};trusted_connection=yes"
            )
            con_string = f"mssql+pyodbc:///?odbc_connect={params}"
            engine = create_engine(con_string, fast_executemany=True)
            connection = engine.connect()
            print("Connected Successfully!") # Connection established Check!

            result = connection.execute(text(query))
            getResult = result.fetchall()
        else:
            connection = pymssql.connect(server=db_server, user=db_user, password=db_pw, database=db_name)
            print("Connected Successfully!")

            cursor = connection.cursor()
            cursor.execute(query)
            getResult = cursor.fetchall()

        print("Query results successfully fetched...")
        return getResult

    except Exception as e:
        print(f"Error Occured: {e}")
        return None

    finally:
        if connection:
            connection.close()

# Function for Procedures and Views
def getProceduresAndViews(db_server, db_name, user, pw):

    # List of procedures and views to back up
    proc_names = ['procedure_1', 'procedure_2'] # List procedures
    view_names = ['customer_view']  # List view
    names = proc_names + view_names
    list = ', '.join([f"'{name}'" for name in names])

    sql_query = f"""
    SELECT name, OBJECT_DEFINITION(object_id) as definition 
    FROM sys.objects 
    WHERE name IN ({list}) AND type IN ('P', 'V')
    """

    return executeQuery(db_server, db_name, user, pw, sql_query)

# Function to save procedures and views to files
def changesToFile(changedQueries, outputDirectory):

    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    for query in changedQueries:
        queryName = query[0]
        queryDefinition = query[1]

        # Define file paths
        queryFilePath = os.path.join(outputDirectory, f"{queryName}.sql")

        # Write the current object to a file with UTF-16 encoding and BOM
        with open(queryFilePath, 'w', encoding='utf-16') as f:
            f.write('\ufeff' + queryDefinition)

# Function to commit changes to local Git repo
def commiChangeToRepo(repositoryPath):

    repo = Repo(repositoryPath)
    repo.git.add(A=True)  # Add all changes

    # Check for changes
    if repo.is_dirty(untracked_files=True):
        get_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_message = f"Automaticaly updated on {get_time}"
        try:
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            origin.push()  # Push changes to remote repo
        except Exception as e:
            print(f"Error pushing changes to Git: {e}")

        return True    
    else:
        print("No changes to Found..")
        return False


repositoryPath = os.getcwd()  # Use the current directory as the repo path
files = getProceduresAndViews(db_server, db_name, db_user, db_password)
commitStatus = False

if files:
    fileLocationFolder = os.path.join(repositoryPath, "procedures")
    changesToFile(files, fileLocationFolder)
    commitStatus = commiChangeToRepo(repositoryPath)
    if commitStatus:
        print("Changes committed successfully!")
    else:
        print("Great Day! No Changes to commit.")
else:
    print("No procedures or views retrieved or failed to retrieve them.")
