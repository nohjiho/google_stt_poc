import os

ip_hashset = set()


def getIpAddr(url):
    # window : nslookup
    # linux : host
    command = 'nslookup ' + url
    process = os.popen(command)
    results = str(process.read())
    if results.find('Addresses:') > -1:
        marker = results.find('Addresses:') + 12

        return results[marker:].splitlines()[1].replace('	', '').replace(' ', '')
    else:
        return ""


def appendHashSet(ipAddr):
    if (ipAddr in ip_hashset) == False:
        ip_hashset.add(ipAddr)
        print('ip_hashset : ', ip_hashset)

# 216.58.221.110
# ssh.cloud.google.com
# google.com
domain = 'ssh.cloud.google.com' # ip_hashset :  {'', '216.58.197.206', '172.217.26.14', '172.217.31.174', '216.58.197.142'}
#domain = 'https://ssh.cloud.google.com/wc/channel?gsessionid=XtpixrlBZVJMxzOJ1IzL3thQA77S8XNP&VER=8&RID=rpc&SID=hmhyNaI1LM3KbMfBOjhzgw&CI=0&AID=0&TYPE=xmlhttp&zx=u46i8gu6zsgv&t=2'
# domain = 'conda.anaconda.org'
# domain = 'speech.googleapis.com'
# 정보보호팀에서 클라우드 쉘 접속 시 막힌 도메인이 이거라고함.
# domain = 'status.cloud.google.com'
#domain = 'cloud.google.com'
# Google STT 인증 시 oauth2.googleapis.com 443 사용
#domain = 'oauth2.googleapis.com'


for i in range(100):
    ipAddr = getIpAddr(domain)
    print('ipAddr : ', ipAddr)
    appendHashSet(ipAddr)

print('ip_hashset : ', ip_hashset)