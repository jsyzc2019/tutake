import logging
import os.path
from os.path import dirname, abspath, join
from pathlib import Path

import yaml

from tutake.utils.logger import setup_logging
from tutake.utils.utils import project_root, file_dir, realpath


class DotConfig(dict):

    def __getattr__(self, k):
        try:
            v = self[k]
            if isinstance(v, dict):
                return DotConfig(v)
            return v
        except KeyError:
            return None

    def __getitem__(self, k):
        try:
            if isinstance(k, str) and '.' in k:
                k = k.split('.')
            if isinstance(k, (list, tuple)):
                def loop(v, kk):
                    try:
                        if len(kk) == 1 and isinstance(v, dict):
                            return v[kk[0]]
                        if isinstance(v, dict):
                            return loop(v[kk[0]], kk[1:])
                        return None
                    except KeyError or TypeError or BaseException:
                        return None

                return loop(self, k)
            return super().__getitem__(k)
        except KeyError or TypeError or BaseException:
            return None

    def get(self, k, default=None):
        try:
            v = self[k]
            if v is None:
                return default
            return v
            # if isinstance(k, str) and '.' in k:
            #     return self[k]
            # return super().get(k, default=default)
        except KeyError or TypeError:
            return default

    def set(self, key, val):
        def __set(_c, k, v):
            if isinstance(k, str) and '.' in k:
                k = k.split('.')
            if isinstance(k, (list, tuple)):
                item = _c.get(k[0])
                if item is None:
                    item = {}
                    _c[k[0]] = item
                if isinstance(item, dict):
                    k_list = k[1:]
                    if len(k_list) == 1:
                        k_list = k_list[0]
                    return __set(item, k_list, v)
                else:
                    return False
            _c[k] = v
            return True

        return __set(self, key, val)


TUTAKE_SQLITE_DRIVER_URL_KEY = "tutake.data.driver_url"
TUTAKE_DATA_DIR_KEY = "tutake.data.dir"
TUTAKE_DATA_SERVER_KEY = "tutake.data.server"
TUSHARE_TOKEN_KEY = "tushare.token"
TUSHARE_TOKENS_KEY = "tushare.tokens"
DEFAULT_TUSHARE_TOKEN = "4907b8834a0cecb6af0613e29bf71847206c41ddc3e598b9a25a0203"  # 网上随机找的，兜底程序一定可用
TUSHARE_META_DRIVER_URL_KEY = "tushare.meta.driver_url"
TUSHARE_META_DIR_KEY = "tushare.meta.dir"
TUTAKE_PROCESS_THREAD_CNT_KEY = 'tutake.process.thread_cnt'
TUTAKE_LOGGING_CONFIG_KEY = 'tutake.logger.config_file'
TUTAKE_SCHEDULER_CONFIG_KEY = 'tutake.scheduler'
TUTAKE_SQLITE_TIMEOUT_CONFIG_KEY = 'tutake.sqlite.timeout'


class TutakeConfig(object):

    def __init__(self, config_file):
        if config_file and os.path.isdir(config_file):
            config_file = f'{config_file}/config.yml'
        if config_file and not os.path.exists(config_file):
            config_file = f'{project_root()}/config.yml'
            if os.path.exists(config_file):
                print(f"Tutake config file is None or not exists. use default configfile. {config_file}")
            else:
                raise Exception(f"Tutake config file is None or not exists. pls set it.")
        self.config_file = config_file
        self.__config = self._load_config_file(self.config_file)
        self._default_config()
        self._sqlite_client = None

    def _default_config(self):
        """
        确认必须的配置项
        :return:
        """
        data_dir = realpath(self.get_config(TUTAKE_DATA_DIR_KEY) or self._get_default_data_dir('data'))
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.set_tutake_data_dir(data_dir)

        meta_dir = realpath(self.get_config(TUSHARE_META_DIR_KEY) or self._get_default_data_dir('meta'))
        if not os.path.exists(meta_dir):
            os.makedirs(meta_dir)
        self.set_tutake_meta_dir(meta_dir)

        self.logger_config_file = self._get_logger_config()
        if self.logger_config_file:
            setup_logging(self.logger_config_file)

        logging.getLogger("tutake.config").debug("Set default config. {}".format(self))

    def __str__(self):
        return f"ConfigFile: {self.config_file}" \
               f"\n\t{TUTAKE_SQLITE_DRIVER_URL_KEY}:\t{self.get_config(TUTAKE_SQLITE_DRIVER_URL_KEY)}" \
               f"\n\t{TUSHARE_TOKEN_KEY}:\t{self.get_tushare_token()}" \
               f"\n\t{TUTAKE_PROCESS_THREAD_CNT_KEY}:\t{self.get_process_thread_cnt()}" \
               f"\n\t{TUTAKE_LOGGING_CONFIG_KEY}:\t{self.logger_config_file}" \
               f"\n\t{TUTAKE_SCHEDULER_CONFIG_KEY}:\t{self.get_config(TUTAKE_SCHEDULER_CONFIG_KEY)}"

    def _load_config_file(self, config_file: str) -> DotConfig:
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf8') as stream:
                return DotConfig(yaml.safe_load(stream))
        else:
            print("Config file is not exits. %s" % config_file)
        return DotConfig()

    def merge_config(self, **_config):
        if _config is not None:
            for key in _config:
                new_key = key.replace("_", ".")
                self.set_config(new_key, _config[key])

    def require_config(self, key: str):
        config = self.get_config(key)
        if config is None:
            raise Exception("Missing required config with key %s" % key)
        return config

    def get_config(self, key: str, default_val=None):
        if key is not None:
            val = self.__config.get(key)
            if val is None:
                return default_val
            else:
                return val
        else:
            return default_val

    def set_config(self, key, val) -> True:
        return self.__config.set(key, val)

    def set_tutake_data_dir(self, _dir=None):
        if _dir:
            self.set_config(TUTAKE_SQLITE_DRIVER_URL_KEY, self._get_default_driver_url(_dir))

    def set_tutake_meta_dir(self, _dir=None):
        if _dir:
            self.set_config(TUSHARE_META_DRIVER_URL_KEY, self._get_default_driver_url(_dir))

    def _get_default_data_dir(self, dir_name):
        db_name = 'tushare_stock_basic.db'
        if dir_name == 'meta':
            db_name = 'tushare_meta.db'
        _dir = "%s/%s" % (dirname(self.config_file), dir_name)
        if os.path.exists("%s/%s" % (_dir, db_name)):
            return _dir
        else:
            return "%s/%s" % (Path.home(), '.tutake')

    def _get_default_driver_url(self, path, sub_dir=None):
        if path is None:
            path = "%s/.tutake" % Path.home()
        if sub_dir:
            path = "%s/%s" % (path, sub_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.expanduser(path)
        return f'sqlite:///{path}'

    @staticmethod
    def __set(config: DotConfig, k, v):
        return config.set(k, v)

    def get_sqlite_client(self):
        if self._sqlite_client is not None:
            return self._sqlite_client
        if self.get_config(TUTAKE_DATA_SERVER_KEY, None) is not None:
            try:
                from tutake.remote.client import SQLiteClient
                self._sqlite_client = SQLiteClient(self.get_config(TUTAKE_DATA_SERVER_KEY))
                return self._sqlite_client
            except:
                return None
        return None

    def is_read_only(self):
        return self.get_sqlite_client() is not None

    def get_sqlite_timeout(self):
        return self.get_config(TUTAKE_SQLITE_TIMEOUT_CONFIG_KEY, 5)

    def get_data_sqlite_driver_url(self, data_file=None):
        url = self.require_config(TUTAKE_SQLITE_DRIVER_URL_KEY)
        if not data_file:
            return url
        if os.name == 'nt':
            return f"{url}{os.sep}{data_file}".replace("\\", "\\\\")
        else:
            return f"{url}{os.sep}{data_file}"

    def get_meta_sqlite_driver_url(self):
        return self.require_config(TUSHARE_META_DRIVER_URL_KEY)

    def set_tushare_token(self, tushare_token):
        if tushare_token:
            self.set_config(TUSHARE_TOKEN_KEY, tushare_token)

    def get_tushare_token(self):
        token = self.get_config(TUSHARE_TOKEN_KEY)
        if token is None:
            tokens = self.get_config(TUSHARE_TOKENS_KEY)
            if tokens:
                return tokens[next(iter(tokens))][0]
        return token

    def _get_logger_config(self):
        logger_config_path = self.get_config(TUTAKE_LOGGING_CONFIG_KEY)
        if logger_config_path and not os.path.isabs(logger_config_path):
            # 如果日志配置文件是相对路径，转换成绝对路径
            logger_config_path = join(abspath(dirname(self.config_file)), logger_config_path)
        if not logger_config_path or not os.path.exists(logger_config_path):
            logging.warning(
                f"Logger config file is not config or not exists. {logger_config_path}")
            logger_config_path = f"{file_dir(__file__)}/ts_logger.yml"
            logging.warning(f"Use default logger config: {logger_config_path}")
        return logger_config_path

    def get_process_thread_cnt(self):
        return self.get_config(TUTAKE_PROCESS_THREAD_CNT_KEY, 4)
