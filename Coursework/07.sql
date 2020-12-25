SELECT P.course FROM Programmes P, Degrees D WHERE P.degree = D.code AND D.type = 'UG' INTERSECT SELECT P.course FROM Programmes P, Degrees D WHERE P.degree = D.code AND D.type = 'PG';
