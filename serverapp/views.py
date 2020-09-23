from django.shortcuts import render
import json

from django.shortcuts import render
from django.db import connection
from .models import temp1,temp2
from django.shortcuts import render, HttpResponse, redirect, reverse
import socket
import time
from django.http import HttpResponse

#初始化
hosts = []
ports = []
def serial(request):
    global hosts
    global ports
    flags = {}
    flags['flag'] = "端口还未配置，请点击配置按钮"
    if request.POST:
        hosts.append(request.POST.get('host1'))
        ports.append(int(request.POST.get('port1')))
        hosts.append(request.POST.get('host2'))
        ports.append(int(request.POST.get('port2')))
        hosts.append(request.POST.get('host3'))
        ports.append(int(request.POST.get('port3')))
        hosts.append(request.POST.get('host4'))
        ports.append(int(request.POST.get('port4')))

        flags['flag'] = "配置完成"
    return render(request,'index.html',flags)


def index(request):
    return render(request,'index.html')

#地面站将航点信息发送给无人机 8100
def process(request):
    host = hosts[0]
    port = ports[0]
    print(host)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host,port))

    pos = []
    for i in range(1,6):
        x = request.POST.get('posx'+str(i))
        y = request.POST.get('posy'+str(i))
        pos.append(x)
        pos.append(y)
    print(pos)

    for context in pos :
        if context!=None:
            context = bytes(context+' ',encoding='UTF-8')
            print(context)
            s.send(context)
    return HttpResponse("ok")

# form表单形式发送数据 起落站 8300
def search1(request):

    host = hosts[2]
    port = ports[2]

    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.connect((host, port))

    ctx1 ={}
    ctx1.setdefault('rlt1', 0)
    if request.POST:
        ctx1['rlt1'] = request.POST['q']

        context = bytes(str(ctx1['rlt1']), encoding='UTF-8')
        print(context)
        s1.send(context)

    return render(request, "index.html", ctx1)



# form表单形式发送数据 无人机 8100
def search2(request):

    host = hosts[0]
    port = ports[0]

    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2.connect((host, port))

    ctx2 ={}
    ctx2.setdefault('rlt2',0)
    if request.POST:
        ctx2['rlt2'] = request.POST['p']
        context = bytes(ctx2['rlt2'] + ' ', encoding='UTF-8')
        print(context)
        s2.send(context)

    return render(request, "index.html", ctx2)


#起落站发送给地面站 8400用于接收起落站数据
def recvdata1(request):
    # 接收一个数据
    if request.is_ajax():
        try:
            s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 接收数据的本机IP和端口号
            host = hosts[3]
            port = ports[3]
            s3.bind((host, port))
            # 接收数据
            data = s3.recv(1024)

            print(data)
            data = str(data, encoding='utf-8')
            data = data.split(' ')
            position = data[0]  # 接收位置信息
            temperature = data[1]  # 接收温度信息
            print(position, temperature)
            # 添加一条数据到数据库中
            temp_data = temp1(position=position, temperature=temperature)
            temp_data.save()
            data = 'position = ' + str(position) + 'm'+'  '+'temperature = ' + str(temperature)+'°'
            print(data)
            r= HttpResponse(data)
            return r
        except:
            data1  =  '当前没有数据输入，请检查数据是否正在输入'
            r1 = HttpResponse(data1)
            return r1
    else:
        return HttpResponse('NO AJAX')

#无人机发送给地面站 8200用于接收无人机数据
def recvdata2(request):
    # 接收一个数据
    if request.is_ajax():
        try:
            s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 接收数据的本机IP和端口号
            host = hosts[1]
            port = ports[1]
            s4.bind((host, port))
            # 接收数据
            data = s4.recv(1024)

            print(data)
            data = str(data, encoding='utf-8')
            data = data.split(' ')
            position = data[0]  # 接收位置信息
            temperature = data[1]  # 接收温度信息
            print(position, temperature)
            # 添加一条数据到数据库中
            temp_data = temp2(position=position, temperature=temperature)
            temp_data.save()
            data = 'position = ' + str(position) + 'm'+'  '+'temperature = ' + str(temperature)+'°'
            print(data)
            r= HttpResponse(data)
            return r
        except:
            data  =  '当前没有数据输入，请检查数据是否正在输入'
            r1 = HttpResponse(data)
            return r1
    else:
        return HttpResponse('NO AJAX')

def get_cursor1():
    return connection.cursor()
def show1(request):
    cursor = get_cursor1()
    cursor.execute("select id,position,date_added,temperature from serverapp_temp1")
    data_temps = cursor.fetchall()  # 数据库所有数据
    length = len(data_temps)
    context ={
        'data' : data_temps,
        'length' : length}
    return render(request, 'show1.html',context)
def show2(request):
    cursor = get_cursor1()
    cursor.execute("select id,position,date_added,temperature from serverapp_temp2")
    data_temps = cursor.fetchall()  # 数据库所有数据
    length = len(data_temps)
    context ={
        'data' : data_temps,
        'length' : length}
    return render(request, 'show2.html',context)

def newest1(request):
    cursor = get_cursor1()
    cursor.execute("select id,position,date_added,temperature from serverapp_temp1")
    data_temps = cursor.fetchall()  # 数据库所有数据
    length = len(data_temps)
    data_temps = data_temps[length-1]
    context ={
        'data' : data_temps,
        'length' : length}
    return render(request, 'newest1.html',context)
def newest2(request):
    cursor = get_cursor1()
    cursor.execute("select id,position,date_added,temperature from serverapp_temp2")
    data_temps = cursor.fetchall()  # 数据库所有数据
    length = len(data_temps)
    data_temps = data_temps[length-1]
    context ={
        'data' : data_temps,
        'length' : length}
    return render(request, 'newest2.html',context)
# 查询
def select1(request):
    if request.method == "POST":
        id = request.POST.get('id')
        position = request.POST.get('position')
        temperature = request.POST.get('temperature')
        date_added = request.POST.get('date_added')
        if id:
            temp_data = temp1.objects.filter(id=id).first()
        if position:
            temp_data = temp1.objects.filter(position=position).all()
        if temperature:
            temp_data = temp1.objects.filter(temperature=temperature).all()
        if date_added:
            temp_data = temp1.objects.filter(date_added=date_added).first()
        if temp_data == None:
            #NoneType
            return HttpResponse("错误")
        else:
            temp_datas = []
            print(temp_data)
            try:
                length = len(temp_data)
                for temp in temp_data:
                    id = temp.id
                    position = temp.position
                    temperature = temp.temperature
                    date_added = temp.date_added
                    datas = [id,position,temperature,date_added]
                    temp_datas.append(datas)
                print(temp_datas)
                context = {
                    'data': temp_datas,
                    'length': length,
                    'msg': True,
                            }
            except TypeError:
                length=1
                id = temp_data.id
                position = temp_data.position
                temperature = temp_data.temperature
                date_added = temp_data.date_added
                datas = [id, position, temperature, date_added]
                temp_datas.append(datas)
                context = {
                    'data': temp_datas,
                    'length': length,
                    'msg': True,
                }
        return render(request, 'select1.html', context)

    else:
        context = {
            'msg' : False,
        }
        return render(request, 'select1.html', context)
def select2(request):
    if request.method == "POST":
        id = request.POST.get('id')
        position = request.POST.get('position')
        temperature = request.POST.get('temperature')
        date_added = request.POST.get('date_added')
        if id:
            temp_data = temp2.objects.filter(id=id).first()
        if position:
            temp_data = temp2.objects.filter(position=position).all()
        if temperature:
            temp_data = temp2.objects.filter(temperature=temperature).all()
        if date_added:
            temp_data = temp2.objects.filter(date_added=date_added).first()
        if temp_data == None:
            #NoneType
            return HttpResponse("错误")
        else:
            temp_datas = []
            print(temp_data)
            try:
                length = len(temp_data)
                for temp in temp_data:
                    id = temp.id
                    position = temp.position
                    temperature = temp.temperature
                    date_added = temp.date_added
                    datas = [id,position,temperature,date_added]
                    temp_datas.append(datas)
                print(temp_datas)
                context = {
                    'data': temp_datas,
                    'length': length,
                    'msg': True,
                            }
            except TypeError:
                length=1
                id = temp_data.id
                position = temp_data.position
                temperature = temp_data.temperature
                date_added = temp_data.date_added
                datas = [id, position, temperature, date_added]
                temp_datas.append(datas)
                context = {
                    'data': temp_datas,
                    'length': length,
                    'msg': True,
                }
        return render(request, 'select2.html', context)

    else:
        context = {
            'msg' : False,
        }
        return render(request, 'select2.html', context)
