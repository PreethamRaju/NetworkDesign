

Files submitted
client.py - The python code to send and receive an image of type jpeg to and from the user.
server.py - The python code to send and reveive an image to and from a client running on the same machine.
clisend.jpg - The image that is sent by the client.
servsend.jpg - The image that is sent by the server to the client.
clirecv.jpg - The image received by the client that was sent by the server.
servrecv.jpg = The image sent from the client side.

Setup
Create a folder(directory) in your PC and name it(say 'phase1').
Now paste all the files i.e. the client and the server code file along with the test images.
OR
copy and paste the folder 'phase1'
Now, open two terminals in ubuntu and change your working directory to phase1 in both.
First type the command 'python client.py'
[Since the server is the first in this case to send the image, the client has to be ready. Hence we are running the client code first].
In the other terminal type the command 'python server.py'
Now both the code have been executed and the images have been exchanged between the server and the client.

  
