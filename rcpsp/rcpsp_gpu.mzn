% Resource Constrained Project Scheduling Problem
include "cumulative.mzn";
include "minicpp.mzn";


% Data
% ---
% The number of resources
int: n_res;  
% The set of all resources
set of int: Res = 1..n_res;
% The resource capabilities
array [Res] of int: rc;         
% The number of tasks
int: n_tasks;     
% The set of all tasks                     
set of int: Tasks = 1..n_tasks;    
% The task durations     
array [Tasks] of int: d;  
% The resource requirements
array [Res,Tasks] of int: rr ; 
% The task successors 
array [Tasks] of set of int: suc;  
 % End time of the planning horizon
int: t_max = sum(i in Tasks)(d[i]); 
% Possible start times   
set of int: Times = 0..(t_max - 1);     


% Variables
% ---
% The start times
array [Tasks] of var Times: s; 
% The project duration (makespan)
var 0..t_max: objective      ; 


% Constraints
% ---
% Precedence constraints
constraint forall(i in Tasks, j in suc[i])(s[i] + d[i] <= s[j]);
% Redundant non-overlapping constraints
constraint forall ( i, j in Tasks where i < j )
    (
        if exists(r in Res)(rr[r, i] + rr[r, j] > rc[r]) 
        then
            s[i] + d[i] <= s[j]   \/ s[j] + d[j] <= s[i]
        else
            true
        endif
    );
% Cumulative resource constraints 
constraint forall ( r in Res )
    (
        let 
        { 
            set of int: RTasks = { i | i in Tasks where rr[r, i] > 0 /\ d[i] > 0 },
            int: sum_rr = sum(i in RTasks)(rr[r, i])
        } 
        in 
        (
            if RTasks != {} /\ sum_rr > rc[r] 
            then
                cumulative([s[i] | i in RTasks], [ d[i] | i in RTasks ], [ rr[r, i] | i in RTasks ], rc[r]):: gpu
            else
                true
            endif
        )
    );
% Makespan constraints
constraint forall (i in Tasks where suc[i] == {}) (s[i] + d[i] <= objective);


% Search
% ---
solve:: int_search(s ++ [objective], smallest, indomain_min, complete) minimize objective;


% Output
% ---
output ["Solution = \(s)\nObjective = \(objective)\n"]; 
