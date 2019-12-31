CREATE DATABASE IF NOT EXISTS aggressive_chores_bot;
USE aggressive_chores_bot;
CREATE TABLE IF NOT EXISTS users
(
    id INT AUTO_INCREMENT PRIMARY KEY
    ,user_id VARCHAR(255) NOT NULL
    ,guild_id VARCHAR(255) NOT NULL
    ,admin_level INT NOT NULL
);
CREATE TABLE IF NOT EXISTS guilds
(
    id INT AUTO_INCREMENT PRIMARY KEY
    ,guild_id VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS chores
(
    id INT AUTO_INCREMENT PRIMARY KEY
    ,user_id VARCHAR(255) NOT NULL
    ,creator VARCHAR(255) NOT NULL
    ,guild_id VARCHAR(255) NOT NULL
    ,description VARCHAR(255) NOT NULL
    ,assigned_date DATETIME NOT NULL
    ,completed_date DATETIME
);
CREATE TABLE IF NOT EXISTS messages
(
    id INT AUTO_INCREMENT PRIMARY KEY
    ,message_id VARCHAR(255) NOT NULL
    ,channel_id VARCHAR(255) NOT NULL
    ,chore_id INT NOT NULL
    ,creation_time DATETIME NOT NULL
);
SHOW TABLES;
SELECT * FROM users;
