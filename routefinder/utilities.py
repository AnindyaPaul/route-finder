import re

import Queue as Q
from graph.models import Graph


def find_districts():
    ret = list()
    '''
    f = open('/mnt/archive/django-workspace/routefinder/static/input.txt')
    queryset = list()
    for line in f:
        lst = re.split(r'\s|\n', line)
        graph = Graph()
        graph.u = lst[0]
        graph.v = lst[1]
        graph.bus = lst[2]
        print lst[3]
        graph.cost = float(lst[3])
        graph.distance = float(lst[4])
        graph.time = float(lst[5])
        queryset.append(graph)
    '''
    queryset = Graph.objects.all()

    for obj in queryset: 
        if str(obj.u) not in ret:
            ret.append(str(obj.u))
        if str(obj.v) not in ret:
            ret.append(str(obj.v))

    for obj in ret:
        print obj
    return ret


def init(src, des, param):
    print "Init starts"
    cnt = 0
    G=list() #adjacency list
    s2i=dict()  #string to integer mapping
    i2s=dict()  #integer to string mapping
    '''
    f = open('/mnt/archive/django-workspace/routefinder/static/input.txt')
    queryset = list()
    for line in f:
        lst = re.split(r'\s|\n', line)
        graph = Graph()
        graph.u = lst[0]
        graph.v = lst[1]
        graph.bus = lst[2]
        print lst[3]
        graph.cost = float(lst[3])
        graph.distance = float(lst[4])
        graph.time = float(lst[5])
        
        print str(graph.cost) + ' ' + str(graph.distance) + ' ' + str(graph.time)
        queryset.append(graph)
    '''
    queryset = Graph.objects.all()
    for obj in queryset:

        if obj.u not in s2i:
            s2i[str(obj.u)] = cnt
            G.append([])
            cnt = cnt +1

        if obj.v not in s2i:
            s2i[str(obj.v)] = cnt
            G.append([])
            cnt = cnt +1

        u = str(obj.u)
        v = str(obj.v)
        bus = str(obj.bus)
       
        cost = obj.cost 
        time = obj.time
        distance = obj.distance

        G[s2i[u]].append({'v' : v, 'bus' : bus,'cost' : cost, 'time' : time, 'distance' : distance})
        G[s2i[v]].append({'v' : u, 'bus' : bus,'cost' : cost, 'time' : time, 'distance' : distance})

    return dijkstra(src,des,G,s2i,param)

def dijkstra(src,des,G,s2i,param):
    dis1 = dict()
    dis2 = dict()
    par1 = dict()
    par2 = dict()
    bus1 =dict()
    bus2 =dict()
    cost = dict()
    time = dict()
    dist = dict()

    q = Q.PriorityQueue()
    q.put((0,src))
    dis1[src] = 0
    par1[src] = src
    cost[src] = 0
    time[src] = 0
    dist[src] = 0
    #par2[src] = "-1"

    while not q.empty():
        
        U = q.get()
        u = U[1]
        i = s2i[u]
        f = 0

        #if u == des:
          #  break
        
        for obj in G[i]:
            v = obj['v'] 
            bus = obj['bus']
            #new node, update best distance
            if v not in dis1:          
                dis1[v] = dis1[u] + obj[param]
                cost[v] = cost[u] + obj['cost']
                time[v] = time[u] + obj['time']
                dist[v] = dist[u] + obj['distance']
                
                f = 1;
                par1[v] = u
                bus1[v] = bus
            
            #relax node with best distance
            elif dis1[v] > dis1[u] + obj[param]:
                dis2[v] = dis1[v]
                bus2[v] = bus1[v]
                par2[v] = par1[v]
                #print "Updated "+v+" "+str(dis2[v])

                dis1[v] = dis1[u] + obj[param]
                cost[v] = cost[u] + obj['cost']
                time[v] = time[u] + obj['time']
                dist[v] = dist[u] + obj['distance']
                par1[v] = u
                bus1[v] = bus
                f = 1

            #second best not yet found
            if v not in dis2:

                #update with best distance of u and current edge if less than best distance of v
                if dis1[u] + obj[param] > dis1[v]:
                    dis2[v] = dis1[u] + obj[param]
                    par2[v] = u
                    bus2[v] = bus
                   # print "Updated "+v+" "+str(dis2[v])+" "+str(par2[v])
                    f = 1

                #update with second best distance of u(if it exists) and current edge if less than best distance of v
                elif u in dis2:
                    if dis2[u] + obj[param] > dis1[v]:
                        dis2[v] = dis2[u] + obj[param]
                        par2[v] = u
                        bus2[v] = bus
                        #print "Updated "+v+" "+str(dis2[v])+" "+str(par2[v])
                        f = 1
            #try to update second best distance with best distance of u and current edge
            elif dis1[u] + obj[param] > dis1[v] and dis1[u] + obj[param] < dis2[v]:
                dis2[v] = dis1[u] + obj[param]
                par2[v] = u
                bus2[v] = bus
                #print "Updated "+v+" "+str(dis2[v])+" "+str(par2[v])
                f = 1

            #try to update second best distance with second best distance of u and current edge
            elif u in dis2 and dis2[u] + obj[param] > dis1[v] and dis2[u] + obj[param] < dis2[v]:
                dis2[v] = dis2[u] + obj[param]
                par2[v] = u
                bus2[v] = bus
                #print "Updated "+v+" "+str(dis2[v])+" "+str(par2[v])
                f = 1

            if f==1:
                q.put((dis1[v],v))

    return path(src,des,par1,par2,bus1,bus2,dis1,dis2,cost,dist,time)
    

def path(src,des,par1,par2,bus1,bus2,dis1,dis2,cost,dist,time):
    s = src
    d = des
    P1 = list()
    f = 0
    while src != des:
        P1.append({'city':des,'bus':bus1[des],'param':dis1[des], 'cost':cost[des], 'dist':dist[des], 'time':time[des]})
        if des not in par1:
            f = 1
            break
        des = par1[des]
    P1.append({'city':src})
    P1.reverse()
    if f == 1:
        P1 = list()
        
    sum1 = 0.0
    icost = 0.0
    idist = 0.0
    itime = 0.0
    print "P 1"
    for i in range(len(P1)):
        print "--------"
        print P1[i]['city']
        if 'bus' in P1[i]:
            print P1[i]['bus']
            P1[i]['param'] -= sum1
            sum1 += P1[i]['param']
            
            P1[i]['cost'] -= icost
            icost += P1[i]['cost']
            
            P1[i]['dist'] -= idist
            idist += P1[i]['dist']
            
            P1[i]['time'] -= itime
            itime += P1[i]['time']
            
            print P1[i]['param']
            print "--------"

    P2 = list()
    sum2 = 0
    '''
    l = list()
    src = s
    des = d
    f = 0
    
    while src != des:
        print des
        if(des in l):
            f = 1
            print "break"
            break
        l.append(des)
        if des in bus2 and des in dis2:
            P2.append({'city':des,'bus':bus2[des],'cost':dis2[des]})
        else:
            f = 1
            break
        if des not in par2:
            f = 1
            break
        des = par2[des]
        print des
        
    print "f "+str(f)
    P2.append({'city':src})
    P2.reverse()
    if f == 1:
        P2 = list()
        print "empty"
        
    sum2 = 0
    print "P 2"
    for i in range(len(P2)):
        print "--------"
        print P2[i]['city']
        if 'bus' in P2[i]:
            print P2[i]['bus']
            P2[i]['cost'] -= sum2
            sum2 += P2[i]['cost']
            print P2[i]['cost']
            print "--------"
    
    print str(sum2) + " " +str(dis2[d])
    if sum2 != dis2[d]:
        print "Empty"
    '''
    return {'P1':P1,'sum1':sum1, 'icost':icost, 'itime':itime, 'idist':idist, 'P2':P2, 'sum2':sum2}