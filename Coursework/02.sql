SELECT COUNT(S.uun) AS total 
FROM Students S, Degrees D 
WHERE S.degree = D.code AND D.type = 'PG';
