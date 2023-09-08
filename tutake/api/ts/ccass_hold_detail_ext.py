"""
Tushare ccass_hold_detail接口
获取中央结算系统机构席位持股明细，数据覆盖全历史，根据交易所披露时间，当日数据在下一交易日早上9点前完成
数据接口-沪深股票-特色数据-中央结算系统持股明细  https://tushare.pro/document/2?doc_id=274
"""


def default_cron_express_ext(self) -> str:
    return ""


def default_order_by_ext(self) -> str:
    """
    查询时默认的排序
    """
    return ''


def default_limit_ext(self) -> str:
    """
    每次取数的默认Limit
    """
    return ""


def prepare_ext(self):
    """
    同步历史数据准备工作
    """


def query_parameters_ext(self):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    return []


def param_loop_process_ext(self, **params):
    """
    每执行一次fetch_and_append前，做一次参数的处理，如果返回None就中断这次执行
    """
    return params
