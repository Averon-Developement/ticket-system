CREATE DATABASE averon_tickets;
USE averon_tickets;

CREATE TABLE guild_settings (
    guild_id BIGINT PRIMARY KEY,
    max_tickets INT NOT NULL DEFAULT 1,
    transcripts BOOLEAN NOT NULL DEFAULT FALSE,
    transcripts_channel BIGINT NULL
);

CREATE TABLE tickets (
    ticket_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    guild_id BIGINT NOT NULL,
    channel_id BIGINT NOT NULL UNIQUE,
    creator_id BIGINT NOT NULL,
    claimed_by BIGINT NULL,
    claimed_at BIGINT NULL,
    status TINYINT NOT NULL DEFAULT 0
    created_at BIGINT NULL
    closed_by BIGINT NULL,
    closed_at BIGINT NULL,

    FOREIGN KEY (guild_id) REFERENCES guild_settings(guild_id)
        ON DELETE CASCADE
);

CREATE TABLE ticket_blacklist (
    guild_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,

    PRIMARY KEY (guild_id, user_id),

    FOREIGN KEY (guild_id) REFERENCES guild_settings(guild_id)
        ON DELETE CASCADE
); 

CREATE TABLE ticket_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    name VARCHAR(50) NOT NULL,
    emoji VARCHAR(32) NULL,
    button_style TINYINT NOT NULL DEFAULT 1,
    category_id BIGINT NOT NULL,

    FOREIGN KEY (guild_id) REFERENCES guild_settings(guild_id)
        ON DELETE CASCADE
);

CREATE TABLE ticket_type_roles (
    type_id INT NOT NULL,
    role_id BIGINT NOT NULL,

    PRIMARY KEY (type_id, role_id),

    FOREIGN KEY (type_id) REFERENCES ticket_types(type_id)
        ON DELETE CASCADE
);