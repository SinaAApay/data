# -*- coding:utf-8 -*-
import os,sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import web
import pymongo
from getclient import getClient
from newclass import getClientName
render=web.template.render('/home/rw/workplace/aapay/data/static')
con=pymongo.Connection('localhost',27017)
db=con.aapay
activities=db.activities
users=db.users
bank=db.bank


def refreshInformations(informations,string):
    if len(informations)<5:
        informations.append(string)
    else:
        del informations[0]
        informations.insert(4,string)
    return informations

class payonline:
    def POST(self):
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        ac=activities.find_one({u'weibo_id':weibo_id})
        hostname=ac[u'peoplePay'][0]
        ifpay=True
        for people in ac[u'peopleInvited']:
            if people in ac[u'peopleIn']:
                ifpay=True
            else:
                ifpay=False
                break
        if ifpay:
            paymoney=float(ac[u'money'])/len(ac[u'peopleIn'])
            print paymoney
            print len(ac[u'peopleIn'])
            hostacount=bank.find_one({u'name':hostname})
            hostmoney=hostacount[u'money']
            hostmoney+=paymoney
            bank.update({u"name":hostname},{"$set":{u"money":hostmoney}})
            cookies=web.cookies()
            acc=cookies[u'access_token']
            exp=cookies[u'expires_in']
            uid=cookies[u'uid']
            client=getClient(acc,exp)
            myname=getClientName(client,int(uid))
            myacount=bank.find_one({u'name':myname})
            mymoney=myacount[u'money']
            mymoney-=paymoney
            bank.update({u"name":myname},{"$set":{u"money":mymoney}})
            peoplePay=ac[u'peoplePay']
            peoplePay.append(myname)
            activities.update({u"weibo_id":weibo_id},{"$set":{u"peoplePay":peoplePay}})
        web.SeeOther("/currentActivity")
            

