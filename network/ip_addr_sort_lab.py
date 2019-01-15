from socket import inet_aton
import struct

ip_hashset = set()
ip_hashset = {'', '172.217.161.238', '216.58.197.174', '216.58.197.206', '172.217.161.206', '172.217.25.110', '216.58.196.238'}
ip_hashset.remove('')
list_of_ips = list(ip_hashset)
sort_ip = sorted(list_of_ips, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])

print('list_of_ips ; ' , list_of_ips)
print(sort_ip)

print('====================== result_ip =======================')
for result_ip in sort_ip:
    print(result_ip)