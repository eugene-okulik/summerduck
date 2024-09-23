-- Все оценки студента
SELECT * FROM marks WHERE student_id='2159' ORDER BY id DESC

-- Все книги, которые находятся у студента
SELECT * FROM books  WHERE taken_by_student_id='2159' ORDER BY id DESC

-- Для вашего студента выведите всё, что о нем есть в базе: группа, книги, оценки с названиями занятий и предметов (всё одним запросом с использованием Join)
SELECT 
    students.name, 
    students.second_name, 
    `groups`.title AS group_title, 
    books.title AS book_title, 
    marks.value AS mark_value, 
    lessons.title AS lesson_title, 
    subjets.title AS subject_title
FROM students
LEFT JOIN `groups` ON students.group_id = groups.id
LEFT JOIN books ON students.id = books.taken_by_student_id
LEFT JOIN marks ON students.id = marks.student_id
LEFT JOIN lessons ON marks.lesson_id = lessons.id
LEFT JOIN subjets ON lessons.subject_id = subjets.id
WHERE students.id = 2159;
