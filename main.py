from julius_controller import JuliusController
import os
import tornado.ioloop
import tornado.web
import tornado.escape


PORT = 8888


class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.tmp_voice_path = 'tmp/voice.wav'
        julius_path = '%s/julius/kit/dictation-kit-v4.4/bin/osx/julius' % os.getcwd()
        self.julius_controller = JuliusController(shell_path='/bin/bash', julius_path=julius_path)
        config = '%s/julius/kit/dictation-kit-v4.4/main.jconf' % os.getcwd()
        self.julius_controller.add_config(config)
        config = '%s/julius/kit/dictation-kit-v4.4/am-gmm.jconf' % os.getcwd()
        self.julius_controller.add_config(config)
        self.julius_controller.start()

    def get(self):
        self.render('index.html')

    def post(self):
        voice = self.request.files['voice']
        with open(self.tmp_voice_path, 'wb') as f:
            f.write(voice[0]['body'])
        f.close()
        text = self.julius_controller.recognize_file(self.tmp_voice_path)
        chunk = tornado.escape.json_encode({'text': text})
        chunk = tornado.escape.utf8(chunk)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self._write_buffer.append(chunk)


application = tornado.web.Application([(r"/", MainHandler)],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
    debug=True
)

if __name__ == "__main__":
    application.listen(PORT)
    print('http://localhost:%d' % PORT)
    tornado.ioloop.IOLoop.instance().start()
