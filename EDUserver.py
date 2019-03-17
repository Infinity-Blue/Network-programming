
# coding: utf-8

# In[ ]:


import socket as mysoc
#.edu server
class EDUserver():
    #create DNS_Table
    EDU_Table={}
    entry=""
    #read file and populate DNS_Table
    def __init__(self,hostname,address,flag):
        self.hostname=hostname
        self.address=address
        self.flag=flag
        EDUserver.EDU_Table[hostname]=self
        
with open ('PROJ2-DNSEDU.txt','r') as input_file:
    for line in input_file:
        words=(line.strip()).split() 
        entryTable=EDUserver(words[0],words[1],words[2])            
try: 
    edusd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("EDU server socket created")
except mysoc.error as err:
    print('[TS]: {} \n'.format("socket open error ",err))
         
port = 51625
EDUserver_binding=("", port)
edusd.bind(EDUserver_binding)
edusd.listen(1)
ctsd, addr=edusd.accept()
while True:
    hnstring=ctsd.recv(100).decode('utf-8').strip(' \t\r\n\0')
    strr=hnstring
    if not strr:
        break
    if strr in EDUserver.EDU_Table and strr:
        entry=strr+ " "+EDUserver.EDU_Table[strr].address + " "+EDUserver.EDU_Table[strr].flag
    if strr not in EDUserver.EDU_Table and strr:
        entry= "Error: HOST NOT FOUND"
    if strr:
        ctsd.send(entry.encode('utf-8')) 

edusd.close()
exit() 

