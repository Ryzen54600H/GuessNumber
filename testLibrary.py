import ConnectToDedicatedServer
import socket

_realIP = '0.tcp.ap.ngrok.io'
_realPort = 18368
_matchMakingAddress = "ws://104.194.240.16:8881"
_localIP = 'localhost'
_localPort = 80


# if (ConnectToDedicatedServer.RegisterGame(_matchMakingAddress, _realIP, _realPort, int(ConnectToDedicatedServer.socket_type["SOCKET"]), "Guess Number", "Info", "Group 1")):
# 	print("Register successfully")
# else:
# 	print("Failed to register")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((_localIP, _localPort))
sock.listen()


# <summary>
#	Create connections with Match making server and get game request
#	Unpack game request to get matchId, uid1, uid2 and key
#	
# <summary>
mmConnect, mmAddress, mmRequest = ConnectToDedicatedServer.ListenToMMServer(sock)
matchId = -1
uid1 = -1
uid2 = -1
key = ""
if (mmConnect is not None):
	print("MM request ", mmRequest)
	action, matchId, uid1, uid2, key = ConnectToDedicatedServer.DecodeMMRequest(mmRequest)


# Overwrite this function 
def __CheckClient(helloPkg):
	if helloPkg == b"Hello":
		return True;
	else:
		return False

def __CreateConnectionWithClient(sock):
	connect, address = sock.accept()
	helloPkg = connect.recv(1024)
	if (__CheckClient(helloPkg)):
		print("Client is accepted")
		return connect, address
	else:
		print("Client is not accepted")
		connect.close()
		return None, None

# <summary>
#	Create connections with clients
#
# <summary>
c1, a1, c2, a2 = None, None, None, None
while (c1 is None):
	c1, a1 = __CreateConnectionWithClient(sock)
print("First client is connected ", a1)
while (c2 is None): 
	c2, a2 = __CreateConnectionWithClient(sock)
print("Second client is connected ", a2)
