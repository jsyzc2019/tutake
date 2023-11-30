import pendulum


def default_order_by_ext(self) -> str:
    """
    查询时默认的排序
    """
    return 'trade_date desc'


def default_limit_ext(self) -> str:
    """
    每次取数的默认Limit
    """
    return '4000'


def query_parameters_ext(self):
    """
    同步历史数据调用的参数
    :return: list(dict)
    XIN9	富时中国A50指数 (富时A50)
    HSI	恒生指数
    HKTECH	恒生科技指数
    HKAH	恒生AH溢价指数
    DJI	道琼斯工业指数
    SPX	标普500指数
    IXIC	纳斯达克指数
    FTSE	富时100指数
    FCHI	法国CAC40指数
    GDAXI	德国DAX指数
    N225	日经225指数
    KS11	韩国综合指数
    AS51	澳大利亚标普200指数
    SENSEX	印度孟买SENSEX指数
    IBOVESPA	巴西IBOVESPA指数
    RTS	俄罗斯RTS指数
    TWII	台湾加权指数
    CKLSE	马来西亚指数
    SPTSX	加拿大S&P/TSX指数
    CSX5P	STOXX欧洲50指数
    RUT	罗素2000指数
    """

    return [{'ts_code': 'XIN9'}, {'ts_code': 'HSI'}, {'ts_code': 'HKTECH'}, {'ts_code': 'HKAH'}, {'ts_code': 'DJI'},
            {'ts_code': 'SPX'}, {'ts_code': 'IXIC'}, {'ts_code': 'FTSE'}, {'ts_code': 'FCHI'}, {'ts_code': 'GDAXI'},
            {'ts_code': 'N225'}, {'ts_code': 'KS11'}, {'ts_code': 'AS51'}, {'ts_code': 'SENSEX'},
            {'ts_code': 'IBOVESPA'},
            {'ts_code': 'RTS'}, {'ts_code': 'TWII'}, {'ts_code': 'CKLSE'}, {'ts_code': 'SPTSX'}, {'ts_code': 'CSX5P'},
            {'ts_code': 'RUT'}]


def param_loop_process_ext(self, **params):
    """
    每执行一次fetch_and_append前，做一次参数的处理，如果返回None就中断这次执行
    """
    date_format = 'YYYYMMDD'
    max_date = self.max("trade_date", "ts_code = '%s'" % params['ts_code'])
    if max_date is None:
        params['start_date'] = ""
    elif max_date == pendulum.now().format(date_format):
        # 如果已经是最新时间
        return None
    else:
        max_date = pendulum.parse(max_date)
        start_date = max_date.add(days=1)
        params['start_date'] = start_date.format(date_format)
    return params
