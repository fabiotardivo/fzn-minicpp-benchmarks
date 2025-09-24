include "alldifferent.mzn";

int: n; % The number of queens.

array [1..n] of var 1..n: q; % Queens' rows

constraint alldifferent(q);
constraint alldifferent(i in 1..n)(q[i] + i);
constraint alldifferent(i in 1..n)(q[i] - i);

solve :: int_search(q, first_fail, indomain_min, complete) satisfy;

% Output
output ["Solution = \(q)\n"];
