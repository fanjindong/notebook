from celery import Celery
from celery import bootsteps
from kombu import Consumer, Exchange, Queue
from kombu.async.timer import Timer
my_queue = Queue('custom', Exchange('custom'), 'routing_key')

app = Celery(broker='amqp://')


class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[my_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        counter = body["counter"]
        try:
            result = counter / (counter if counter > 0 else 0)
            print("result:", result)
        except ZeroDivisionError as why:
            body["counter"] += 1
            timer = Timer()
            timer.call_repeatedly(secs=0.1, fun=self.print_message, args=(body["counter"],), priority=10)
            # send_me_a_message("celery", who=body)
            # self.print_message(body["counter"])
        message.ack()

    def print_message(self, s):
        print(s)

app.steps['consumer'].add(MyConsumerStep)


def send_me_a_message(self, who=None, producer=None):
    with app.producer_or_acquire(producer) as producer:
        producer.publish(
            who,
            serializer='json',
            exchange=my_queue.exchange,
            routing_key=my_queue.routing_key,
            declare=[my_queue],
            retry=True,
        )

if __name__ == '__main__':
    pass
    # send_me_a_message('celery')
