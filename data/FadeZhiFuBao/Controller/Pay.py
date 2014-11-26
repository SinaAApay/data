import pymongo
import web
con=pymongo.Connection("localhost",27017)
bank=con.bank
accounts=bank.accounts
render=web.template.render("/home/rw/workplace/aapay/data/FadeZhiFuBao/template")
class ShowPayPage:
    def GET(self):
        webinput=web.input()
        money=webinput[u'money']
        account=webinput[u'account']
        return render.simuAli(money,account) 


class Pay:
    def POST(self):
        webinput=web.input()
        money=float(webinput[u'money'])
        addaccount=accounts.find_one({u'account':webinput[u'addaccount']})
        moneyadd=addaccount[u'money']+money
        accounts.update({u'account':addaccount},{"$set":{u'money':moneyadd}})
        subaccount=accounts.find_one({u'account':webinput[u'subaccount']})
        moneysub=subaccount[u'money']-money
        accounts.update({u'account':subaccount},{"$set":{u'money':moneysub}})
        web.seeother("http://0.0.0.0:8080/payed")
        
