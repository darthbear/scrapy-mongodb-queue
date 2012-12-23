scrapy-mongodb-queue
====================

Use scrapy with mongodb as a queue.

The queue can be defined as a FIFO or LIFO. The order will rely on natural ordering (order of the elements on the disk, so the
queue won't be strictly ordered as a FIFO or LIFO but should be close to it).

To use it, edit settings.py and add the following line:
* SCHEDULER = "scrapy_mongodb_queue.scheduler.Scheduler"

Other options:
* MONGODB_QUEUE_SERVER: mongodb server (default: localhost)
* MONGODB_QUEUE_PORT: mongodb port (default: 27017)
* MONGODB_QUEUE_DB: mongodb db (default: scrapy)
* SCHEDULER_PERSIST: should the queue be persisted after the crawl or if the crawl is interrupted (default: True)
* SCHEDULER_QUEUE_NAME: name of the collection. By default it will be set to the name of the spider postfixed by "_queue"
* QUEUE_TYPE: can be FIFO or LIFO
