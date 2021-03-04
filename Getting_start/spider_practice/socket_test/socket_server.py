# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 22:50:39 2020

@author: Minzel
"""

# socket服务端
import socket
import threading

server = socket.socket()
# 绑定的第一个参数是IP地址, 第二个参数是端口
# 两个参数是一个tuple
server.bind(('10.67.69.106', 8000))

server.listen()

# 获取客户端连接并启动线程去处理
def handle_sock(sock, addr):
    while True:
        # recv方法是阻塞的
        tmp_data = sock.recv(1024)
        print(tmp_data.decode("utf8"))
        input_data = input()
        sock.send(input_data.encode("utf8"))


while True:
    # 阻塞等待连接
    sock, addr = server.accept()

    #启动一个线程去处理新的用户连接
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()


#体验到直接获取原始数据,裸数据




    # if tmp_data:
    #     data += tmp_data.decode("utf8")
    #     if tmp_data.decode("utf8").endswith("#"):
    #         break
    # else:
    #     break;

# print(data)
# sock.close()