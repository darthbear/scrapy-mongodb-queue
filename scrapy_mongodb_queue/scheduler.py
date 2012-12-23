from scrapy.utils.reqser import request_to_dict, request_from_dict
import marshal
import pymongo
import datetime

class Scheduler(object):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, persist, queue_key, queue_order):
        self.mongodb_server = mongodb_server
        self.mongodb_port = mongodb_port
        self.mongodb_db = mongodb_db
        self.queue_key = queue_key
	self.persist = persist
	self.queue_order = queue_order

    def __len__(self):
        return self.client.size()

    @classmethod
    def from_crawler(cls, crawler):
	settings = crawler.settings
	mongodb_server = settings.get('MONGODB_QUEUE_SERVER', 'localhost')
	mongodb_port = settings.get('MONGODB_QUEUE_PORT', 27017)
	mongodb_db = settings.get('MONGODB_QUEUE_DB', 'scrapy')
        persist = settings.get('MONGODB_QUEUE_PERSIST', True)
        queue_key = settings.get('MONGODB_QUEUE_NAME', None)
        queue_type = settings.get('MONGODB_QUEUE_TYPE', 'FIFO')

	if queue_type not in ('FIFO', 'LIFO'):
	    raise Error('MONGODB_QUEUE_TYPE must be FIFO (default) or LIFO')

	if queue_type == 'LIFO':
	    queue_order = -1
	else:
	    queue_order = 1

        return cls(mongodb_server, mongodb_port, mongodb_db, persist, queue_key, queue_order)

    def open(self, spider):
        self.spider = spider
	if self.queue_key is None:
	    self.queue_key = "%s_queue"%spider.name

	connection = pymongo.Connection(self.mongodb_server, self.mongodb_port)
	self.db = connection[self.mongodb_db]
	self.collection = self.db[self.queue_key]

        # notice if there are requests already in the queue
	size = self.collection.count()
        if size > 0:
            spider.log("Resuming crawl (%d requests scheduled)" % size)

    def close(self, reason):
        if not self.persist:
            self.collection.drop()

    def enqueue_request(self, request):
	data = marshal.dumps(request_to_dict(request, self.spider))
	
	self.collection.insert({
		'data': data 
	})

    def next_request(self):
	entry = self.collection.find_and_modify(sort={"$natural":self.queue_order}, remove=True)
	if entry:
	    request = request_from_dict(marshal.loads(entry['data']), self.spider)
	    return request
	
        return None

    def has_pending_requests(self):
        return self.collection.count() > 0
