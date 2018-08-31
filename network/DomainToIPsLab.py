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
# domain = 'ssh.cloud.google.com'
# domain = 'conda.anaconda.org'
# domain = 'speech.googleapis.com'
# 정보보호팀에서 클라우드 쉘 접속 시 막힌 도메인이 이거라고함.
# domain = 'status.cloud.google.com'
#domain = 'cloud.google.com'
# Google STT 인증 시 oauth2.googleapis.com 443 사용
domain = 'oauth2.googleapis.com'


for i in range(5000):
    ipAddr = getIpAddr(domain)
    print('ipAddr : ', ipAddr)
    appendHashSet(ipAddr)

print('ip_hashset : ', ip_hashset)