% Bin Packing Problem

include "globals.mzn";
include "minicpp.mzn";

% Constants
int: items;                        % Number of items
int: capacity;                     % Bins' capacity 
array [1..items] of int: weights;  % Items' weights
int: n_bins;                       % Number of bins (Optimal)

% Decisional variables
array [1..items] of var 1..items: items_bin;

% Constraints
constraint forall(i in 1..items)(items_bin[i] <= n_bins);
constraint bin_packing(capacity, items_bin, weights);

% Search heuristic
solve ::int_search(items_bin, input_order, indomain_min, complete) satisfy;


% Output
output ["Solution = \(items_bin)\n"]; 
