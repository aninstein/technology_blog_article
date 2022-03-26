#!/user/bin/env python
# -*- coding: utf-8 -*-

import traceback
import json

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
from flask_babel import Babel
from flask import request


babel = Babel()


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['zh', 'en'])


def consumer_demo():
    consumer = KafkaConsumer(
        'kafka_demo',
        bootstrap_servers=':9092',
        group_id='test'
    )
    for message in consumer:
        print("receive, key: {}, value: {}".format(
            json.loads(message.key.decode()),
            json.loads(message.value.decode())
            )
        )


if __name__ == '__main__':
    consumer_demo()
