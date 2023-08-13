import logging
import time
from concurrent.futures import ThreadPoolExecutor

from tutake.api.process_bar import process, finish_task
from tutake.api.process_report import ProcessReport, ActionResult, ProcessException, ProcessReportContainer, \
    CriticalException


class DataProcess:
    """
    获取保存数据的核心类，用以实现获取数据到保存数据的过程，封装了中间的限流、异常、重试、日志、多线程等的一些处理步骤，每个具体的接口都继承这个类，
    在每个具体的实现类中实现获取数据和保存的具体操作
    """

    def __init__(self, name, config):
        self.logger = logging.getLogger('api.tushare.%s' % name)
        self.name = name
        self._report_container = ProcessReportContainer(config)
        self.config = config
        self.max_repeat = config.get_config("tutake.process.max_repeat", 3)

    def name(self):
        return self.name

    def process(self):
        pass

    def api_token_limit(self) -> (int, int):
        """
        接口的限制
        :return: （最小的积分，接口限流）
        """
        return ()

    def prepare(self):
        """
        同步历史数据准备工作
        """

    def query_parameters(self):
        """
        同步历史数据调用的参数
        :return: list(dict)
        """
        return [{}]

    def param_loop_process(self, **params):
        """
        每执行一次fetch_and_append前，做一次参数的处理，如果返回None就中断这次执行
        """
        return params

    def _process(self, fetch_and_append) -> ProcessReport:
        """
        同步历史数据
        :return:
        """
        # self.logger.info(f"Start {self.entities.__name__} process.")
        process.console.log(f"Start {self.entities.__name__} process.")
        if self.config.get_config("tutake.logger.console", False):
            report = self._report_container.create_process_report("tushare_%s" % self.name, self.name, process.console)
        else:
            report = self._report_container.create_process_report("tushare_%s" % self.name, self.name, None)
        self.prepare()
        params = self.query_parameters()
        try:
            if params:
                report.set_exec_params(params)

                def action(param) -> ActionResult:
                    start = time.time()
                    new_param = self.param_loop_process(**param)
                    if new_param is None:
                        return ActionResult(start, time.time(), param, new_param, status='Skip')
                    try:
                        append_cnt = fetch_and_append(**new_param)
                        return ActionResult(start, time.time(), param, new_param, append_cnt)
                    except ProcessException as err:
                        return ActionResult(start, time.time(), {**param, **err.param}, new_param, err=err,
                                            status='Failed')
                    except Exception as err:
                        return ActionResult(start, time.time(), param, new_param, err=err, status='Failed')

                task_id = process.add_task(description=self.name, total=len(params))
                with ThreadPoolExecutor(max_workers=self.config.get_process_thread_cnt()) as pool:
                    for result in pool.map(action, params):
                        process.advance(task_id, 1)
                        critical_failed = report.finish_task(result)
                        process.update(task_id, **report.result_summary())
                        if critical_failed:
                            process.stop_task(task_id)
                            self.logger.critical(f"Stop with critical exception. {result}")
                            return report

                    repeat_params = report.repeat()
                    retry_cnt = 0
                    while repeat_params and len(repeat_params) > 0:
                        if retry_cnt >= self.max_repeat:
                            report = report.close("FAILED_OVER_RETRY")
                            raise CriticalException(
                                f"Retry execute {self.name} times is than {self.max_repeat}, check it pls!")
                        process.update(task_id, description=self.name + "[R]", completed=0, total=len(repeat_params))
                        report.set_exec_params(repeat_params, 'Repeat')
                        for result in pool.map(action, repeat_params):
                            process.advance(task_id, 1)
                            report.finish_task(result)
                            process.update(task_id, **report.result_summary())
                        repeat_params = report.repeat()
                        retry_cnt += 1
                finish_task(task_id)
            report = report.close()
        except Exception as err:
            logging.error(err)
        process.console.log(
            f"Finished {self.entities.__name__} process with status: {report.status}. it takes {report.process_time()}s")
        return report
