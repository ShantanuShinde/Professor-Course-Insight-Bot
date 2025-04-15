# Professor-Course-Insight-Bot

## Loading database into MySQL

With MySQL installed in your machine, run the following command to load `insight_database.sql` into your MySQL server.
> Get-Content .\resources\insight_database.sql | mysql -u root -p insight_database

To save updated database into the file, run the following command
> mysqldump -u root -p insight_database > insight_database.sql

## Running the bot
1. Go to Discord and create a server.
2. Open https://discord.com/oauth2/authorize?client_id=1351965308130295859&permissions=8&integration_type=0&scope=bot to add
the bot to your server with administrator permissions.
3. Add the bot token in the `discord_bot.py` file.
4. Run `discord_bot.py`.
5 Ask questions to the bot through your server chat.