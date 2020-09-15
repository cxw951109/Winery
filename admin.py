#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 21:01
# @Author  : cxw
# @File    : app
# @Software: PyCharm


import os
import datetime
import flask
import shutil
import glob
import zipfile
from flask import request, Response
from app import create_app
from flask_socketio import SocketIO, emit
from app.model import History, Imgs
from app.validators.terminal import Real_time
import threading
import socket  #导入socket模块
import time #导入time模块
import config
import json


app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")
m_exit_prog = False


@socketio.on('connect', namespace='/chatroom')
def connect():
    print('connect')


@socketio.on('disconnect', namespace='/chatroom')
def disconnect():
    print('Client disconnected')


@app.route("/get_mes", methods=['POST', 'GET'])
def get_mes():
    data = request.get_data()
    data_str = data.decode()
    data_dict =json.dumps({"ID":data_str[1:7],"step":data_str[7:11]})
    print(type(data_dict), data_dict)
    socketio.emit('chat_message',
                  {"data":str(data_dict)},
                  namespace='/chatroom')
    return ('')


def print_log(message):
    print(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()), message)


def mes_update(folder_name):
    times =time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime())
    with open(folder_name+"result.json") as json_file:
        text = json.load(json_file)
    address =folder_name.replace('D:/nginx-1.18.0/html/dist/static','static')
    mes1 = History(timestamp=text["timestamp"], status=text["status"], create_at=times,result=text["result"],machine_id=text["machine_id"])
    History.add(mes1)
    History.flush()
    if text["result"] != 0:
        data = []
        ls = os.listdir(folder_name)
        lists = [i[:-4] for i in ls if i.endswith('.txt')]
        for x in lists:
            with open(folder_name+x+'.txt') as f:
                txt =f.read()
                data.append(Imgs(txt=txt,img=address+x+'.png',img1=address+x+'1.png',img2=address+x+'2.png',img3=address+x+'3.png',history_id=mes1.id))
        Imgs.add_all(data)
    result = History.update()
    if result:
        if text["result"] != 0:
            socketio.emit('real',
                          {"data": {"result":text["result"],"machine_id":text["machine_id"],"images":[address+x+'.png' for x in lists],'id':int(text["machine_id"][-2:])-1}},
                          namespace='/chatroom')
        else:
            lists = []
            socketio.emit('real',
                          {"data": {"result":text["result"],"machine_id":text["machine_id"],"images":[],'id':int(text["machine_id"][-2:])-1}},
                          namespace='/chatroom')



def extract_upload(zip_filename, folder_name):
    print_log('extract_upload, filename={}, machine_id={}'.format(zip_filename, folder_name))
    try:
        f = zipfile.ZipFile(zip_filename)
    except Exception as e:
        print_log('上传文件受损，无法解压')
        return False
    sub_folder_name = f.namelist()[0].split('/')[0]
    tmp_folder = 'D:/nginx-1.18.0/html/dist/static/tmp_data'
    if os.path.exists(tmp_folder):
        shutil.rmtree(tmp_folder)
    os.mkdir(tmp_folder)
    print_log('sub_folder_name={}'.format(sub_folder_name))
    f.extractall(path=tmp_folder)
    f.close()

    file_list = [x for x in os.listdir(tmp_folder + '/' + sub_folder_name)]
    for filename in file_list:
        print_log("move {} to {}".format(tmp_folder + '/' + sub_folder_name + '/' + filename, folder_name))
        if not os.path.exists(folder_name + filename):
            shutil.move(tmp_folder + '/' + sub_folder_name + '/' + filename, folder_name)
    shutil.rmtree(tmp_folder)
    return True


def rename_to_posted(current_folder, file_list):
    for filename in file_list:
        shutil.move(current_folder + filename, current_folder + filename + "_posted")


def listen():
    print_log("启动UPD监听")
    #server 接收端
    # 设置服务器默认端口号
    # 创建一个套接字socket对象，用于进行通讯
    # socket.AF_INET 指明使用INET地址集，进行网间通讯
    # socket.SOCK_DGRAM 指明使用数据协议，即使用传输层的udp协议
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # address = (config.udp_ip, config.udp_port)
    address = ('172.20.10.3', 8082)
    server_socket.bind(address)  # 为服务器绑定一个固定的地址，ip和端口
    server_socket.settimeout(10)  #设置一个时间提示，如果10秒钟没接到数据进行提示

    while not m_exit_prog:
        #正常情况下接收数据并且显示，如果10秒钟没有接收数据进行提示（打印 "ok"）
        #当然可以不要这个提示，那样的话把"try:" 以及 "except"后的语句删掉就可以了
        try:
            # 接收客户端传来的数据 recvfrom接收客户端的数据，默认是阻塞的，直到有客户端传来数据
            # recvfrom 参数的意义，表示最大能接收多少数据，单位是字节
            # recvfrom返回值说明
            # receive_data表示接受到的传来的数据,是bytes类型
            # client  表示传来数据的客户端的身份信息，客户端的ip和端口，元组
            receive_data, client = server_socket.recvfrom(1024)
            receive_data = receive_data.decode("gbk")
            print_log("来自客户端{},发送的:{}".format(client, receive_data))  #打印接收的内容
            socketio.emit('chat_message',
                          {"data": {"data":receive_data}},
                          namespace='/chatroom')
        except socket.timeout:  #如果10秒钟没有接收数据进行提示（打印 "ok"）
            print_log("udp ok,no message!")


@app.route('/save_frames', methods=['POST'])
def upload():
    if flask.request.method == 'POST':
        file0 = request.files['zipfile']
        machine_id = request.args.get('machine_id')
        if not os.path.isdir('D:/nginx-1.18.0/html/dist/static/site_data/' + machine_id):
            os.mkdir('D:/nginx-1.18.0/html/dist/static/site_data/' + machine_id)
        folder_name = "D:/nginx-1.18.0/html/dist/static/site_data/{}/{}/".format(machine_id, request.args.get('folder_name'))
        print_log("folder_name={}".format(folder_name))
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        print_log('upload received, folder=' + folder_name)
        filename = '{}_{}.zip'.format(machine_id, int(time.time() * 1000))
        file0.save(file0.filename)  # file0.filename = 'to_post.zip'
        size = os.stat(file0.filename).st_size
        print_log('file size={}, saved_as: {}'.format(size, filename))
        if size < 10:  # 没有内容
            if os.path.exists(file0.filename):
                os.remove(filename)
            print_log('no file inside the zip file.')
            return json.dumps({'status': 3})
        else:
            result = extract_upload(file0.filename, folder_name)
            if result:
                os.remove(file0.filename)
                mes_update(folder_name)
                print_log('received images saved to {}'.format(folder_name))
                # 此处解压出来的文件夹里，包含result.json文件，检测结果，异常信息，错误代码等都会在里面
                return json.dumps({'status': 1})
            else:
                return json.dumps({'status': 2})


@app.route('/real_time_img',methods=["POST"])
def real_time_img():
    form = Real_time().check_param()
    file0 = request.files['image']
    id = file0.filename.split('_')[0]
    t =int(time.time())
    file0.filename =id+'_'+str(t)+'.jpg'
    path ='D:/nginx-1.18.0/html/dist/static/site_data/now'
    # path ='../Spirit/src/assets/site_data/now'
    if not os.path.isdir(path):
        os.mkdir(path)
    files = glob.glob(path+'/'+id+'_'+'*.jpg')
    if files:
        os.remove(files[0])
    file0.save(os.path.join(path, file0.filename))
    socketio.emit('present',
                  {"data": {"images":"static/site_data/now/"+file0.filename,"id":int(id)-1}},
                  namespace='/chatroom')
    return json.dumps({'status': 1})


@app.route('/get_imgs',methods=["POST"])
def get_imgs():
    path = 'D:/nginx-1.18.0/html/dist/static/site_data/now/'
    list2=[{"id":i,"images":''} for i in range(36)]
    if not os.path.isdir(path):
        return json.dumps({'data': list2})
    for file in os.listdir(path):
        id = file.split('_')[0]
        list2[int(id)-1]["images"] ='static/site_data/now/'+file

    return json.dumps({'data': list2})

# t1 = threading.Thread(target=listen, name="listen")
# t1.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

