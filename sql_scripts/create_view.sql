CREATE VIEW `statistic` AS SELECT count(1) AS `count` FROM `users`;

CREATE VIEW `sec_tasks_users` AS
SELECT users.user_id AS `user`, sections.section_name AS `section`,
section_tasks.task AS `tasks` FROM `users` LEFT JOIN
sections ON sections.`user` = users.`id` LEFT JOIN
section_tasks ON section_tasks.section = sections.`id`;

CREATE VIEW `oth_tasks_users` AS
SELECT users.user_id AS `user`, other_tasks.task AS `other`
FROM `users` LEFT JOIN
other_tasks ON other_tasks.`user` = users.`id`;