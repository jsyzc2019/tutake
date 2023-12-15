import pendulum


def default_order_by_ext(self) -> str:
    return "trade_date,ts_code"


def default_limit_ext(self):
    return ''


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
        trade_date = pendulum.parse(max_date).add(days=1)
    else:
        trade_date = start_record_date
    while trade_date.diff(pendulum.now(), False).in_hours() > 0:
        params.append({"trade_date": trade_date.format(str_format)})
        trade_date = trade_date.add(days=1)
    return params
