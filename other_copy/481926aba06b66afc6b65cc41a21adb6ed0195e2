from __future__ import absolute_import, unicode_literals

import psycopg2
import redis
import re
from celery import Celery, Task, platforms
from pymongo import MongoClient, errors

import conf


class ConnectionTask(Task):
    abstract = True

    def __init__(self):
        self._testmdb = None
        self._dmdb = None
        self._dmdb_ctrip = None
        self._smdb = None
        self._pmdb = None
        self._static = None
        self._static_cluster = None
        self._static_cluster_ctrip = None
        self._static_ctrip = None
        self._prrdb={}
        self._drdb_mast = {}
        self._drdb_paym = {}
        self._drdb_new = {}
        self._srdb_mast = {}
        self._srdb_new = {}
        self._dpprdb = {}
        self._prdb_mast = {}
        self._prdb_paym = {}
        self._prdb_activity = {}
        self._dpgdb = {}
        self._spgdb = {}
        self._ppgdb = {}
    @property
    def testmdb(self):
        if self._testmdb is None:
            _mc = MongoClient("mongodb://root:Boluome123@139.198.191.20:17017")
            self._testmdb = _mc['boluome']
        return self._testmdb
    
    @property
    def dmdb(self):
        if self._dmdb is None:
            _mc = MongoClient(conf.DEV_MONGO_HOST, replicaset=conf.REPLICASET_NAME)
            self._dmdb = _mc['boluome']
        return self._dmdb

    @property
    def dmdb_ctrip(self):
        if self._dmdb_ctrip is None:
            _mc = MongoClient(conf.CTRIP_MONGO_HOST)
            self._dmdb_ctrip = _mc['ctrip']
        return self._dmdb_ctrip

    @property
    def smdb(self):
        if self._smdb is None:
            _mc = MongoClient(conf.STG_MONGO_HOST, replicaset=conf.REPLICASET_NAME)
            self._smdb = _mc['boluome']
        return self._smdb

    @property
    def pmdb(self):
        if self._pmdb is None:
            _mc = MongoClient(conf.PRO_MONGO_HOST, replicaset=conf.REPLICASET_NAME)
            self._pmdb = _mc['boluome']
        return self._pmdb

    @property
    def static(self):
        if self._static is None:
            _mc = MongoClient(conf.STATIC_MONGO_HOST, replicaset=conf.REPLICASET_NAME)
            self._static = _mc['boluome']
        return self._static

    @property
    def static_cluster(self):
        if self._static_cluster is None:
            _mc = MongoClient('mongodb://root:Boluome123@staticmongo-m.localdomain,staticmongo-s1.localdomain,staticmongo-s2.localdomain/?authSource=admin&readPreference=secondaryPreferred')
            self._static_cluster = _mc['boluome']
        return self._static_cluster
    
    @property
    def static_cluster_ctrip(self):
        if self._static_cluster_ctrip is None:
            _mc = MongoClient('mongodb://root:Boluome123@staticmongo-m.localdomain,staticmongo-s1.localdomain,staticmongo-s2.localdomain/?authSource=admin&readPreference=secondaryPreferred')
            self._static_cluster_ctrip = _mc['ctrip']
        return self._static_cluster_ctrip
    
    @property
    def static_ctrip(self):
        if self._static_ctrip is None:
            _mc = MongoClient(conf.STATIC_MONGO_HOST, replicaset=conf.REPLICASET_NAME)
            self._static_ctrip = _mc['ctrip']
        return self._static_ctrip

    def prrdb(self, db):
        if self._prrdb.get(db) is None:
            self._prrdb[db] = redis.StrictRedis(host='rrdb.localdomain',
                                                     port='16379',
                                                     db=db,
                                                     encoding='utf-8',
                                                     decode_responses=True)
        return self._prrdb[db]
    
    def drdb_mast(self, db):
        if self._drdb_mast.get(db) is None:
            self._drdb_mast[db] = redis.StrictRedis(host=conf.DEV_REDIS_MAST_HOST,
                                                    port=conf.REDIS_PORT,
                                                    db=db, charset="utf-8",
                                                    decode_responses=True)
        return self._drdb_mast.get(db)

    def drdb_paym(self, db):
        if self._drdb_paym.get(db) is None:
            self._drdb_paym[db] = redis.StrictRedis(host=conf.DEV_REDIS_PAYM_HOST,
                                                    port=conf.REDIS_PORT,
                                                    db=db, charset="utf-8",
                                                    decode_responses=True)
        return self._drdb_paym.get(db)

    def drdb_new(self, db):
        if self._drdb_new.get(db) is None:
            self._drdb_new[db] = redis.StrictRedis(host=conf.DEV_REDIS_NEW_HOST,
                                                   port=conf.REDIS_PORT,
                                                   db=db, charset="utf-8",
                                                   decode_responses=True)
        return self._drdb_new.get(db)

    def srdb_mast(self, db):
        if self._srdb_mast.get(db) is None:
            self._srdb_mast[db] = redis.StrictRedis(host=conf.STG_REDIS_MAST_HOST,
                                                    port=conf.REDIS_PORT,
                                                    db=db, charset="utf-8",
                                                    decode_responses=True)
        return self._srdb_mast.get(db)

    def srdb_new(self, db):
        if self._srdb_new.get(db) is None:
            self._srdb_new[db] = redis.StrictRedis(host=conf.STG_REDIS_NEW_HOST,
                                                   port=conf.REDIS_PORT,
                                                   db=db, charset="utf-8",
                                                   decode_responses=True)
        return self._srdb_new.get(db)
    
    def dpprdb(self, db):
        if self._dpprdb.get(db) is None:
            self._dpprdb[db] = redis.StrictRedis(host="dppredis.localdomain",
                                                   port=conf.REDIS_PORT,
                                                   db=db, charset="utf-8",
                                                   decode_responses=True)
        return self._dpprdb.get(db)
    
    def prdb_mast(self, db):
        if self._prdb_mast.get(db) is None:
            self._prdb_mast[db] = redis.StrictRedis(host=conf.PRO_REDIS_MAST_HOST,
                                                    port=conf.REDIS_PORT,
                                                    db=db, charset="utf-8",
                                                    decode_responses=True)
        return self._prdb_mast.get(db)

    def prdb_paym(self, db):
        if self._prdb_paym.get(db) is None:
            self._prdb_paym[db] = redis.StrictRedis(host=conf.PRO_REDIS_PAYM_HOST,
                                                    port=conf.REDIS_PORT,
                                                    db=db, charset="utf-8",
                                                    decode_responses=True)
        return self._prdb_paym.get(db)
    
    def prdb_activity(self, db):
        if self._prdb_activity.get(db) is None:
            self._prdb_activity[db] = redis.StrictRedis(host=conf.PRO_REDIS_ACTIVITY_HOST,
                                                    port=conf.REDIS_PORT,
                                                    db=db, charset="utf-8",
                                                    decode_responses=True)
        return self._prdb_activity.get(db)

    def dpgdb(self, db):
        if self._dpgdb.get(db) is None:
            self._dpgdb[db] = psycopg2.connect("host=192.168.0.8 dbname={} user=root password=Boluome123".format(db))
        # else:
        #     self._dpgdb.rollback()
        return self._dpgdb.get(db)

    def spgdb(self, db):
        if self._spgdb.get(db) is None:
            self._spgdb[db] = psycopg2.connect("host=192.168.2.10 dbname={} user=root password=Boluome123".format(db))
        # else:
        #     self._spgdb.rollback()
        return self._spgdb.get(db)

    def ppgdb(self, db):
        if self._ppgdb.get(db) is None:
            self._ppgdb[db] = psycopg2.connect('host=pg.localdomain dbname={} user=root password=Boluome123'.format(db))
        # else:
        #     self._ppgdb.rollback()
        return self._ppgdb.get(db)

    def __getitem__(self, key):
        if key in ["dmdb", "dev"]:
            return self.dmdb
        elif key in ["test"]:
            return self.testmdb
        elif key in ["dmdb_ctrip"]:
            return self.dmdb_ctrip
        elif key in ["smdb", "stg"]:
            return self.smdb
        elif key in ["pmdb", "pro"]:
            return self.pmdb
        elif key == "static":
            return self.static
        elif key == "static_ctrip":
            return self.static_ctrip
        elif key == "static_cluster":
            return self.static_cluster
        elif key == "static_cluster_ctrip":
            return self.static_cluster_ctrip
        else:
            raise KeyError


def mongo_upsert_operation(mdb, database, query, update, upsert=False):
    """
    封装mongo,update_one()操作
    mdb(Object):
    database(str):
    query(dict):
    update(dict):
    upsert(bool):
    """
    try:
        mdb[database].update_one(query, update, upsert=upsert)
    except errors.DuplicateKeyError as why:
        mongo_upsert_operation(mdb, database, query, update, upsert)
        print("DuplicateKeyError fetch and retry ok", query)
    return


def insert_sql_parse(sql):
    pattern = re.compile("\(.+?\)")
    r = re.findall(pattern, sql)
    r[0] = r[0].replace('(', '')
    r[0] = r[0].replace(')', '')
    r[0] = r[0].replace(' ', '')
    keys = r[0].split(',')
    assert len(keys) == len(r[1].split(','))
    return keys


def pg_insert(sql, data, conn):
    """
    封装PostgreSql语句之 INSERT INTO
    Args:
        sql(str):
        data(list):[{},{}]
    Returns:
        out: list of tuples
    """
    assert isinstance(sql, str)
    assert isinstance(data, list)
    assert ";" in sql
    sql = sql.replace('?', '%s')
    keys = insert_sql_parse(sql)
    conn.commit()
    conn.rollback()
    with conn.cursor() as curs:
        sql_pg = ""
        for item in data:
            value = [item.get(k) for k in keys]
            sql_pg += curs.mogrify(sql, value).decode()
        curs.execute(sql_pg)
        conn.commit()
    return


def update_sql_parse(sql):
    sql_list = sql.split(' ')
    sql_list = [v for v in sql_list if '%s' in v]
    sql_clean = ''.join(sql_list)
    sql_clean = sql_clean.replace(';', '')
    sql_clean = sql_clean.replace('=%s', ',')
    keys = [v for v in sql_clean.split(',') if v]
    assert len(keys) > 1
    return keys


def pg_update(sql, data, conn):
    """
    封装PostgreSql语句之 UPDATE
    Args:
        sql(str):
        data(list):[{},{}]
    Returns:
        out: list of tuples
    """
    assert isinstance(sql, str)
    assert isinstance(data, list)
    assert ";" in sql
    sql = sql.replace('?', '%s')
    keys = update_sql_parse(sql)
    conn.commit()
    conn.rollback()
    with conn.cursor() as curs:
        sql_pg = ""
        for item in data:
            value = [item.get(k) for k in keys]
            sql_pg += curs.mogrify(sql, value).decode()
        curs.execute(sql_pg)
        conn.commit()
    return


def pg_select(sql, conn):
    """
    封装PostgreSql语句之 SELECT
    Args:
        sql(str):
    Returns:
        out: list of dict

    datas=pg_select('SELECT key FROM boluome_settlement')
    """
    assert isinstance(sql, str)
    assert ";" in sql
    conn.commit()
    conn.rollback()
    with conn.cursor() as curs:
        curs.execute(sql)
        keys = curs.description
        data_all = curs.fetchall()
        conn.commit()
    for item in data_all:
        yield {v[0]: item[k] for k, v in enumerate(keys)}


def get_in(coll, path=None, default=None):
    """Returns a value at path in the given nested collection.
    Args:
        coll(object):
        path(str):'a.0.b.c'
    """
    if path is None:
        return coll

    for key in path.split('.'):
        try:
            if isinstance(coll, dict):
                coll = coll[key]
            elif isinstance(coll, list):
                coll = coll[int(key)]
            else:
                raise KeyError
        except (KeyError, IndexError, TypeError, ValueError):
            return default
    return coll


def iteritems(coll):
    return coll.items() if hasattr(coll, 'items') else coll


def merge_with(*dicts):
    """Merge several dicts."""
    dicts = list(dicts)
    if not dicts:
        return {}
    elif len(dicts) == 1:
        return dicts[0]

    lists = {}
    for c in dicts:
        for k, v in iteritems(c):
            lists[k] = v

    return lists
