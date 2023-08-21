def default_cron_express_ext(self) -> str:
    return ""


def default_order_by_ext(self) -> str:
    return "cal_date,exchange"


def default_limit_ext(self):
    return ''


def prepare_ext(self):
    """
    同步历史数据准备工作
    :return:
    """
    self.delete_all()


def query_parameters_ext(self):
    """
    同步历史数据调用的参数
    :return: list(dict)
    """
    return [{'exchange': 'SSE'}, {'exchange': 'SZSE'}, {'exchange': 'CFFEX'}, {'exchange': 'SHFE'},
            {'exchange': 'CZCE'}, {'exchange': 'DCE'}, {'exchange': 'INE'}]


def param_loop_process_ext(self, **params):
    """
    每执行一次fetch_and_append前，做一次参数的处理，如果返回None就中断这次执行
    """
    return params
