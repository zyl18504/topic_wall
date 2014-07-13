import os.path,json
import tornado.httpserver
import tornado.ioloop
import tornado.web
from topic_util import get_topic_info


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class TopicHandler(tornado.web.RequestHandler):

    def post(self):
        topic_name = self.get_argument('topic_name')
        params = locals()
        params.pop('self')
        self.render('result.html', **params)

    def check_xsrf_cookie(self):
        pass

    def get(self):
        keyword = self.get_argument("keyword")
        topic_info_list = get_topic_info(keyword)
        if not topic_info_list:
            self.write("")
        else:
            self.write(json.dumps(topic_info_list))
        return


def main():
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'debug': True,
    }
    application = tornado.web.Application([
        ('/', MainHandler),
        ('/result', TopicHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()