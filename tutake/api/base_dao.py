import logging
import pickle
import sqlite3
import threading
import time
from operator import and_
from sqlite3 import Connection

import pandas as pd
from sqlalchemy import text, create_engine
from sqlalchemy.orm import load_only, declarative_base, sessionmaker

from tutake.utils.config import TutakeConfig

Base = declarative_base()


class BaseDao(object):

    def __init__(self, engine, session_factory: sessionmaker, entities, database, table_name, query_fields,
                 entity_fields,
                 config: TutakeConfig):
        self.engine = engine
        self.entities = entities
        self.database = database
        self.session_factory: sessionmaker = session_factory
        self.table_name = table_name
        self.query_fields = query_fields
        self.entity_fields = entity_fields
        self.logger = logging.getLogger('tutake.dao.base.{}'.format(table_name))
        self.time_order = config.get_config("tutake.query.time_order")

    def columns_meta(self):
        pass

    def delete_all(self):
        self.logger.warning("Delete all data of {}".format(self.table_name))
        session = self.session_factory()
        session.query(self.entities).delete()
        session.commit()

    def delete_by(self, **kwargs):
        self.logger.warning("Delete data from {} by {}".format(self.table_name, kwargs))
        session = self.session_factory()
        session.query(self.entities).filter_by(**kwargs).delete()
        session.commit()

    def get_ident(self, ident):
        session = self.session_factory()
        return session.query(self.entities).get(ident)

    def filter(self, **params):
        session = self.session_factory()
        query = session.query(self.entities).filter_by(**params)
        return query.commit()

    def column_data(self, columns: [], *criteria):
        if criteria:
            result = self.session_factory().query(self.entities).filter(*criteria).options(load_only(*columns)).all()
        else:
            result = self.session_factory().query(self.entities).options(load_only(*columns)).all()
        vals = list({key: i.__dict__[key] for key in columns} for i in result)
        return vals

    def max(self, column: str, condition: str = ""):
        return self._single_func(column, 'max', condition)

    def min(self, column: str, condition: str = ""):
        return self._single_func(column, 'min', condition)

    def count(self, condition: str = ""):
        return self._single_func('*', 'count', condition)

    def _single_func(self, column: str, func: str, condition: str = ""):
        with self.engine.connect() as con:
            if condition.strip() == '':
                sql = 'SELECT {}({}) FROM {}'.format(func, column, self.table_name)
            else:
                sql = 'SELECT {}({}) FROM {} WHERE {}'.format(func, column, self.table_name, condition)
            rs = con.execute(sql)
            for i in rs:
                return i[0]

    def default_order_by(self) -> str:
        """
            默认的查询排序
        """
        return ''

    def default_limit(self) -> str:
        """
         每次取数的limit
        """
        return ''

    def default_time_range(self) -> ():
        return None

    def filter_process(self, filter_criterion, filter_by):
        return filter_criterion, filter_by

    def _get_time_criterion_filter(self, **kwargs):
        time_range_query = self.default_time_range()
        criterion = None
        if time_range_query:
            start = kwargs.get(time_range_query[0])
            end = kwargs.get(time_range_query[1])
            time_field = time_range_query[2]
            if start and end:
                criterion = and_(time_field >= start, time_field <= end)
            elif end:
                criterion = time_field <= end
            elif start:
                criterion = time_field >= start
        return criterion

    def _get_query_fields(self, fields=''):
        if fields != '':
            return list(getattr(self.entities, f.strip()) for f in fields.split(',') if f.strip() in self.entity_fields)
        return None

    def _get_query_limit(self, **kwargs):
        limit = 10000000  # 默认200000000条 避免导致数据库压力过大
        if kwargs.get('limit') and str(kwargs.get('limit')).isnumeric():
            input_limit = int(kwargs.get('limit'))
            if input_limit < limit:
                return input_limit
            else:
                return limit
        elif self.default_limit() != "":
            default_limit = int(self.default_limit())
            if default_limit < limit:
                return default_limit
            else:
                return limit

        return None

    def _get_query_offset(self, **kwargs):
        if kwargs.get('offset') and str(kwargs.get('offset')).isnumeric():
            return kwargs.get('offset')
        return None

    def _get_order_by(self, **kwargs):
        if kwargs.get('order_by'):
            return kwargs.get('order_by')
        order_by = self.default_order_by()
        if self.time_order:
            time_range = self.default_time_range()
            if time_range:
                time_column = time_range[2]
                if order_by:
                    tokens = order_by.split(",")
                    n_order_by = []
                    for t in tokens:
                        if t.startswith(time_column.name):
                            n_order_by.append(f"{time_column.name} {self.time_order}")
                        else:
                            n_order_by.append(t)
                    return ",".join(n_order_by)
                else:
                    return f"{time_column.name} {self.time_order}"
        else:
            return order_by

    def query(self, fields='', **kwargs):
        filter_criterion = self._get_time_criterion_filter(**kwargs)
        filter_by = {
            key: kwargs[key]
            for key in kwargs.keys()
            if key in self.query_fields and key in self.entity_fields and key is not None and kwargs[key] != ''
        }
        filter_criterion, filter_by = self.filter_process(filter_criterion, filter_by)
        order_by = self._get_order_by(**kwargs)
        limit = self._get_query_limit(**kwargs)
        offset = self._get_query_offset(**kwargs)
        return self.direct_query(fields, filter_criterion, filter_by, order_by, limit, offset)

    def direct_query(self, fields: str = None, filter_criterion=None, filter_by: dict = None,
                     order_by: str = None, limit: int = None, offset: int = None):
        start = time.time()
        query = None
        if filter_criterion is not None:
            query = self.session_factory().query(self.entities).filter(filter_criterion)
        else:
            query = self.session_factory().query(self.entities)
        if filter_by:
            if query:
                query = query.filter_by(**filter_by)
            else:
                query = self.session_factory().query(self.entities).filter_by(**filter_by)
        if fields:
            query_fields = self._get_query_fields(fields)
            query = query.with_entities(*query_fields)
        if order_by:
            query = query.order_by(text(order_by))
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        df = pd.read_sql(query.statement, query.session.bind)
        df = df.drop(['id'], axis=1, errors='ignore')
        self.logger.debug(
            "Finished {} query, it costs {}s".format(self.entities.__name__, time.time() - start))
        return df

    def sql(self, sql):
        start = time.time()
        query = self.session_factory().query(self.entities)
        sql = sql.format(table=self.table_name).strip()
        if sql.split(" ")[0].upper().startswith("SELECT"):
            df = pd.read_sql(sql, query.session.bind)
            df = df.drop(['id'], axis=1, errors='ignore')
            self.logger.debug(
                "Finished {} query, sql is {} it costs {}s".format(self.entities.__name__, sql, time.time() - start))
            return df
        return pd.DataFrame()

    def meta(self):
        return {"table_name": self.table_name, "columns": self.columns_meta(),
                "default_order_by": self.default_order_by(),
                "default_limit": self.default_limit()}

    def uniq_check(self, columns):
        group = ','.join(columns)
        sql = "select " + group + " from {table} group by " + group + "  have count(*)>1"
        return self.sql(sql)


class Records:
    def __init__(self, fields=None, items=None):
        self.fields = fields
        if items is None:
            self.items = []
        else:
            self.items = items

    def data_frame(self):
        return pd.DataFrame(self.items, columns=self.fields)

    def size(self):
        if self.items is None:
            return 0
        else:
            return len(self.items)

    def append(self, records):
        if self.fields is None:
            self.fields = records.fields
        self.items = self.items + records.items


class BatchWriter:

    def __init__(self, engine, table: str):
        self.records = Records()
        self.engine = engine
        self.table = table
        self.shared_resource_lock = threading.Lock()
        self.conn: Connection = None
        self.logger = logging.getLogger('tutake.dao.writer.{}'.format(table))
        self.database = self.engine.url.database.split("/")[-1]

    def start(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.engine.url.database)
        # self.conn.execute('''PRAGMA synchronous = OFF''')

    def rollback(self):
        if self.conn:
            self.logger.warning(f"Rollback all {self.table} records of writers.")
            self.conn.rollback()
            self.conn.close()
            self.conn = None

    def commit(self):
        if self.conn:
            self.flush()
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def add_records(self, records):
        if isinstance(records, Records):
            self.records.append(records)
            if self.records.size() > 500000:
                self.flush()

    def flush(self):
        self.shared_resource_lock.acquire()
        records = self.records
        self.records = Records()
        self.shared_resource_lock.release()
        size = records.size()
        if size > 0:
            t = time.time()
            sql = "insert or ignore into {}({}) values ({})".format(self.table, ','.join(records.fields),
                                                                    ','.join(["?" for _ in
                                                                              range(len(records.fields))]))
            if self.conn is None:
                self.start()
            self.conn.executemany(sql, records.items)

            self.logger.debug("Save {} records to table {} in {}, costs {}s".format(size, self.table,
                                                                                    self.database,
                                                                                    '%.4f' % (time.time() - t)))
