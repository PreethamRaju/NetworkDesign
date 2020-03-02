Files submitted
client.py - The python code to receive an image of type jpeg from the server.
server.py - The python code to send an image to a client running on the same machine.
Channel.py - This is the code to simulate the prroperties of the channel such as data, ack error, data, ack loss. 
servsend.jpg - The image that is sent by the server to the client.

Setup
Create a folder(directory) in your PC and name it(say 'phase4').
Now paste all the files i.e. the client, channel and the server code file along with the test image.
OR
copy and paste the folder 'phase4'
Now, open 3 terminals in ubuntu and change your working directory to phase3 in both.
First type the command 'python client.py'
[Since the server is the first in this case to send the image, the client has to be ready. Hence we are running the client code first].
In the another terminal type the command 'python channel.py' and select the property of the channel.
In the other terminal type the command 'python server.py'
Now all the the code have been executed and the image has been exchanged between the server and the client.

  
