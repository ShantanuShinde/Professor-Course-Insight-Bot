# Professor-Course-Insight-Bot

## Loading database into MySQL

With MySQL installed in your machine, run the following command to load `insight_database.sql` into your MySQL server.
> Get-Content .\resources\insight_database.sql | mysql -u root -p insight_database

To save updated database into the file, run the following command
> mysqldump -u root -p insight_database > insight_database.sql

## Running the Chatbot Server
1. Go to the back_end directory.
2. Install the required libraries using:
> pip install -r requirements.txt
3. Run the  `chatbot_api_server.py` file as 
> python chatbot_api_server.py

## Running the frontend server
1. Go to the front_end directory
2. Make sure you have nodejs installed.
3. Install nextjs and react using:
> npm install next react react-dom
4. Run the nodejs server using:
> npm run dev
5. The frontend should open up at the mentioned link in the output.

[Demo Video](https://www.youtube.com/watch?v=E-0W8S8kJyA&t=5s)