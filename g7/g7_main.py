# main_g7.py
import config

from g7_logic import (
    parse_requirements,
    if_else_syntax_check,
    for_condition_syntax_check,
    while_syntax_check,
    switch_syntax_check,
    edge_case_check,
    checklist_presence,
    div_by_zero_check,
    infinite_loop_check,
    null_pointer_check,
    out_of_range_check,
    var_input_analysis
)
from config import DEFAULT_SRS_PATH
def main():

    algo_req = parse_requirements(DEFAULT_SRS_PATH)

    ## Objective G 7.1 ##
    if_else_syntax_check(algo_req)
    for_condition_syntax_check(algo_req)
    while_syntax_check(algo_req)
    switch_syntax_check(algo_req)

    ## Objective G 7.2 ##
    edge_case_check(algo_req)

    ## Objective G 7.3 ##
    checklist_presence(algo_req)

    ## Objective G 7.7 ##
    div_by_zero_check(algo_req)
    infinite_loop_check(algo_req)
    null_pointer_check(algo_req)
    out_of_range_check(algo_req)
    var_input_analysis(algo_req)

if __name__ == "__main__":
    main()
