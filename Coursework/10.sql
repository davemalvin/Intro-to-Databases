SELECT S.uun, S.name 
FROM Students S 
EXCEPT 
SELECT S1.uun, S1.name 
FROM (SELECT S.uun, S.name, P.course 
      FROM Programmes P, Students S 
      WHERE P.degree = S.degree 
      EXCEPT 
      SELECT S.uun, S.name, E.course 
      FROM Students S, Exams E 
      WHERE S.uun = E.student) AS S1;
