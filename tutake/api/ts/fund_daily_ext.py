"""
Tushare fund_daily接口
获取场内基金日线行情，类似股票日行情
数据接口-公募基金-基金行情  https://tushare.pro/document/2?doc_id=127
"""
import pendulum


def default_order_by_ext(self) -> str:
    """
    查询时默认的排序
    """
    return 'trade_date,ts_code'


def default_limit_ext(self) -> str:
    """
    每次取数的默认Limit
    """
    return "1500"


def query_parameters_ext(self):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    max = self.max('trade_date')
    if max:
        start = pendulum.parse(max).add(days=1)
    else:
        min = self.api.fund_basic.min("list_date")
        start = pendulum.parse(min)
    params = []
    now = pendulum.now()
    while start.diff(now).days > 0:
        params.append({"trade_date": start.format("YYYYMMDD")})
        start = start.add(days=1)
    return params
