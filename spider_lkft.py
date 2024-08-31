from datetime import datetime
from pathlib import Path
from liebes.sql_helper import SQLHelper
from liebes.CiObjects import DBCheckout, DBBuild, DBTestRun, DBTest, Checkout
from liebes.analysis import CIAnalysis
import openpyxl
from liebes.ci_logger import logger
from liebes.GitHelper import GitHelper
from liebes.Glibc_CG import CallGraph as G_CG
from liebes.CallGraph import CallGraph as CG
import pickle
import pathlib
import re

# if __name__ == "__main__":
#     sql = SQLHelper()
#     checkouts = sql.session.query(DBCheckout).order_by(DBCheckout.git_commit_datetime.desc()).limit(600).all()
#     cia = CIAnalysis()
#     for ch in checkouts:
#         cia.ci_objs.append(Checkout(ch))

#     case_num = 0
#     for c in cia.ci_objs:
#         test_cases = c.get_all_testcases()
#         case_num = case_num + len(test_cases)
    
#     logger.info(f'commits num: {len(cia.ci_objs)} ; case num: {case_num}')

def data_cout(cia: CIAnalysis):
    case_num = 0
    for c in cia.ci_objs:
        test_cases = c.get_all_testcases()
        case_num = case_num + len(test_cases)
    
    avg_cout = int(case_num / len(cia.ci_objs))
    logger.info(f'commits num: {len(cia.ci_objs)} ; case num: {case_num} ; avg num: {avg_cout}')


if __name__ == "__main__":
    sql = SQLHelper()
    checkouts = sql.session.query(DBCheckout).order_by(DBCheckout.git_commit_datetime.desc()).limit(600).all()
    cia = CIAnalysis()

    for ch in checkouts:
        cia.ci_objs.append(Checkout(ch))
    data_cout(cia)
    cia.set_parallel_number(40)
    cia.filter_job("COMBINE_SAME_CASE")
    data_cout(cia)
    cia.filter_job("FILTER_SMALL_BRANCH", minimal_testcases=20)
    cia.filter_job("COMBINE_SAME_CONFIG")
    cia.filter_job("CHOOSE_ONE_BUILD")
    cia.filter_job("FILTER_SMALL_BRANCH", minimal_testcases=20)
    data_cout(cia)
    cia.filter_job("FILTER_FAIL_CASES_IN_LAST_VERSION")
    data_cout(cia)

    cia.ci_objs = cia.ci_objs[1:]
    cia.statistic_data()

        

