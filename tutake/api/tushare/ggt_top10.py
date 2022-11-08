"""
This file is auto generator by CodeGenerator. Don't modify it directly, instead alter tushare_api.tmpl of it.

Tushare ggt_top10接口
数据接口-沪深股票-行情数据-港股通十大成交股  https://tushare.pro/document/2?doc_id=49

@author: rmfish
"""
import pandas as pd
import logging
from sqlalchemy import Integer, String, Float, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from tutake.api.tushare.base_dao import BaseDao
from tutake.api.tushare.dao import DAO
from tutake.api.tushare.extends.ggt_top10_ext import *
from tutake.api.tushare.process import ProcessType, DataProcess
from tutake.api.tushare.tushare_base import TuShareBase
from tutake.utils.config import tutake_config
from tutake.utils.decorator import sleep

engine = create_engine("%s/%s" % (tutake_config.get_data_sqlite_driver_url(), 'tushare_ggt_top10.db'))
session_factory = sessionmaker()
session_factory.configure(bind=engine)
Base = declarative_base()
logger = logging.getLogger('api.tushare.ggt_top10')


class TushareGgtTop10(Base):
    __tablename__ = "tushare_ggt_top10"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_date = Column(String, index=True, comment='交易日期')
    ts_code = Column(String, index=True, comment='股票代码')
    name = Column(String, comment='股票名称')
    close = Column(Float, comment='收盘价')
    p_change = Column(Float, comment='涨跌幅')
    rank = Column(String, comment='资金排名')
    market_type = Column(String, index=True, comment='市场类型 2：港股通（沪） 4：港股通（深）')
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


class GgtTop10(BaseDao, TuShareBase, DataProcess):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        query_fields = [
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
        entity_fields = [
            "trade_date", "ts_code", "name", "close", "p_change", "rank", "market_type", "amount", "net_amount",
            "sh_amount", "sh_net_amount", "sh_buy", "sh_sell", "sz_amount", "sz_net_amount", "sz_buy", "sz_sell"
        ]
        BaseDao.__init__(self, engine, session_factory, TushareGgtTop10, 'tushare_ggt_top10', query_fields,
                         entity_fields)
        TuShareBase.__init__(self)
        DataProcess.__init__(self, "ggt_top10")
        self.dao = DAO()

    def ggt_top10(self, fields='', **kwargs):
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
        return super().query(fields, **kwargs)

    def process(self, process_type: ProcessType):
        """
        同步历史数据
        :return:
        """
        return super()._process(process_type, self.fetch_and_append)

    def fetch_and_append(self, **kwargs):
        """
        获取tushare数据并append到数据库中
        :return: 数量行数
        """
        init_args = {
            "ts_code": "",
            "trade_date": "",
            "start_date": "",
            "end_date": "",
            "market_type": "",
            "limit": "",
            "offset": ""
        }
        if len(kwargs.keys()) == 0:
            kwargs = init_args
        # 初始化offset和limit
        if not kwargs.get("limit"):
            kwargs['limit'] = self.default_limit()
        init_offset = 0
        offset = 0
        if kwargs.get('offset'):
            offset = int(kwargs['offset'])
            init_offset = offset

        kwargs = {key: kwargs[key] for key in kwargs.keys() & init_args.keys()}

        @sleep(timeout=61, time_append=60, retry=20, match="^抱歉，您每分钟最多访问该接口")
        def fetch_save(offset_val=0):
            kwargs['offset'] = str(offset_val)
            logger.debug("Invoke pro.ggt_top10 with args: {}".format(kwargs))
            res = self.tushare_api().ggt_top10(**kwargs, fields=self.entity_fields)
            res.to_sql('tushare_ggt_top10', con=engine, if_exists='append', index=False, index_label=['ts_code'])
            return res

        df = fetch_save(offset)
        offset += df.shape[0]
        while kwargs['limit'] != "" and str(df.shape[0]) == kwargs['limit']:
            df = fetch_save(offset)
            offset += df.shape[0]
        return offset - init_offset


setattr(GgtTop10, 'default_limit', default_limit_ext)
setattr(GgtTop10, 'default_order_by', default_order_by_ext)
setattr(GgtTop10, 'prepare', prepare_ext)
setattr(GgtTop10, 'tushare_parameters', tushare_parameters_ext)
setattr(GgtTop10, 'param_loop_process', param_loop_process_ext)

if __name__ == '__main__':
    pd.set_option('display.max_columns', 500)    # 显示列数
    pd.set_option('display.width', 1000)
    logger.setLevel(logging.INFO)
    api = GgtTop10()
    api.process(ProcessType.HISTORY)    # 同步历史数据
    # api.process(ProcessType.INCREASE)  # 同步增量数据
    print(api.ggt_top10())    # 数据查询接口
