SELECT E.student, MIN(E.grade) AS mingrade, MAX(E.grade) AS maxgrade, COUNT(E.grade) AS totalexams FROM Exams E GROUP BY E.student HAVING AVG(E.grade) >= 75;
