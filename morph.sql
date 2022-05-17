CREATE TABLE t_user (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    ,username VARCHAR(255) NOT NULL
    ,nickname VARCHAR(255) NOT NULL
    ,password VARCHAR(255) NOT NULL
    ,status TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Account status: 1-valid'
    ,created_at DATETIME NOT NULL
    ,updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ,UNIQUE KEY uk_username (username)
) COMMENT 'User';

INSERT INTO t_user (id, username, nickname, password, status, created_at)
VALUES (1, 'admin', 'Administrator', '132e92e991d94525638c1e5ffbf030eb', 1, NOW());
