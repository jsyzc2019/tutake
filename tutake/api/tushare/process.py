import logging
import time
from concurrent.futures import ThreadPoolExecutor

from tutake.api.process_report import ProcessReport, ProcessType, ActionResult, ProcessException, ProcessReportContainer
from tutake.utils.config import tutake_config


class DataProcess:

    def __init__(self, name):
        self.logger = logging.getLogger(('api.tushare.%s' % name))
        self.name = name
        self._report_container = ProcessReportContainer()

    def prepare(self, process_type: ProcessType):
        """
        同步历史数据准备工作
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

    def _process(self, process_type: ProcessType, fetch_and_append) -> ProcessReport:
        """
        同步历史数据
        :return:
        """
        report = self._report_container.create_process_report("tushare_%s" % self.name, self.name, process_type,
                                                              self.logger)
        self.prepare(process_type)
        params = self.tushare_parameters(process_type)
        if params:
            report.set_exec_params(params)

            def action(param) -> ActionResult:
                start = time.time()
                new_param = self.param_loop_process(process_type, **param)
                if new_param is None:
                    return ActionResult(start, time.time(), param, new_param, status='Skip')
                try:
                    append_cnt = fetch_and_append(**new_param)
                    return ActionResult(start, time.time(), param, new_param, append_cnt)
                except Exception as err:
                    if isinstance(err.args[0], str) and (err.args[0].startswith("抱歉，您没有访问该接口的权限")
                                                         or err.args[0].startswith("抱歉，您每天最多访问该接口")):
                        return ActionResult(start, time.time(), param, new_param,
                                            err=Exception("Exit with tushare api flow limit. {}", err.args[0]),
                                            status='Failed')
                    else:
                        return ActionResult(start, time.time(), param, new_param,
                                            err=ProcessException(param=new_param, cause=err),
                                            status='Failed')

            with ThreadPoolExecutor(max_workers=tutake_config.get_process_thread_cnt()) as pool:
                for result in pool.map(action, params):
                    if report.finish_task(result):
                        self.logger.critical("Stop with critical exception. {}", result)
                        return report

                repeat_params = report.repeat()
                if repeat_params:
                    report.set_exec_params(repeat_params, 'Repeat')
                    for p in repeat_params:
                        report.finish_task(action(p))
        return report.close()
