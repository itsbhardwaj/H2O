import tornado.ioloop
import tornado.web
import motor.motor_tornado
import nest_asyncio
import os.path
import json
from bson import json_util
from tornado import gen
from datetime import datetime

nest_asyncio.apply()
class Home(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class Feedback(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        result = []
        cursor = collection.find()
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            result.append(document)
        self.write(json.dumps({'data': result[::-1]}, default=json_util.default))
        self.finish()

    def post(self):
        name = self.get_argument('name')
        feedback = self.get_argument('feedback')
        def getTime(now):
            return str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " " + str(now.day) + "/" + str(now.month)  + "/" + str(now.year)
        async def do_insert():
            document = {'name': name, 'feedback': feedback, 'created_date': getTime(datetime.now())}
            result = await collection.insert_one(document)
            print('result %s' % repr(result.inserted_id))
        tornado.ioloop.IOLoop.current().run_sync(do_insert)
        
client = motor.motor_tornado.MotorClient('localhost', 27017)
database = client['H2O']
collection = database['feedback']

settings = dict(
        db=database,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )

application = tornado.web.Application({
        (r"/", Home),
        (r"/feedback", Feedback)
    }, **settings)

if __name__ == "__main__":
    print("server listening to port 8888 ...")
    print("press ctrl+c to stop")
    application.listen(8888)
    try:
        tornado.ioloop.IOLoop.current().start()
    except:
        print("server closed")
