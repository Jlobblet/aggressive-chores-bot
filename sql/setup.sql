CREATE DATABASE IF NOT EXISTS aggressive_chores_bot;
USE aggressive_chores_bot;
CREATE TABLE IF NOT EXISTS users
(
    id INT AUTO_INCREMENT PRIMARY KEY
    ,user_id BIGINT(255) NOT NULL
    ,guild_id BIGINT(255) NOT NULL
    ,admin_level INT NOT NULL DEFAULT 0
    ,points INT DEFAULT 0
    ,registered BOOLEAN DEFAULT 0
);
CREATE TABLE IF NOT EXISTS guilds
(
    id INT AUTO_INCREMENT PRIMARY KEY
    ,guild_id BIGINT(255) NOT NULL
    ,prefix VARCHAR(10) NOT NULL DEFAULT "|"
);
CREATE TABLE IF NOT EXISTS chores
(
    id INT AUTO_INCREMENT PRIMARY KEY
    ,user_id BIGINT(255) NOT NULL
    ,creator BIGINT(255) NOT NULL
    ,guild_id BIGINT(255) NOT NULL
    ,description VARCHAR(255) NOT NULL
    ,assigned_date DATETIME NOT NULL
    ,deadline DATETIME DEFAULT NULL
    ,completed_date DATETIME DEFAULT NULL
    ,time_taken BIGINT DEFAULT NULL
    ,points INT DEFAULT 0
    ,hidden BOOLEAN DEFAULT 0
    ,chore_id INT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages
(
    id INT AUTO_INCREMENT PRIMARY KEY
    ,message_id BIGINT(255) NOT NULL
    ,channel_id BIGINT(255) NOT NULL
    ,chore_id INT NOT NULL
    ,creation_time DATETIME NOT NULL
);
