#!/user/bin/env python
# -*- coding: utf-8 -*-
import pika
import random
from multiprocessing import Pool
import os


# 接收消息，并写入文件
def write_file(message):
    with open("msg00.txt", "a+") as f:
        print(message)
        f.write(message)


def consumer_fanout(i):
    # 获取与rabbitmq 服务的连接
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=pika.PlainCredentials('guest', 'guest')))
    # 创建一个 AMQP 信道（Channel）
    channel = connection.channel()
    # 声明exchange名为tony_test的交换机，如不存在，则创建。type=fanout表示所有消息都可以送达到所有的queue中.durable = True 代表exchange持久化存储
    channel.exchange_declare(exchange='tony_test', exchange_type='fanout', durable=True)
    # 随机创建一个队列名称
    # queuename = "tester" + str(random.randrange(10, 1000))
    queuename = "tester" + str(i)
    result = channel.queue_declare(queue=queuename)
    # 将exchange 与queue 进行绑定
    channel.queue_bind(exchange='test', queue=queuename)

    # 定义回调处理消息的函数
    def callback(ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(body.decode)
        print("queuename =", queuename)
        print("process id =", os.getpid())
        write_file(body.decode())

    # 告诉rabbitmq，用callback来接收并处理消息
    channel.basic_consume(result.method.queue, callback, False)
    # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
    channel.start_consuming()


if __name__ == "__main__":
    pool = Pool(processes=5)
    for i in range(5):
        pool.apply_async(consumer_fanout, (i, ))
    pool.close()
    pool.join()