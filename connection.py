__author__ = 'nahid'

from collections import namedtuple
import Queue
import random
import cql
import logging
from copy import copy
# from exceptions import PycqlException
from contextlib import contextmanager
from thrift.transport.TTransport import TTransportException


LOG = logging.getLogger('pycql.cql')
Host = namedtuple('Host', ['name', 'port', 'keyspace'])
_max_connections = 25
connection_pool = None


def setup(hosts, username=None, password=None, max_connections=25, keyspace=None):
    """
    Records the hosts and connects to one of them

    :param hosts: list of hosts, strings in the <hostname>:<port>, or just <hostname>
    """
    global _max_connections
    global connection_pool
    _max_connections = max_connections

    _hosts = []
    for host in hosts:
        host = host.strip()
        host = host.split(':')
        if len(host) == 1:
            _hosts.append(Host(host[0], 9160, keyspace))
        elif len(host) == 3:
            _hosts.append(Host(*host))
        else:
            raise CQLConnectionError("Can't parse {}".format(''.join(host)))

    if not _hosts:
        raise CQLConnectionError("At least one host required")

    connection_pool = ConnectionPool(_hosts, username, password)


class CQLConnectionError(Exception):
    pass


class ConnectionPool(object):
    """Handles pooling of database connections."""

    def __init__(self, hosts, username=None, password=None):
        self._hosts = hosts
        self._username = username
        self._password = password

        self._queue = Queue.Queue(maxsize=_max_connections)

    def clear(self):
        """
        Force the connection pool to be cleared. Will close all internal
        connections.
        """
        try:
            while not self._queue.empty():
                self._queue.get().close()
        except:
            pass

    def get(self):
        """
        Returns a usable database connection. Uses the internal queue to
        determine whether to return an existing connection or to create
        a new one.
        """
        try:
            if self._queue.empty():
                return self._create_connection()
            return self._queue.get()
        except CQLConnectionError as cqle:
            raise cqle

    def put(self, conn):
        """
        Returns a connection to the queue freeing it up for other queries to
        use.

        :param conn: The connection to be released
        :type conn: connection
        """

        if self._queue.full():
            conn.close()
        else:
            self._queue.put(conn)

    def _create_connection(self):
        """
        Creates a new connection for the connection pool.

        should only return a valid connection that it's actually connected to
        """
        if not self._hosts:
            raise CQLConnectionError("At least one host required")

        hosts = copy(self._hosts)
        random.shuffle(hosts)

        for host in hosts:
            try:
                new_conn = cql.connect(host.name, host.port, keyspace=host.keyspace, user=self._username, password=self._password)
                new_conn.set_cql_version('3.0.0')
                return new_conn
            except Exception as e:
                logging.debug("Could not establish connection to {} at {}:{}".format(host.keyspace, host.name, host.port))
                pass

        raise CQLConnectionError("Could not connect to any server in cluster")

    def execute(self, query, params):
        try:
            con = self.get()
            cur = con.cursor()
            cur.execute(query, params)
            self.put(con)
            return cur
        except cql.ProgrammingError as ex:
            raise Exception(unicode(ex))
        except TTransportException:
            pass

        raise Exception("Could not execute query against the cluster")


def execute(query, params={}):
    return connection_pool.execute(query, params)

@contextmanager
def connection_manager():
    global connection_pool
    tmp = connection_pool.get()
    yield tmp
    connection_pool.put(tmp)

