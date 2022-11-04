import pandas as pd
import logging
from sqlalchemy import Integer, String, Float, Column, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from tutake.api.base_dao import BaseDao
from tutake.api.dao import DAO
from tutake.api.process_type import ProcessType
from tutake.api.tushare_base import TuShareBase
from tutake.utils.config import config
from tutake.utils.decorator import sleep
"""
Tushare ggt_top10接口
数据接口-沪深股票-行情数据-港股通十大成交股  https://tushare.pro/document/2?doc_id=49
"""

engine = create_engine("%s/%s" % (config['database']['driver_url'], 'tushare_ggt_top10.db'))
session_factory = sessionmaker()
session_factory.configure(bind=engine)
Base = declarative_base()
logger = logging.getLogger('api.tushare.ggt_top10')


class TushareGgtTop10(Base):
    __tablename__ = "tushare_ggt_top10"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_date = Column(String, comment='交易日期')
    ts_code = Column(String, comment='股票代码')
    name = Column(String, comment='股票名称')
    close = Column(Float, comment='收盘价')
    p_change = Column(Float, comment='涨跌幅')
    rank = Column(String, comment='资金排名')
    market_type = Column(String, comment='市场类型 2：港股通（沪） 4：港股通（深）')
    amount = Column(Float, comment='累计成交金额')
    net_amount = Column(Float, comment='净买入金额')
    sh_amount = Column(Float, comment='沪市成交金额')
    sh_net_amount = Column(Float, comment='沪市净买入金额')
    sh_buy = Column(Float, comment='沪市买入金额')
    sh_sell = Column(Float, comment='沪市卖出金额')
    sz_amount = Column(Float, comment='深市成交金额')
    sz_net_amount = Column(Float, comment='深市净买入金额')
    sz_buy = Column(Float, comment='深市买入金额')
    sz_sell = Column(Float, comment='深市卖出金额')


TushareGgtTop10.__table__.create(bind=engine, checkfirst=True)


class GgtTop10(BaseDao, TuShareBase):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        BaseDao.__init__(self, engine, session_factory, TushareGgtTop10, 'tushare_ggt_top10')
        TuShareBase.__init__(self)
        self.dao = DAO()

    def ggt_top10(self, **kwargs):
        """
        

        | Arguments:
        | ts_code(str):   股票代码
        | trade_date(str):   交易日期
        | start_date(str):   开始日期
        | end_date(str):   结束日期
        | market_type(str):   市场类型 2：港股通（沪） 4：港股通（深）
        | limit(int):   单次返回数据长度
        | offset(int):   请求数据的开始位移量
        

        :return: DataFrame
         trade_date(str)  交易日期
         ts_code(str)  股票代码
         name(str)  股票名称
         close(float)  收盘价
         p_change(float)  涨跌幅
         rank(str)  资金排名
         market_type(str)  市场类型 2：港股通（沪） 4：港股通（深）
         amount(float)  累计成交金额
         net_amount(float)  净买入金额
         sh_amount(float)  沪市成交金额
         sh_net_amount(float)  沪市净买入金额
         sh_buy(float)  沪市买入金额
         sh_sell(float)  沪市卖出金额
         sz_amount(float)  深市成交金额
         sz_net_amount(float)  深市净买入金额
         sz_buy(float)  深市买入金额
         sz_sell(float)  深市卖出金额
        
        """
        args = [
            n for n in [
                'ts_code',
                'trade_date',
                'start_date',
                'end_date',
                'market_type',
                'limit',
                'offset',
            ] if n not in ['limit', 'offset']
        ]
        params = {key: kwargs[key] for key in kwargs.keys() & args}
        query = session_factory().query(TushareGgtTop10).filter_by(**params)
        query = query.order_by(text("trade_date desc,ts_code"))
        input_limit = 10000    # 默认10000条 避免导致数据库压力过大
        if kwargs.get('limit') and str(kwargs.get('limit')).isnumeric():
            input_limit = int(kwargs.get('limit'))
            query = query.limit(input_limit)
        if "" != "":
            default_limit = int("")
            if default_limit < input_limit:
                query = query.limit(default_limit)
        if kwargs.get('offset') and str(kwargs.get('offset')).isnumeric():
            query = query.offset(int(kwargs.get('offset')))
        return pd.read_sql(query.statement, query.session.bind)

    def prepare(self, process_type: ProcessType):
        """
        同步历史数据准备工作
        :return:
        """

    def tushare_parameters(self, process_type: ProcessType):
        """
        同步历史数据调用的参数
        :return: list(dict)
        """
        return [{}]

    def param_loop_process(self, process_type: ProcessType, **params):
        """
        每执行一次fetch_and_append前，做一次参数的处理，如果返回None就中断这次执行
        """
        return params

    def process(self, process_type: ProcessType):
        """
        同步历史数据
        :return:
        """
        self.prepare(process_type)
        params = self.tushare_parameters(process_type)
        logger.debug("Process tushare params is {}".format(params))
        if params:
            for param in params:
                new_param = self.param_loop_process(process_type, **param)
                if new_param is None:
                    logger.debug("Skip exec param: {}".format(param))
                    continue
                try:
                    cnt = self.fetch_and_append(process_type, **new_param)
                    logger.debug("Fetch and append {} data, cnt is {}".format("daily", cnt))
                except Exception as err:
                    if err.args[0].startswith("抱歉，您没有访问该接口的权限") or err.args[0].startswith("抱歉，您每天最多访问该接口"):
                        logger.error("Throw exception with param: {} err:{}".format(new_param, err))
                        return
                    else:
                        logger.error("Execute fetch_and_append throw exp. {}".format(err))
                        continue

    def fetch_and_append(self, process_type: ProcessType, **kwargs):
        """
        获取tushare数据并append到数据库中
        :return: 数量行数
        """
        if len(kwargs.keys()) == 0:
            kwargs = {
                "ts_code": "",
                "trade_date": "",
                "start_date": "",
                "end_date": "",
                "market_type": "",
                "limit": "",
                "offset": ""
            }
        # 初始化offset和limit
        if not kwargs.get("limit"):
            kwargs['limit'] = ""
        init_offset = 0
        offset = 0
        if kwargs.get('offset'):
            offset = int(kwargs['offset'])
            init_offset = offset

        kwargs = {
            key: kwargs[key] for key in kwargs.keys() & list([
                'ts_code',
                'trade_date',
                'start_date',
                'end_date',
                'market_type',
                'limit',
                'offset',
            ])
        }

        @sleep(timeout=5, time_append=30, retry=20, match="^抱歉，您每分钟最多访问该接口")
        def fetch_save(offset_val=0):
            kwargs['offset'] = str(offset_val)
            logger.debug("Invoke pro.ggt_top10 with args: {}".format(kwargs))
            fields = [
                "trade_date", "ts_code", "name", "close", "p_change", "rank", "market_type", "amount", "net_amount",
                "sh_amount", "sh_net_amount", "sh_buy", "sh_sell", "sz_amount", "sz_net_amount", "sz_buy", "sz_sell"
            ]
            res = pro.ggt_top10(**kwargs, fields=fields)
            res.to_sql('tushare_ggt_top10', con=engine, if_exists='append', index=False, index_label=['ts_code'])
            return res

        pro = self.tushare_api()
        df = fetch_save(offset)
        offset += df.shape[0]
        while kwargs['limit'] != "" and str(df.shape[0]) == kwargs['limit']:
            df = fetch_save(offset)
            offset += df.shape[0]
        return offset - init_offset


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    api = GgtTop10()
    # api.process(ProcessType.HISTORY)  # 同步历史数据
    # api.process(ProcessType.INCREASE)  # 同步增量数据
    print(api.ggt_top10())    # 数据查询接口
