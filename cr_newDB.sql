CREATE TABLE IF NOT EXISTS employee (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
surname text NOT NULL,
email text,
home_address text,
date_of_last_changes date
);

CREATE TABLE IF NOT EXISTS office (
code integer PRIMARY KEY AUTOINCREMENT,
address text NOT NULL,
phone_number integer
);

CREATE TABLE IF NOT EXISTS post (
code integer PRIMARY KEY AUTOINCREMENT,
title text,
Duties text
);

CREATE TABLE IF NOT EXISTS work_record (
id_employee integer,
post_code integer,
office_code integer,
start_date date,
finish_date date,
CONSTRAINT new_pk PRIMARY KEY (id_employee, post_code, office_code),
FOREIGN KEY (id_employee) REFERENCES employee(id),
FOREIGN KEY (post_code) REFERENCES post(code),
FOREIGN KEY (office_code) REFERENCES office(code)
);

CREATE TABLE IF NOT EXISTS history_of_changes (
id_employee integer,
start_date date,
finish_date date,
surname text NOT NULL,
email text,
home_address text,
CONSTRAINT new_pk PRIMARY KEY (id_employee, start_date)
FOREIGN KEY (id_employee) REFERENCES employee(id)
FOREIGN KEY (start_date) REFERENCES employee(date_of_last_changes)
);

--DELETE FROM employee
--WHERE employee.id == 5
--INSERT INTO employee
--(name, surname, email, home_address)
--VALUES ('Анна', 'Ушакова', 'Ushakova@gmail.com', 'адрес');
--INSERT INTO employee
--(id, name, surname, email, home_address)
--VALUES (3, 'Arsen', 'Zlochevsky', 'Zlo@gmail.com', 'myaddress_Ars');
--INSERT INTO employee
--(id, name, surname, email, home_address)
--VALUES (4, 'Olechka', 'Yatsenko', 'olya@gmail.com', 'myaddress_Olya');
--
--INSERT INTO "office"
--(code, address, phone_number)
--VALUES (1, 'addr1', 12345);
--INSERT INTO "office"
--(code, address, phone_number)
--VALUES (2, 'addr2', 23456);
--INSERT INTO "office"
--(code, address, phone_number)
--VALUES (3, 'addr3', 34567);
--
--INSERT INTO "post"
--("code", "title", "Duties")
--VALUES (1, 'post1', 'all1');
--INSERT INTO "post"
--("code", "title", "Duties")
--VALUES (2, 'post2', 'all2');
--INSERT INTO "post"
--("code", "title", "Duties")
--VALUES (3, 'post3', 'all3');
--
