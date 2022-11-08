"""
This file is auto generator by CodeGenerator. Don't modify it directly, instead alter tushare_api.tmpl of it.

Tushare cashflow_vip接口
数据接口-沪深股票-财务数据-现金流量表  https://tushare.pro/document/2?doc_id=4400

@author: rmfish
"""
import pandas as pd
import logging
from sqlalchemy import Integer, String, Float, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from tutake.api.tushare.base_dao import BaseDao
from tutake.api.tushare.dao import DAO
from tutake.api.tushare.extends.cashflow_vip_ext import *
from tutake.api.tushare.process import ProcessType, DataProcess
from tutake.api.tushare.tushare_base import TuShareBase
from tutake.utils.config import tutake_config
from tutake.utils.decorator import sleep

engine = create_engine("%s/%s" % (tutake_config.get_data_sqlite_driver_url(), 'tushare_cashflow_vip.db'))
session_factory = sessionmaker()
session_factory.configure(bind=engine)
Base = declarative_base()
logger = logging.getLogger('api.tushare.cashflow_vip')


class TushareCashflowVip(Base):
    __tablename__ = "tushare_cashflow_vip"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String, index=True, comment='TS股票代码')
    ann_date = Column(String, index=True, comment='公告日期')
    f_ann_date = Column(String, index=True, comment='实际公告日期')
    end_date = Column(String, index=True, comment='报告期')
    comp_type = Column(String, index=True, comment='公司类型(1一般工商业2银行3保险4证券)')
    report_type = Column(String, index=True, comment='报表类型')
    end_type = Column(String, index=True, comment='报告期类型')
    net_profit = Column(Float, comment='净利润')
    finan_exp = Column(Float, comment='财务费用')
    c_fr_sale_sg = Column(Float, comment='销售商品、提供劳务收到的现金')
    recp_tax_rends = Column(Float, comment='收到的税费返还')
    n_depos_incr_fi = Column(Float, comment='客户存款和同业存放款项净增加额')
    n_incr_loans_cb = Column(Float, comment='向中央银行借款净增加额')
    n_inc_borr_oth_fi = Column(Float, comment='向其他金融机构拆入资金净增加额')
    prem_fr_orig_contr = Column(Float, comment='收到原保险合同保费取得的现金')
    n_incr_insured_dep = Column(Float, comment='保户储金净增加额')
    n_reinsur_prem = Column(Float, comment='收到再保业务现金净额')
    n_incr_disp_tfa = Column(Float, comment='处置交易性金融资产净增加额')
    ifc_cash_incr = Column(Float, comment='收取利息和手续费净增加额')
    n_incr_disp_faas = Column(Float, comment='处置可供出售金融资产净增加额')
    n_incr_loans_oth_bank = Column(Float, comment='拆入资金净增加额')
    n_cap_incr_repur = Column(Float, comment='回购业务资金净增加额')
    c_fr_oth_operate_a = Column(Float, comment='收到其他与经营活动有关的现金')
    c_inf_fr_operate_a = Column(Float, comment='经营活动现金流入小计')
    c_paid_goods_s = Column(Float, comment='购买商品、接受劳务支付的现金')
    c_paid_to_for_empl = Column(Float, comment='支付给职工以及为职工支付的现金')
    c_paid_for_taxes = Column(Float, comment='支付的各项税费')
    n_incr_clt_loan_adv = Column(Float, comment='客户贷款及垫款净增加额')
    n_incr_dep_cbob = Column(Float, comment='存放央行和同业款项净增加额')
    c_pay_claims_orig_inco = Column(Float, comment='支付原保险合同赔付款项的现金')
    pay_handling_chrg = Column(Float, comment='支付手续费的现金')
    pay_comm_insur_plcy = Column(Float, comment='支付保单红利的现金')
    oth_cash_pay_oper_act = Column(Float, comment='支付其他与经营活动有关的现金')
    st_cash_out_act = Column(Float, comment='经营活动现金流出小计')
    n_cashflow_act = Column(Float, comment='经营活动产生的现金流量净额')
    oth_recp_ral_inv_act = Column(Float, comment='收到其他与投资活动有关的现金')
    c_disp_withdrwl_invest = Column(Float, comment='收回投资收到的现金')
    c_recp_return_invest = Column(Float, comment='取得投资收益收到的现金')
    n_recp_disp_fiolta = Column(Float, comment='处置固定资产、无形资产和其他长期资产收回的现金净额')
    n_recp_disp_sobu = Column(Float, comment='处置子公司及其他营业单位收到的现金净额')
    stot_inflows_inv_act = Column(Float, comment='投资活动现金流入小计')
    c_pay_acq_const_fiolta = Column(Float, comment='购建固定资产、无形资产和其他长期资产支付的现金')
    c_paid_invest = Column(Float, comment='投资支付的现金')
    n_disp_subs_oth_biz = Column(Float, comment='取得子公司及其他营业单位支付的现金净额')
    oth_pay_ral_inv_act = Column(Float, comment='支付其他与投资活动有关的现金')
    n_incr_pledge_loan = Column(Float, comment='质押贷款净增加额')
    stot_out_inv_act = Column(Float, comment='投资活动现金流出小计')
    n_cashflow_inv_act = Column(Float, comment='投资活动产生的现金流量净额')
    c_recp_borrow = Column(Float, comment='取得借款收到的现金')
    proc_issue_bonds = Column(Float, comment='发行债券收到的现金')
    oth_cash_recp_ral_fnc_act = Column(Float, comment='收到其他与筹资活动有关的现金')
    stot_cash_in_fnc_act = Column(Float, comment='筹资活动现金流入小计')
    free_cashflow = Column(Float, comment='企业自由现金流量')
    c_prepay_amt_borr = Column(Float, comment='偿还债务支付的现金')
    c_pay_dist_dpcp_int_exp = Column(Float, comment='分配股利、利润或偿付利息支付的现金')
    incl_dvd_profit_paid_sc_ms = Column(Float, comment='其中:子公司支付给少数股东的股利、利润')
    oth_cashpay_ral_fnc_act = Column(Float, comment='支付其他与筹资活动有关的现金')
    stot_cashout_fnc_act = Column(Float, comment='筹资活动现金流出小计')
    n_cash_flows_fnc_act = Column(Float, comment='筹资活动产生的现金流量净额')
    eff_fx_flu_cash = Column(Float, comment='汇率变动对现金的影响')
    n_incr_cash_cash_equ = Column(Float, comment='现金及现金等价物净增加额')
    c_cash_equ_beg_period = Column(Float, comment='期初现金及现金等价物余额')
    c_cash_equ_end_period = Column(Float, comment='期末现金及现金等价物余额')
    c_recp_cap_contrib = Column(Float, comment='吸收投资收到的现金')
    incl_cash_rec_saims = Column(Float, comment='其中:子公司吸收少数股东投资收到的现金')
    uncon_invest_loss = Column(Float, comment='未确认投资损失')
    prov_depr_assets = Column(Float, comment='加:资产减值准备')
    depr_fa_coga_dpba = Column(Float, comment='固定资产折旧、油气资产折耗、生产性生物资产折旧')
    amort_intang_assets = Column(Float, comment='无形资产摊销')
    lt_amort_deferred_exp = Column(Float, comment='长期待摊费用摊销')
    decr_deferred_exp = Column(Float, comment='待摊费用减少')
    incr_acc_exp = Column(Float, comment='预提费用增加')
    loss_disp_fiolta = Column(Float, comment='处置固定、无形资产和其他长期资产的损失')
    loss_scr_fa = Column(Float, comment='固定资产报废损失')
    loss_fv_chg = Column(Float, comment='公允价值变动损失')
    invest_loss = Column(Float, comment='投资损失')
    decr_def_inc_tax_assets = Column(Float, comment='递延所得税资产减少')
    incr_def_inc_tax_liab = Column(Float, comment='递延所得税负债增加')
    decr_inventories = Column(Float, comment='存货的减少')
    decr_oper_payable = Column(Float, comment='经营性应收项目的减少')
    incr_oper_payable = Column(Float, comment='经营性应付项目的增加')
    others = Column(Float, comment='其他')
    im_net_cashflow_oper_act = Column(Float, comment='经营活动产生的现金流量净额(间接法)')
    conv_debt_into_cap = Column(Float, comment='债务转为资本')
    conv_copbonds_due_within_1y = Column(Float, comment='一年内到期的可转换公司债券')
    fa_fnc_leases = Column(Float, comment='融资租入固定资产')
    im_n_incr_cash_equ = Column(Float, comment='现金及现金等价物净增加额(间接法)')
    net_dism_capital_add = Column(Float, comment='拆出资金净增加额')
    net_cash_rece_sec = Column(Float, comment='代理买卖证券收到的现金净额(元)')
    credit_impa_loss = Column(Float, comment='信用减值损失')
    use_right_asset_dep = Column(Float, comment='使用权资产折旧')
    oth_loss_asset = Column(Float, comment='其他资产减值损失')
    end_bal_cash = Column(Float, comment='现金的期末余额')
    beg_bal_cash = Column(Float, comment='减:现金的期初余额')
    end_bal_cash_equ = Column(Float, comment='加:现金等价物的期末余额')
    beg_bal_cash_equ = Column(Float, comment='减:现金等价物的期初余额')
    update_flag = Column(String, comment='更新标志')


TushareCashflowVip.__table__.create(bind=engine, checkfirst=True)


class CashflowVip(BaseDao, TuShareBase, DataProcess):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        query_fields = [
            n for n in [
                'ts_code',
                'ann_date',
                'f_ann_date',
                'start_date',
                'end_date',
                'period',
                'report_type',
                'comp_type',
                'end_type',
                'is_calc',
                'limit',
                'offset',
            ] if n not in ['limit', 'offset']
        ]
        entity_fields = [
            "ts_code", "ann_date", "f_ann_date", "end_date", "comp_type", "report_type", "end_type", "net_profit",
            "finan_exp", "c_fr_sale_sg", "recp_tax_rends", "n_depos_incr_fi", "n_incr_loans_cb", "n_inc_borr_oth_fi",
            "prem_fr_orig_contr", "n_incr_insured_dep", "n_reinsur_prem", "n_incr_disp_tfa", "ifc_cash_incr",
            "n_incr_disp_faas", "n_incr_loans_oth_bank", "n_cap_incr_repur", "c_fr_oth_operate_a", "c_inf_fr_operate_a",
            "c_paid_goods_s", "c_paid_to_for_empl", "c_paid_for_taxes", "n_incr_clt_loan_adv", "n_incr_dep_cbob",
            "c_pay_claims_orig_inco", "pay_handling_chrg", "pay_comm_insur_plcy", "oth_cash_pay_oper_act",
            "st_cash_out_act", "n_cashflow_act", "oth_recp_ral_inv_act", "c_disp_withdrwl_invest",
            "c_recp_return_invest", "n_recp_disp_fiolta", "n_recp_disp_sobu", "stot_inflows_inv_act",
            "c_pay_acq_const_fiolta", "c_paid_invest", "n_disp_subs_oth_biz", "oth_pay_ral_inv_act",
            "n_incr_pledge_loan", "stot_out_inv_act", "n_cashflow_inv_act", "c_recp_borrow", "proc_issue_bonds",
            "oth_cash_recp_ral_fnc_act", "stot_cash_in_fnc_act", "free_cashflow", "c_prepay_amt_borr",
            "c_pay_dist_dpcp_int_exp", "incl_dvd_profit_paid_sc_ms", "oth_cashpay_ral_fnc_act", "stot_cashout_fnc_act",
            "n_cash_flows_fnc_act", "eff_fx_flu_cash", "n_incr_cash_cash_equ", "c_cash_equ_beg_period",
            "c_cash_equ_end_period", "c_recp_cap_contrib", "incl_cash_rec_saims", "uncon_invest_loss",
            "prov_depr_assets", "depr_fa_coga_dpba", "amort_intang_assets", "lt_amort_deferred_exp",
            "decr_deferred_exp", "incr_acc_exp", "loss_disp_fiolta", "loss_scr_fa", "loss_fv_chg", "invest_loss",
            "decr_def_inc_tax_assets", "incr_def_inc_tax_liab", "decr_inventories", "decr_oper_payable",
            "incr_oper_payable", "others", "im_net_cashflow_oper_act", "conv_debt_into_cap",
            "conv_copbonds_due_within_1y", "fa_fnc_leases", "im_n_incr_cash_equ", "net_dism_capital_add",
            "net_cash_rece_sec", "credit_impa_loss", "use_right_asset_dep", "oth_loss_asset", "end_bal_cash",
            "beg_bal_cash", "end_bal_cash_equ", "beg_bal_cash_equ", "update_flag"
        ]
        BaseDao.__init__(self, engine, session_factory, TushareCashflowVip, 'tushare_cashflow_vip', query_fields,
                         entity_fields)
        TuShareBase.__init__(self)
        DataProcess.__init__(self, "cashflow_vip")
        self.dao = DAO()

    def cashflow_vip(self, fields='', **kwargs):
        """
        
        | Arguments:
        | ts_code(str): required  股票代码
        | ann_date(str):   公告日期
        | f_ann_date(str):   实际公告日期
        | start_date(str):   报告期开始日期
        | end_date(str):   报告期结束日期
        | period(str):   报告期
        | report_type(str):   报告类型
        | comp_type(str):   公司类型
        | end_type(str):   报告期编号，1~4报告期
        | is_calc(int):   是否计算报表
        | limit(int):   单次返回数据长度
        | offset(int):   请求数据的开始位移量
        
        :return: DataFrame
         ts_code(str)  TS股票代码
         ann_date(str)  公告日期
         f_ann_date(str)  实际公告日期
         end_date(str)  报告期
         comp_type(str)  公司类型(1一般工商业2银行3保险4证券)
         report_type(str)  报表类型
         end_type(str)  报告期类型
         net_profit(float)  净利润
         finan_exp(float)  财务费用
         c_fr_sale_sg(float)  销售商品、提供劳务收到的现金
         recp_tax_rends(float)  收到的税费返还
         n_depos_incr_fi(float)  客户存款和同业存放款项净增加额
         n_incr_loans_cb(float)  向中央银行借款净增加额
         n_inc_borr_oth_fi(float)  向其他金融机构拆入资金净增加额
         prem_fr_orig_contr(float)  收到原保险合同保费取得的现金
         n_incr_insured_dep(float)  保户储金净增加额
         n_reinsur_prem(float)  收到再保业务现金净额
         n_incr_disp_tfa(float)  处置交易性金融资产净增加额
         ifc_cash_incr(float)  收取利息和手续费净增加额
         n_incr_disp_faas(float)  处置可供出售金融资产净增加额
         n_incr_loans_oth_bank(float)  拆入资金净增加额
         n_cap_incr_repur(float)  回购业务资金净增加额
         c_fr_oth_operate_a(float)  收到其他与经营活动有关的现金
         c_inf_fr_operate_a(float)  经营活动现金流入小计
         c_paid_goods_s(float)  购买商品、接受劳务支付的现金
         c_paid_to_for_empl(float)  支付给职工以及为职工支付的现金
         c_paid_for_taxes(float)  支付的各项税费
         n_incr_clt_loan_adv(float)  客户贷款及垫款净增加额
         n_incr_dep_cbob(float)  存放央行和同业款项净增加额
         c_pay_claims_orig_inco(float)  支付原保险合同赔付款项的现金
         pay_handling_chrg(float)  支付手续费的现金
         pay_comm_insur_plcy(float)  支付保单红利的现金
         oth_cash_pay_oper_act(float)  支付其他与经营活动有关的现金
         st_cash_out_act(float)  经营活动现金流出小计
         n_cashflow_act(float)  经营活动产生的现金流量净额
         oth_recp_ral_inv_act(float)  收到其他与投资活动有关的现金
         c_disp_withdrwl_invest(float)  收回投资收到的现金
         c_recp_return_invest(float)  取得投资收益收到的现金
         n_recp_disp_fiolta(float)  处置固定资产、无形资产和其他长期资产收回的现金净额
         n_recp_disp_sobu(float)  处置子公司及其他营业单位收到的现金净额
         stot_inflows_inv_act(float)  投资活动现金流入小计
         c_pay_acq_const_fiolta(float)  购建固定资产、无形资产和其他长期资产支付的现金
         c_paid_invest(float)  投资支付的现金
         n_disp_subs_oth_biz(float)  取得子公司及其他营业单位支付的现金净额
         oth_pay_ral_inv_act(float)  支付其他与投资活动有关的现金
         n_incr_pledge_loan(float)  质押贷款净增加额
         stot_out_inv_act(float)  投资活动现金流出小计
         n_cashflow_inv_act(float)  投资活动产生的现金流量净额
         c_recp_borrow(float)  取得借款收到的现金
         proc_issue_bonds(float)  发行债券收到的现金
         oth_cash_recp_ral_fnc_act(float)  收到其他与筹资活动有关的现金
         stot_cash_in_fnc_act(float)  筹资活动现金流入小计
         free_cashflow(float)  企业自由现金流量
         c_prepay_amt_borr(float)  偿还债务支付的现金
         c_pay_dist_dpcp_int_exp(float)  分配股利、利润或偿付利息支付的现金
         incl_dvd_profit_paid_sc_ms(float)  其中:子公司支付给少数股东的股利、利润
         oth_cashpay_ral_fnc_act(float)  支付其他与筹资活动有关的现金
         stot_cashout_fnc_act(float)  筹资活动现金流出小计
         n_cash_flows_fnc_act(float)  筹资活动产生的现金流量净额
         eff_fx_flu_cash(float)  汇率变动对现金的影响
         n_incr_cash_cash_equ(float)  现金及现金等价物净增加额
         c_cash_equ_beg_period(float)  期初现金及现金等价物余额
         c_cash_equ_end_period(float)  期末现金及现金等价物余额
         c_recp_cap_contrib(float)  吸收投资收到的现金
         incl_cash_rec_saims(float)  其中:子公司吸收少数股东投资收到的现金
         uncon_invest_loss(float)  未确认投资损失
         prov_depr_assets(float)  加:资产减值准备
         depr_fa_coga_dpba(float)  固定资产折旧、油气资产折耗、生产性生物资产折旧
         amort_intang_assets(float)  无形资产摊销
         lt_amort_deferred_exp(float)  长期待摊费用摊销
         decr_deferred_exp(float)  待摊费用减少
         incr_acc_exp(float)  预提费用增加
         loss_disp_fiolta(float)  处置固定、无形资产和其他长期资产的损失
         loss_scr_fa(float)  固定资产报废损失
         loss_fv_chg(float)  公允价值变动损失
         invest_loss(float)  投资损失
         decr_def_inc_tax_assets(float)  递延所得税资产减少
         incr_def_inc_tax_liab(float)  递延所得税负债增加
         decr_inventories(float)  存货的减少
         decr_oper_payable(float)  经营性应收项目的减少
         incr_oper_payable(float)  经营性应付项目的增加
         others(float)  其他
         im_net_cashflow_oper_act(float)  经营活动产生的现金流量净额(间接法)
         conv_debt_into_cap(float)  债务转为资本
         conv_copbonds_due_within_1y(float)  一年内到期的可转换公司债券
         fa_fnc_leases(float)  融资租入固定资产
         im_n_incr_cash_equ(float)  现金及现金等价物净增加额(间接法)
         net_dism_capital_add(float)  拆出资金净增加额
         net_cash_rece_sec(float)  代理买卖证券收到的现金净额(元)
         credit_impa_loss(float)  信用减值损失
         use_right_asset_dep(float)  使用权资产折旧
         oth_loss_asset(float)  其他资产减值损失
         end_bal_cash(float)  现金的期末余额
         beg_bal_cash(float)  减:现金的期初余额
         end_bal_cash_equ(float)  加:现金等价物的期末余额
         beg_bal_cash_equ(float)  减:现金等价物的期初余额
         update_flag(str)  更新标志
        
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
            "ann_date": "",
            "f_ann_date": "",
            "start_date": "",
            "end_date": "",
            "period": "",
            "report_type": "",
            "comp_type": "",
            "end_type": "",
            "is_calc": "",
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
            logger.debug("Invoke pro.cashflow_vip with args: {}".format(kwargs))
            res = self.tushare_api().cashflow_vip(**kwargs, fields=self.entity_fields)
            res.to_sql('tushare_cashflow_vip', con=engine, if_exists='append', index=False, index_label=['ts_code'])
            return res

        df = fetch_save(offset)
        offset += df.shape[0]
        while kwargs['limit'] != "" and str(df.shape[0]) == kwargs['limit']:
            df = fetch_save(offset)
            offset += df.shape[0]
        return offset - init_offset


setattr(CashflowVip, 'default_limit', default_limit_ext)
setattr(CashflowVip, 'default_order_by', default_order_by_ext)
setattr(CashflowVip, 'prepare', prepare_ext)
setattr(CashflowVip, 'tushare_parameters', tushare_parameters_ext)
setattr(CashflowVip, 'param_loop_process', param_loop_process_ext)

if __name__ == '__main__':
    pd.set_option('display.max_columns', 500)    # 显示列数
    pd.set_option('display.width', 1000)
    logger.setLevel(logging.INFO)
    api = CashflowVip()
    api.process(ProcessType.HISTORY)    # 同步历史数据
    # api.process(ProcessType.INCREASE)  # 同步增量数据
    print(api.cashflow_vip())    # 数据查询接口
