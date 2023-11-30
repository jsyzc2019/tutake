"""
业绩预告
接口：forecast，可以通过数据工具调试和查看数据。
描述：获取业绩预告数据
权限：用户需要至少800积分才可以调取，具体请参阅积分获取办法
"""
import pendulum


def default_cron_express_ext(self) -> str:
    return "0 3 * * *"


def default_order_by_ext(self) -> str:
    """
    查询时默认的排序
    """
    return "end_date desc,f_ann_date"


def default_limit_ext(self) -> str:
    """
    每次取数的默认Limit
    """
    return '3500'


def query_parameters_ext(self):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    params = []
    str_format = "YYYYMMDD"
    start_record_period = pendulum.parse('19901231')  # 最早的数据记录
    max_period = self.max("end_date")
    if max_period is not None:
        period = pendulum.parse(max_period).add(months=3).last_of("quarter")
    else:
        period = start_record_period
    while period.diff(pendulum.now().last_of('quarter'), False).in_days() > 0:
        params.append({"period": period.format(str_format)})
        period = period.add(months=3).last_of("quarter")
    return params
