
# coding: utf-8

# In[ ]:


import socket as mysoc
class RSserver:
    RS_Table={}
    #NSkey=""
    entry=""
    #self refers to the instance of RSserver being created with init
    def __init__(self,hostname,address,flag):
        self.hostname=hostname
        self.address=address
        self.flag=flag
        RSserver.RS_Table[hostname]=self
        
    #read file and populate DNS_Table
with open ('PROJ2-DNSRS.txt','r') as input_file:
    for line in input_file:
        words=(line.strip()).split() 
        entry=RSserver(words[0],words[1],words[2])
        if words[2]=="NS":
            NSkey=words[0]        
try: 
    rssd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("RSserver socket created")
except mysoc.error as err:
    print('[RS]: {} \n'.format("RSserver socket open error ",err))

try: 
    edusd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("EDUserver socket created")
except mysoc.error as err:
    print('[EDU]: {} \n'.format("EDUserver socket open error ",err))   
#connect to EDUserver running in same network as RSserver
edu_ip=mysoc.gethostbyname(mysoc.gethostname())
eduserver_binding=(edu_ip,51625)
edusd.connect(eduserver_binding)

try: 
    comsd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("COMserver socket created")
except mysoc.error as err:
    print('[COM]: {} \n'.format("COMserver socket open error ",err))
#connect to COMserver running on grep.cs.rutgers.edu
com_ip=mysoc.gethostbyname('grep.cs.rutgers.edu')
comserver_binding=(com_ip,56871)
comsd.connect(comserver_binding)

#determine local hostname, IP, select a port number
port=52171
#RS_host =mysoc.gethostbyname(mysoc.gethostname())
RSserver_binding=('', port)
rssd.bind(RSserver_binding)
rssd.listen(1)
crsd,addr=rssd.accept()
while True:
    hnstring=crsd.recv(100).decode('utf-8').strip(' \t\r\n\0')
    strr=hnstring
    if not strr:
        break
    if strr in RSserver.RS_Table and strr:
        entry=strr+ " "+RSserver.RS_Table[strr].address + " "+RSserver.RS_Table[strr].flag
    if strr not in RSserver.RS_Table and strr:
        #check .com or .edu. if .com, connect to comserver. If neither .com nor .edu, return error to client
        if ".com"in strr:
            comsd.send(strr.encode('utf-8'))
            entry=comsd.recv(100).decode('utf-8')    
        elif ".edu"in strr:
            edusd.send(strr.encode('utf-8'))
            entry=edusd.recv(100).decode('utf-8')
        else:
            entry="Error: HOST NOT FOUND"
    if strr:
        crsd.send(entry.encode('utf-8')) 

rssd.close()
exit()

