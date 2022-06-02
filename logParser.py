from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

# FlatZinc output grammar
FznOutputGrammar = Grammar("""
    outputs = output+
    output = instance statistics result* search_status? statistics+
    instance = "%%%mzn-stat: dzn=" word ".dzn" nl
    statistics = statistic+ "%%%mzn-stat-end" nl
    statistic = "%%%mzn-stat: " word "=" value nl
    result = solution objective? timestamp "----------" nl
    solution = "Solution = [" int_list "]" nl 
    objective = "Objective = " int nl 
    timestamp = "% time elapsed: " float " s" nl
    search_status = search_completed / search_unknown / search_error
    search_completed = "==========" nl "% time elapsed: " float " s" nl
    search_unknown = "=====UNKNOWN=====" nl "% time elapsed: " float " s" nl
    search_error = "=====ERROR=====" nl "% time elapsed: " float " s" nl
    int_list = int (", " int)*
    str = ~"."+
    word = ~"[a-zA-Z0-9_]"+
    value = float / int
    int = ~"[-+]"? ~"[0-9]"+
    float = int "." int
    nl = ~"\\n"
    """)

# FlatZinc statistics
fzn_statistics = ["failures", "initTime", "nodes", "peakDepth", "propagations", "solutions", "solveTime", "variables"]

# FlatZinc output tree visitor
class FznOutputVisitor(NodeVisitor):

    def __init__ (self):
        self.current_instance = ""
        self.current_stats = []
        self.stats_header = ["instance", "searchCompleted"] + fzn_statistics
        self.stats_rows = []
        self.results_header = ["instance", "time", "objective", "solution"]
        self.results_rows = []

    def visit_outputs(self, node, visited_children):
        return {"stats_header": self.stats_header, 
                "stats_rows" : self.stats_rows,
                "results_header" : self.results_header,
                "results_rows" : self.results_rows}
                
    def visit_output(self, node, visited_children):
        self.stats_rows.append(self.current_stats)

    def visit_instance(self, node, visited_children):
        self.current_instance = visited_children[1]
        self.current_stats = [None] * len(self.stats_header)
        self.current_stats[0] = self.current_instance
        self.current_stats[1] = 0 # Search completed

    def visit_statistic(self, node, visited_children):
        stat_name = visited_children[1]
        stat_val = visited_children[3]
        if stat_name in fzn_statistics:
            stat_idx = self.stats_header.index(stat_name)
            self.current_stats[stat_idx] = stat_val

    def visit_search_completed(self, node, visited_children):
        self.current_stats[1] = 1

    def visit_result(self, node, visited_children):
        # Satisfiability
        if len(visited_children) == 4:
            solution = visited_children[0]
            time = visited_children[1]
            self.results_rows.append([self.current_instance, time, None, solution])
        else: # Optimization
            solution = visited_children[0]
            objective = visited_children[1]
            time = visited_children[2]
            self.results_rows.append([self.current_instance, time, objective, solution])

    def visit_solution(self, node, visited_children):
        return visited_children[1]

    def visit_objective(self, node, visited_children):
        return visited_children[1]

    def visit_timestamp(self, node, visited_children):
        return visited_children[1]

    def visit_int_list(self, node, visited_children):
        return node.text.replace(",", "")

    def visit_value(self, node, visited_children):
        return visited_children[0]

    def visit_float(self, node, visited_children):
        return float(node.text)

    def visit_int(self, node, visited_children):
        return int(node.text)

    def visit_word(self, node, visited_children):
        return node.text

    def visit_str(self, node, visited_children):
        return node.text
    
    def generic_visit(self, node, visited_children):
        if len(visited_children) == 0:
            return None
        else:
            return visited_children[0]
