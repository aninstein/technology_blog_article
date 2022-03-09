#!/user/bin/env python
# -*- coding: utf-8 -*-
import json
import pika
import datetime


# 生成消息入口处
def get_message():
    for i in range(5000):
        message = json.dumps(
            {'id': "10000%s" % i, "amount": 100 * i, "name": "tony", "createtime": str(datetime.datetime.now())})
        producter_fanout(message)


def producter_fanout(messages):
    # 获取与rabbitmq 服务的连接，虚拟队列需要指定参数 virtual_host，如果是默认的可以不填（默认为/)，也可以自己创建一个
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=pika.PlainCredentials('guest', 'guest')))
    # 创建一个 AMQP 信道（Channel）
    channel = connection.channel()
    # 声明exchange名为tony_test的交换机，如不存在，则创建。type=fanout表示所有消息都可以送达到所有的queue中.durable = True 代表exchange持久化存储
    channel.exchange_declare(exchange='tony_test', exchange_type='fanout', durable=True)
    # 向exchange名为tony_test的交换机， routing_key 不需要配置，body是要处理的消息，delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。
    print(messages)
    channel.basic_publish(exchange='tony_test', routing_key='', body=messages,
                          properties=pika.BasicProperties(delivery_mode=2))
    # 关闭与rabbitmq的连接
    connection.close()


if __name__ == "__main__":
    get_message()