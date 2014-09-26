import os,sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import weibo

import web

urls=(
    '/index','index',
    '/hello','hello',
    )

render = web.template.render('/var/www/AA/static')
class index:
    def GET(self):
        return render.index()

class hello:
    def GET(self):
        return "hello"





app=web.application(urls,globals())
application=app.wsgifunc()

if __name__=="__main__":
    app.run()
