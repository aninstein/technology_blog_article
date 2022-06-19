# -*- utf-8 -*-
from functools import wraps

from kazoo.client import KazooClient


def check_zk(func):
    @wraps(func)
    def inner(foo_self, *args, **kwargs):
        if not foo_self.zk:
            raise RuntimeError("zk is not connect!")
        res = func(foo_self, *args, **kwargs)
        return res
    return inner


class ZKTools(object):

    def __init__(self, host, port=2181, timeout=10.0, logger=None, client_id=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.logger = logger
        self.client_id = client_id
        self.zk: KazooClient = None

    def __del__(self):
        self.close()

    def open(self):
        hosts = "{}:{}".format(self.host, self.port)
        self.zk = KazooClient(hosts=hosts,
                              timeout=self.timeout,
                              logger=self.logger,
                              client_id=self.client_id)
        self.zk.start()

    def close(self):
        self.zk.stop()

    def show_node(self, node_path=""):
        if node_path:
            nodes = self.get_node(node_path)
        else:
            nodes = self.get_all_node()
        print("zookeeper nodes %s:%s: " % (self.host, self.port))
        print(nodes)

    @check_zk
    def get_all_node(self):
        return self.zk.get_children("/")

    @check_zk
    def get_node(self, node_path, watch: callable = None):
        return self.zk.get_children(node_path, watch=watch)

    @check_zk
    def get_node_watch(self, node_path, watch: callable = None):
        return self.zk.get(node_path, watch=watch)

    @check_zk
    def add_null_node(self, node_path):
        if self.zk.exists(node_path):
            return
        self.zk.create(node_path)

    @check_zk
    def add_node(self, node_path, data: bytes = b""):
        """
        makepath是递归创建,如果不加上中间那一段，就是建立一个空的节点
        :param node_path:
        :param data:
        :return:
        """
        if self.zk.exists(node_path):
            return
        self.zk.create(node_path, data, makepath=True)

    @check_zk
    def set_node(self, node_path, data: bytes):
        self.zk.set(node_path, data)

    @check_zk
    def delete_node(self, node_path, recursive=True):
        """
        :param node_path:
        :param recursive: True是递归删除，就是无视下面的节点是否是空，都干掉，不加上的话，会提示子节点非空，删除失败
        :return:
        """
        self.zk.delete(node_path, recursive=recursive)

    @check_zk
    def delete_all_node(self):
        """
        在zookeeper的新版本支持使用deleteall递归删除
        :return:
        """
        all_nodes = self.get_all_node()
        for i in all_nodes:
            if i == "zookeeper":
                continue
            self.zk.delete('/%s' % i, recursive=True)

    @check_zk
    def exist(self, path, watch: callable):
        return self.zk.exists(path, watch)


def test_watch(event):
    """
     zookeeper 所有读操作都有设置 watch 选项（get_children() 、get() 和 exists()）。
     watch 是一个触发器，当检测到 zookeeper 有子节点变动 或者 节点value发生变动时触发。
    :param event:
    :return:
    """
    print(event)


if __name__ == '__main__':
    zk = ZKTools(host="192.168.199.88", port=2181)
    zk.open()
    zk.add_node("/lichangan/001", b"zookeeper hello world 1")
    zk.add_node("/lichangan/002", b"zookeeper hello world 2")
    zk.show_node()
    zk.close()

    zk2 = ZKTools(host="192.168.199.88", port=2182)
    zk2.open()
    data = zk2.get_node_watch("/lichangan/001", watch=test_watch)
    print(data)
    zk2.set_node("/lichangan/001", b"watch hello 1")
    data = zk2.get_node_watch("/lichangan/001", watch=test_watch)
    print(data)
    zk2.close()

    zk3 = ZKTools(host="192.168.199.88", port=2183)
    zk3.open()
    zk3.show_node()
    zk3.close()

