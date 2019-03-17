
# coding: utf-8

# In[ ]:


import socket as mysoc
#.com server
class COMserver():
    #create DNS_Table
    COM_Table={}
    entry=""
    #read file and populate DNS_Table
    def __init__(self,hostname,address,flag):
        self.hostname=hostname
        self.address=address
        self.flag=flag
        COMserver.COM_Table[hostname]=self
        
with open ('PROJ2-DNSCOM.txt','r') as input_file:
    for line in input_file:
        words=(line.strip()).split() 
        entryTable=COMserver(words[0],words[1],words[2])            
try: 
    comsd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("COMserver socket created")
except mysoc.error as err:
    print('[TS]: {} \n'.format("socket open error ",err))
             
port = 56871 
COMserver_binding=("", port)
comsd.bind(COMserver_binding)
comsd.listen(1)
ctsd, addr=comsd.accept()
while True:
    hnstring=ctsd.recv(100).decode('utf-8').strip(' \t\r\n\0')
    strr=hnstring
    if not strr:
        break
    if strr in COMserver.COM_Table and strr:
        entry=strr+ " "+COMserver.COM_Table[strr].address + " "+COMserver.COM_Table[strr].flag
    if strr not in COMserver.COM_Table and strr:
        entry= "Error: HOST NOT FOUND"
    if strr:
        ctsd.send(entry.encode('utf-8')) 

comsd.close()
exit() 

