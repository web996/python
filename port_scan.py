def tcp_scan(ip,port):
        try:
            sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            # Print if the port is open
            res=sock.connect_ex((ip, port))
            sock.close()
            if res==0:
             #print(ip+" open")
             return 1
            else:
             #print("fail")
             return 0
            #return 1
        except Exception as e:
               #print(e)
               pass
               return 0


def Read_txt(txt):##read ip files
    with open(txt, "r") as f:
        data=f.readlines()
        return data


def create_thread(ip, port,is_ssl,thread_list):  ##IP PORT
    t = threading.Thread(target=main_scan_fun, args=(ip, port,is_ssl))
    thread_list.append(t)
    t.start()


def main_scan_fun(ip, port,is_ssl):
    #print("thread ",ip)
    is_open=tcp_scan(ip,port)
    if(is_open==1):##if port open
       mysql.insert_ipinfo(ip,port,'open')


def thread_joins(thread_list):  # put all threads in block until threads finished
    for t in thread_list:
        t.join()

def main_scan_threads(ip):
    thread_list = []
    ip=ip.rstrip('\n')
    net = ipaddress.ip_network(ip,False)
    ip_count = net.num_addresses##write address counts to sql
    print(ip_count,net)#write ips amount and ip address to sql
    mysql.insert_data_task(net,ip_count)
    cc=0
    ip_cur=0
    for ip in net:
        cc+=1
        ip_cur+=1
        ips=str(ip)
        ##create_thread(ips,80,0,thread_list)
        #create_thread(ips, 443, 1,thread_list)
        create_thread(ips, 1024, 0,thread_list)
        create_thread(ips, 8080, 0,thread_list)
        #create_thread(ips, 8888, 0,thread_list)
        #break
        ###update cur cur/max
        #mysql.update_data_cur_cout(net,ip_cur)
        if(cc==50000):
         thread_joins(thread_list)
         thread_list.clear()#clear []##consider to cancel
         cc=0##reset

    thread_joins(thread_list)
    mysql.update_task_done(net)###update task ip is done
 


def init_pool(ip_file):#ips array,threads nums
    datas=Read_txt(ip_file)##ret ips[]
    counts=len(datas)##write task number
    if(counts==0):
        print("ip's empty")
        return
    ###start init pool
    cpus = multiprocessing.cpu_count()
    print("cpus",cpus)
    pool = Pool(cpus-1)##leving one cpu for web server
    pool_outputs = pool.map(main_scan_threads, datas)##parament
    pool.close()  #
    pool.join()  #


def main_map(i):
    print(i)

if __name__ == '__main__':
 if (len(sys.argv)) != 2:
    print("Usage: " + sys.argv[0] + " IP File")
    exit(1)

 ip_file = sys.argv[1]
 init_pool(ip_file)
