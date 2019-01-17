import os
from socket import inet_aton
import struct

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
#domain = 'github.com'   #github
#domain = 'api.dialogflow.com'   #dialogflow api
#domain = 'https://ssh.cloud.google.com/wc/channel?gsessionid=XtpixrlBZVJMxzOJ1IzL3thQA77S8XNP&VER=8&RID=rpc&SID=hmhyNaI1LM3KbMfBOjhzgw&CI=0&AID=0&TYPE=xmlhttp&zx=u46i8gu6zsgv&t=2'
# domain = 'conda.anaconda.org'
# domain = 'speech.googleapis.com'
# 정보보호팀에서 클라우드 쉘 접속 시 막힌 도메인이 이거라고함.
# domain = 'status.cloud.google.com'
#domain = 'cloud.google.com'
# Google STT 인증 시 oauth2.googleapis.com 443 사용
#domain = 'oauth2.googleapis.com'

def sort_list_print():
    ip_hashset.remove('')
    list_of_ips = list(ip_hashset)
    sort_ip = sorted(list_of_ips, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])

    print('list_of_ips ; ', list_of_ips)
    print(sort_ip)

    print('====================== result_ip =======================')
    for result_ip in sort_ip:
        print(result_ip)

for i in range(5000):
    ipAddr = getIpAddr(domain)
    print('ipAddr : ', ipAddr)
    appendHashSet(ipAddr)

print('ip_hashset : ', ip_hashset)
sort_list_print()