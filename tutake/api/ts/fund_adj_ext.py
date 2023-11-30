"""
Tushare fund_adj接口
获取基金复权因子，用于计算基金复权行情
数据接口-公募基金-复权因子  https://tushare.pro/document/2?doc_id=199
"""

from tutake.api.ts.date_utils import start_end_step_params


def default_order_by_ext(self) -> str:
    """
    查询时默认的排序
    """
    return 'trade_date,ts_code desc'


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
