import time
from datetime import timedelta
import os.path


class Hash:
    def __init__(self):
        self.dict = {}
        self.time = {}
        Hash.init_hash(self)

    def save_disk(self):
        with open('dns.txt', 'w') as file:
            for el in self.time.keys():
                list_time = el.split()
                time = '_'.join(list_time)
                list_ip = self.dict[self.time[el]].split()
                ip = '_'.join(list_ip)
                list_name = self.time[el].split()
                name = '_'.join(list_name)
                file.write(name + " " + ip + " " + time + "\n")

    def init_hash(self):
        file_path = 'dns.txt'
        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            return
        with open('dns.txt', 'r') as file:
            for line in file.readlines():
                list_lines = line[:-2].split(" ")
                list_name = list_lines[0].split("_")
                list_ip = list_lines[1].split("_")
                self.dict[' '.join(list_name)] = ' '.join(list_ip)
                list_time = list_lines[2].split("_")
                time = ' '.join(list_time)
                self.time[time] = ' '.join(list_name)
        with open('dns.txt', 'wb'):
            pass
        Hash.deadline_check(self)

    def contains_name(self, name):
        Hash.deadline_check(self)
        if name in self.dict.keys():
            return True
        return False

    def get_elements(self, name):
        return self.dict[name]

    def add_item(self, name, ip, time):
        self.dict[name] = ip
        self.time[time] = name

    def remove_item(self, name):
        self.dict.pop(name)

    def deadline_check(self):
        real_time = time.strftime("%D.%H.%M.%S", time.localtime())
        tm1 = timedelta(days=int(real_time[3:5]), hours=int(real_time[9:11]),
                        minutes=int(real_time[12:14]),
                        seconds=int(real_time[15:17])).__str__()
        list_keys = list(self.time.keys())
        list_keys.append(tm1)
        list_keys.sort()
        flag = True
        for i in list_keys:
            if i == tm1:
                flag = False
            elif flag:
                Hash.remove_item(self, self.time[i])
                self.time.pop(i)
