SELECT E.student, SUM(CASE WHEN E.grade >= 80 
                      THEN 1 ELSE 0 
                      END) AS a, 
                   SUM(CASE WHEN E.grade >= 60 AND E.grade <= 79 
                       THEN 1 ELSE 0 
                       END) AS b, 
                   SUM(CASE WHEN E.grade >= 40 AND E.grade <= 59 
                       THEN 1 ELSE 0 
                       END) AS c, 
                   SUM(CASE WHEN E.grade < 40 
                       THEN 1 ELSE 0 
                       END) AS d 
FROM Exams E 
GROUP BY E.student;
