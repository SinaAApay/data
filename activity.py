import web
import pymongo
import code

render=web.template.render('static')
con=pymongo.Connection('localhost',27017)
db=con.aapay
activities=db.activities
users=db.users

class currentActivity:
    def GET(self):
        cookie=web.cookies()
        activityIn=[]
        activityORG=[]
        uid=int(cookie[u'uid'])
        user=users.find_one({'uid':uid})
        for ac in user[u'activities']:
            print ac
            a_activity=activities.find_one({u'weibo_id':ac})
            print a_activity
            activityORG.append(a_activity)

        return "currentActivity"
