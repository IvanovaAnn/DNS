# DNS
Ivanova Anna KN-202 Topic 2 Task 4. 
User person.py sends a request to the server to determine the ip address by domain name(A) or to get the Name Server(NS).
The server sends requests via dns.py, gets the response, checks if it is in the cache, and adds it there if in the cache hashing.py it's gone.
To stop the server, the user sends the stop command, and everything is loaded from the cache to a file dns.txt.
When the server is reactivated from the file, everything will automatically go to the hash after passing the lifetime check. 
(!) Before the domain name, write the record type: A or NS. After the type of record it is necessary to put a space. 
The record type is stored in the same place as the domain name.
An example of running: C:\Users\PycharmProjects\untitled1\DNS>python serv.py
C:\Users\PycharmProjects\untitled1\DNS>python person.py NS habr.com 
C:\Users\PycharmProjects\untitled1\DNS>python person.py A habr.com
C:\Users\PycharmProjects\untitled1\DNS>python person.py stop
