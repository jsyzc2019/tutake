"""
Tushare fina_audit接口
获取上市公司定期财务审计意见数据
数据接口-沪深股票-财务数据-财务审计意见  https://tushare.pro/document/2?doc_id=80
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
    self.delete_all()


def query_parameters_ext(self):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    return self.api.stock_basic.column_data(['ts_code'])


def param_loop_process_ext(self, **params):
    """
    每执行一次fetch_and_append前，做一次参数的处理，如果返回None就中断这次执行
    """
    return params
