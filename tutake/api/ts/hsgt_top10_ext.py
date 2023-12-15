"""
沪深股通十大成交股
接口：hsgt_top10
描述：获取沪股通、深股通每日前十大成交详细数据，每天18~20点之间完成当日更新
"""
import pendulum


def default_order_by_ext(self) -> str:
    return "trade_date,ts_code"


def default_limit_ext(self):
    return '300'


def query_parameters_ext(self):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    params = []
    str_format = "YYYYMMDD"
    start_record_date = pendulum.parse('20141117')  # 最早的数据记录
    max_date = self.max("trade_date")
    if max_date is not None:
        start_date = pendulum.parse(max_date).add(days=1)
    else:
        start_date = start_record_date
    while start_date.diff(pendulum.now(), False).in_hours() > 0:
        end_date = start_date.add(days=300)
        params.append({"start_date": start_date.format(str_format), "end_date": end_date.format(str_format)})
        start_date = start_date.add(days=1)
    return params
