"""
Tushare fund_share接口
获取基金规模数据，包含上海和深圳ETF基金
数据接口-公募基金-基金规模  https://tushare.pro/document/2?doc_id=207
"""

from tutake.api.ts.date_utils import start_end_step_params


def default_order_by_ext(self) -> str:
    """
    查询时默认的排序
    """
    return 'trade_date,ts_code'


def default_limit_ext(self) -> str:
    """
    每次取数的默认Limit
    """
    return "2000"


def query_parameters_ext(self):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    return start_end_step_params(self)
