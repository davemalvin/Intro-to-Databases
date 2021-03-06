SELECT D.code, SUM(C.credits) AS totalcredits 
FROM Degrees D, Programmes P, Courses C 
WHERE P.degree = D.code AND P.course = C.code 
GROUP BY D.code 
UNION 
SELECT D.code, 0 
FROM Degrees D 
WHERE D.code <> ALL(SELECT P.degree FROM Programmes P);
