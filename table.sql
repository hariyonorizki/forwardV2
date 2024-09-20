CREATE DATABASE IF NOT EXISTS telegram_bot;

USE telegram_bot;

-- Tabel untuk menyimpan task
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(255) NOT NULL UNIQUE,
    filter TEXT NOT NULL DEFAULT 'all',
    blacklist TEXT DEFAULT NULL,
    replace TEXT DEFAULT NULL
);

-- Tabel untuk menyimpan sesi pengguna
CREATE TABLE IF NOT EXISTS user_sessions (
    user_id BIGINT NOT NULL UNIQUE,
    session_data TEXT NOT NULL,
    phone_encrypted BLOB NOT NULL,
    PRIMARY KEY (user_id)
);

-- Tabel untuk menyimpan log
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);