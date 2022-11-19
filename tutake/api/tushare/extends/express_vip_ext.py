from tutake.api.process_report import ProcessType
from tutake.api.tushare.extends.date_utils import financial_report_time_params


def default_cron_express_ext(self) -> str:
    return "0 1 * * *"


def default_order_by_ext(self) -> str:
    """
    查询时默认的排序
    """
    return 'end_date desc,ann_date desc'


def default_limit_ext(self) -> str:
    """
    每次取数的默认Limit
    """
    return '5000'


def prepare_ext(self, process_type: ProcessType):
    """
    同步历史数据准备工作
    """


def tushare_parameters_ext(self, process_type: ProcessType):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    return financial_report_time_params(self, process_type, '20041231')


def param_loop_process_ext(self, process_type: ProcessType, **params):
    """
    每执行一次fetch_and_append前，做一次参数的处理，如果返回None就中断这次执行
    """
    return params
