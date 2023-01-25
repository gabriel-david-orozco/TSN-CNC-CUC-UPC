import pika
def send_message(message, queue_name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq-microservice'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print("Message sent to RabbitMQ")
    connection.close()