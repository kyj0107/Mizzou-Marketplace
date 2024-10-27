Hello!

This is the makings of a Mizzou Marketplace website!

10/21/2024 Update:

I've got a Docker environment up and running! Navigate to mu_marketplace_env and run docker compose up -d to install the MySQL container. I haven't gotten around to getting it to work with the Flask app yet, but feel free to play around with the database.

10/27/2024 Update:

Docker is being weird and causing the MySQL container to act up. I've got it working on my end, but if you run into the issue where it restarts constantly for no reason, you'll have to reinstall Docker. Otherwise, run docker exec -it capstone-mysql bash to get into the container! Then use mysql -u root -p (password: root) to log into the server. To load the database, once you're logged into the server, run source ~/sql-files/mizzou_marketplace.sql.