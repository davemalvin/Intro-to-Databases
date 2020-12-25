SELECT E.student, E.date 
FROM Exams E, (SELECT E.student, MAX(E.date) AS recent 
               FROM Exams E GROUP BY E.student) E1 
WHERE E.student = E1.student AND E.date = E1.recent 
GROUP BY E.student, E.date 
HAVING COUNT(E.date) > 1;
