SELECT S.uun 
FROM Students S 
WHERE NOT EXISTS (SELECT DISTINCT E.student 
                  FROM Exams E 
                  WHERE S.uun = E.student);
