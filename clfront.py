import socket
import ipcalc,re
import threading


bg=''

G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'


ipranges={"CLOUDFRONT_GLOBAL_IP_LIST": ["52.85.96.0/24"] }
 
 
frstarray=ipranges["CLOUDFRONT_GLOBAL_IP_LIST"]
secondarray=ipranges["CLOUDFRONT_REGIONAL_EDGE_IP_LIST"]
	

def scanner(host):
	sock=socket.socket()
	sock.settimeout(5)
	try:
		sock.connect((str(host),80))
		payload='GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(host)
		sock.send(payload.encode())
		response=sock.recv(1024).decode('utf-8','ignore')
		for data in response.split('\r\n'):
			data=data.split(':')
			if re.match(r'HTTP/\d(\.\d)?' ,data[0]):
				print('response status : {}{}{}'.format(O,data[0],GR))
			if data[0]=='Server':
				try:
					if data[1] ==' CloudFront':
						print('{}server : {}\nFound working {}..'.format(G,host,GR))
						with open('wrCloudfrontIp.txt','a') as fl:
							fl.write(str(host)+'\n')
							fl.close()
				except Exception as e:
					print(e)
	except Exception as e:print(e)

def Main():
	for k,v in ipranges.items():
		print('{',k,' : ',v,'}',end='\n')
	dicts=[frstarray,secondarray]
	choose = int(input('enter dict number of cloudront ipranges (1/2) : '.title()))-1
	cidrs_list = dicts[choose]
	for cidr in cidrs_list:
			iprange=[]
			for ip in ipcalc.Network(cidr):
				iprange.append(ip)
			for index in range(len(iprange)):			
					try:
						print("{}[INFO] Probing... ({}/{}) [{}]{}".format(
						R,index+1,len(iprange),iprange[index],GR))
						sc=threading.Thread(target=scanner,args=(iprange[index],))
						sc.start()
					except KeyboardInterrupt:
						print('{}Scan aborted by user!{}'.format(R,GR))
						break
Main()				
