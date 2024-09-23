-- Создайте студента (student)
INSERT INTO students (name, second_name, group_id) VALUES ('Daria', 'Summerduck', NULL)	

-- Создайте несколько книг (books) и укажите, что ваш созданный студент взял их
INSERT INTO books (title, taken_by_student_id) VALUES ('1984', 2159)

INSERT INTO books (title, taken_by_student_id) 
VALUES ('1985', 2159), ('1986', 2159)

-- Создайте группу (group) и определите своего студента туда
INSERT INTO `groups` (title, start_date, end_date) VALUES ('Summerduck 101', 'aug 2024', 'oct 2024')

UPDATE students SET group_id=1950 WHERE name='Daria'and second_name='Summerduck'

-- Создайте несколько учебных предметов (subjects)
INSERT INTO subjets (title) VALUES ('Mathematics 101'), ('Physics 101');

-- Создайте по два занятия для каждого предмета (lessons)
INSERT INTO lessons (title, subject_id)
VALUES 
('Mathematics Lesson 1', 2780),
('Mathematics Lesson 2', 2780),
('Physics Lesson 1', 2781),
('Physics Lesson 2', 2781);

-- Поставьте своему студенту оценки (marks) для всех созданных вами занятий
INSERT INTO marks (value, lesson_id, student_id)
VALUES
(10, 5774, 2159),
(9, 5773, 2159),
(8, 5772, 2159),
(7, 5771, 2159);