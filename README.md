# DNS
Ivanova Anna KN-202 topic 2 task 4.User person.py sends a request to the server to determine the ip address by domain name. 
The server sends requests via dns.py, gets the response, checks if it is in the cache, and adds it there if in the hash hashing.py it's gone. 
To stop the server, the user sends the stop command, and everything is loaded from the hash to a file dns.txt. 
When the server is reactivated from the file, everything will automatically go to the hash, having passed the lifetime check. 
Launch example: C:\Users\PycharmProjects\untitled1\DNS>python serv.py 
C:\Users\PycharmProjects\untitled1\DNS>python person.py habr.com 
C:\Users\PycharmProjects\untitled1\DNS>python person.py stop
