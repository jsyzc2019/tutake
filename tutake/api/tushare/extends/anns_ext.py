"""
Tushare anns接口
获取上市公司公告数据及原文文本，数据从2000年开始。
数据接口-另类数据-上市公司公告原文  https://tushare.pro/document/2?doc_id=176
"""

from tutake.api.process_report import ProcessType


def default_cron_express_ext(self) -> str:
    return "0 9 * * *"


def default_order_by_ext(self) -> str:
    """
    查询时默认的排序
    """
    return ''


def default_limit_ext(self) -> str:
    """
    每次取数的默认Limit
    """
    return ''


def prepare_ext(self, process_type: ProcessType):
    """
    同步历史数据准备工作
    """


def tushare_parameters_ext(self, process_type: ProcessType):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    return []


def param_loop_process_ext(self, process_type: ProcessType, **params):
    """
    每执行一次fetch_and_append前，做一次参数的处理，如果返回None就中断这次执行
    """
    return params
