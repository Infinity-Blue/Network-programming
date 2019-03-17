
# coding: utf-8

# In[ ]:


import socket as mysoc
def client(file_name):
    #first socket for RSserver
    nbrConnect=0
    try: 
        ctors = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("RS server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
        
    RS_ip=mysoc.gethostbyname(mysoc.gethostname())
    RSserver_binding=(RS_ip,52171)
    ctors.connect(RSserver_binding)
    
    with open('RESOLVED.txt', 'w') as output_file:
        with open('PROJ2-HNS.txt', 'r') as input_file:
            for line in input_file:
                ctors.send(line.encode('utf-8'))
                dr=ctors.recv(100).decode('utf-8')
                output_file.write(dr.strip()+'\n')

    ctors.close()
    exit()
client('PROJ2-HNS.txt')

