# capstone-project-3900-h12a-all4stonks
capstone-project-3900-h12a-all4stonks created by GitHub Classroom

# USER MANUAL
# How to Install Watchdog (from Linux Image)
1. Python 3.8 pre installed, double check and install if required
2. Download and unzip from github repo (This unzipped folder contains the [Project Root])
 
# Install Required deb Files
3. sudo apt install python3-pip
4. sudo apt python3-flask
5. sudo apt-get install mysql-client
6. sudo apt-get install libmysqlclient-dev
7. sudo apt update
8. sudo apt install mysql-server
 
# Check if MySQL is running, Should Show MySQL loaded
9. sudo systemctl status mysql

# Install Python Libraries using pip
10. pip install -r /path/to/[Project Root]/requirements.txt  

# Use sudo to Access MySQL and Remove the Password
# Also, Create the Watchdog Database.
11. sudo mysql
12. ALTER USER ‘root’@‘localhost’ IDENTIFIED WITH caching_sha2_password BY ‘’;
13. create database watchdog;
14. exit;

# Set up and Configure the Watchdog Database
15. mysql -u root watchdog < /path/to/[Project Root]/Backend/database/schema.sql
 
# Download file from https://dev.mysql.com/downloads/workbench/
# Download the file suitable for your OS:
# mysql-workbench-community_8.0.27-1ubuntu20.04_amd64.deb (Recommended for Linux image)

# Assuming it is in ~/Downloads:
16. sudo apt --fix-broken install ~/Downloads/[downloaded_deb_file]

# Import Stocks into the Database
17. Once installed, go to Applications and launch MySQL Workbench
 
18. Double click the watchdog instance
19. Go to the watchdog database/schema
20. Right click stocks table in MySQL
21. Select 'Table Data Import Wizard'
22. Find stock_database.csv in Backend/database/
23. Use Existing Table (watchdog.stocks)
24. Select all source columns, encoding utf-8 is fine
25. NASDAQ:A->ID, A -> stock_code, Agilent... -> NAME
26. Click next to import
27. Click next once completed to finish. (Takes 30-90sec)
28. 9980 Rows Imported!

# Run Flask
28. Go to [Project Root]/Backend directory
29. flask run

# You May Now Access the App Through Browser
# e.g. Using localhost:5000/home

Please feel free to contact if you have any issues =)



# Classes
User

Portfolio 

Stock 

Watch List

Home Page

# APIs

ASX

Homepage

NASDAQ

Portfolios

User

Watch List

Search Results





