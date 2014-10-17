import web
from code import getClient
render=web.template.render('static')


class sendweibo:
    def POST(self):
        a=web.input()
        cookie=web.cookies()
        i=cookie[u'friendscount']
        namelist=[]
        for index in range(0,int(i)):
            try:
                name=a[str(index)]
                namelist.append(name)
            except:
                continue
        
        activityMoney=a['ActivityMoney']
        activityName=a['ActivityName']
        activityTime=a['ActivityTime']
        activityPosition=a['ActivityPosition']

        moneyforeach=0.0
        moneyforeach=float(activityMoney)/(len(namelist)+1)
        print moneyforeach
        ac=cookie[u'access_token']
        exp=cookie[u'expires_in']
        uid=cookie[u'uid']
        client=getClient(ac,exp)
        status="I invite you all to a activity:"+activityName+",place:"+activityPosition+",time:"+activityTime+",money for each person:"+str(moneyforeach)+"."
        for name in namelist:
            print name
            status+=" @"+name
        print status
        try:
            client.statuses.update.post(status=status)
        except:
            web.seeother("/error")
        web.SeeOther("http://weibo.com")





        
