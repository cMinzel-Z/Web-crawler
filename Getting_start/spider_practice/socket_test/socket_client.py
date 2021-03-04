# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 23:14:47 2020

@author: Minzel
"""

# socket客户端
import socket

client = socket.socket()
client.connect(('10.67.69.106',8000))

# 数据发送
#client.send(b'bobby')

#server_data = client.recv(1024)
#print('server response: {}'.format(server_data.decode('utf8')))

# 当输出完成以后以#结尾就认为传输完成
while True:
    input_data = input()
    client.send(input_data.encode('utf8'))
    server_data = client.recv(1024)
    print('server response: {}'.format(server_data.decode('utf8')))
    
client.close()
