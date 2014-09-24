from weibo import APIClient

class pachong:
    def __init__(self,appkey,appsecret,callbackurl,accesstoken,expin):
        self.client=APIClient(app_key=appkey,app_secret=appsecret)
        self.client.set_access_token(accesstoken,expin)


    def printcurrentuser(self):
        print self.client.statuses.user_timeline.get()

    def printuserwithname(self,name):
        statuses=self.client.statuses.user_timeline.get(screen_name=name)
        for s in statuses[u"statuses"]:
            print s[u"text"]
    
    def ShowUserInformation(self,name):
        print self.client.users.show.get(screen_name=name)

    def ShowUserList(self,name):
        a=self.client.friendships.followers.ids.get(screen_name=name)
        for i in a[u'ids']:
            print i

    def ShowUserFriends(self,name):
        print self.client.friendships.friends.get(screen_name=name)


















if __name__=="__main__":
    Appkey="3423280349"
    Appsecret="1f74f37b71c5ca2e0faadc41129d516a"
    callbackurl="http://www.baidu.com"
    ack="2.00pVrsKC3mz1gE840b5f298788d81D"
    expin="7801776"

    p=pachong(Appkey,Appsecret,callbackurl,ack,expin)
   # p.printcurrentuser()
   # p.printuserwithname(u"")
   # p.ShowUserInformation(u"Fencingworld")
    #p.ShowUserList(u"Fencingworld")
  #  p.ShowUserFriends(u"Fencingworld")
