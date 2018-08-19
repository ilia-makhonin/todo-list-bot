USE `todo_list`;

CREATE TABLE IF NOT EXISTS `users` (
    `id` INT(9) NOT NULL AUTO_INCREMENT,
    `user_id` INT(11) NOT NULL,
    `name` VARCHAR(30) NOT NULL,
    PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `sections` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `section_name` VARCHAR(50) NOT NULL,
    `user` INT(9) NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY (`user`) REFERENCES `users`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `section_tasks` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `task` VARCHAR(250) NOT NULL,
    `section` INT(11) NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY (`section`) REFERENCES `sections`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `other_tasks` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `task` VARCHAR(250) NOT NULL,
    `user` INT(9) NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY (`user`) REFERENCES `users`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);