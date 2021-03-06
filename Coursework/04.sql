SELECT DISTINCT E.student 
FROM Exams E, (SELECT E.student, COUNT(E.grade) AS fail 
               FROM Exams E 
               WHERE E.grade < 40 
               GROUP BY E.student) AS F 
WHERE E.student = F.student 
GROUP BY E.student, F.fail 
HAVING (CAST(F.fail AS NUMERIC) / COUNT(E.grade)) > 0.3;
