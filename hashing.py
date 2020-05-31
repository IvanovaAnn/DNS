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
                file.write(self.time[el] + " " +
                           self.dict[self.time[el]] + " " + time + "\n")


    def init_hash(self):
        print("eeee")
        file_path = 'dns.txt'
        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            return
        with open('dns.txt', 'r') as file:
            print("uf")
            for line in file.readlines():
                list_lines = line[:-2].split(" ")
                self.dict[list_lines[0]] = list_lines[1]
                list_time = list_lines[2].split("_")
                time = ' '.join(list_time)
                self.time[time] = list_lines[0]
        print(self.time)
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
