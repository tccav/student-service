-- migrate:up

CREATE TABLE IF NOT EXISTS students
(
	id         bigint PRIMARY KEY,
	name       varchar NOT NULL,
	cpf        varchar NOT NULL,
	birth_date date    NOT NULL,
	email      varchar NOT NULL,
	course_id  uuid    NOT NULL
);

-- migrate:down

DROP TABLE IF EXISTS students;