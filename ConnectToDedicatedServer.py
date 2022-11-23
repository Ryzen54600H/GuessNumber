import websockets
import struct
import asyncio
import socket 

# <summary>
# Type of socket connection to communicate with match making server
# <summary>
socket_type = {
	"WEB_SOCKET" : 1,
	"SOCKET" : 0
}

# <summary>
# Type of package to communicate with match making server
# <summary>
manager_pkg_type = {
	"PKG_HELLO": 1
}



# <summary>
#	<para>
#	Format register package
#	<para>
#	<param name="ip">Ip address of Game server which handle the match<param>
#	<param name="port">Port of Game server which listen to connections<param>
#	<param name="socketType">Type of the socket connection<param>
#	<param name="gameName">Name of the game<param>
#	<param name="gameInfo">Infomation of the game, eg: description, rule...<param>
#	<param name="authString">Authentication string<param>
# <summary>
def __createGameRegisterPackage(ip, port, socketType, gameName, gameInfo, authString):
	registerPackage = bytearray()
	registerPackage.extend(int(1).to_bytes(4, 'little'))
	registerPackage.extend(len(ip).to_bytes(4, 'little'))
	registerPackage.extend(ip.encode())
	registerPackage.extend(port.to_bytes(4, 'little'))
	registerPackage.extend(socketType.to_bytes(4, 'little'))
	registerPackage.extend(len(gameName).to_bytes(4, 'little'))
	registerPackage.extend(gameName.encode())
	registerPackage.extend(len(gameInfo).to_bytes(4, 'little'))
	registerPackage.extend(gameInfo.encode())
	registerPackage.extend(len(authString).to_bytes(4, 'little'))
	registerPackage.extend(authString.encode())
	return registerPackage

# <summary>
#	<para>
#	Register game to Match making server
#	<para>
#	<param name="ip">Ip address of Game server which handle the match<param>
#	<param name="port">Port of Game server which listen to connections<param>
#	<param name="socketType">Type of the socket connection<param>
#	<param name="gameName">Name of the game<param>
#	<param name="gameInfo">Infomation of the game, eg: description, rule...<param>
#	<param name="authString">Authentication string<param>
# <summary>
async def __registerGame(matchMakingAddress, ip, port, socketType, gameName, gameInfo, authString):
	async with websockets.connect(matchMakingAddress) as websocket:
		registerPackage = __createGameRegisterPackage(ip, port, socketType, gameName, gameInfo, authString)
		await websocket.send(registerPackage)
		resultPkg = await websocket.recv()
		result = int.from_bytes(resultPkg[0: 1], 'little')
		if (result == 1):
			return True
		else:
			return False


# <summary>
#	<para>
#	Unpack creating room request received from Match making server
#	<para>
#	<param name="mmRequest">Creating room request received from Match making server<param>
# <summary>
def __decodeMMRequest(mmRequest):
	action = int.from_bytes(mmRequest[0: 4], 'little')
	matchId = int.from_bytes(mmRequest[4: 8], 'little')
	uid1 = int.from_bytes(mmRequest[8: 12], 'little')
	uid2 = int.from_bytes(mmRequest[12: 16], 'little')
	keyLength = int.from_bytes(mmRequest[16: 20], 'little')
	key = mmRequest[20: 20 + keyLength].decode()
	print(action, " ", matchId, " ", uid1, " ", uid2, " ", keyLength, " ", key)
	return action, matchId, uid1, uid2, keyLength, key

# <summary>
#	<para>
#	Create package to response creating room request of Match making server
#	<para>
#	<param name="isRoomCreated">True if room is created and False if room is failed to create<param>
#	<param name="error">Reason causes failed to create room. None if room is created<param>
# <summary>
def __createMMResponse(isRoomCreated, error):
	mmResponse = bytearray();
	if (isRoomCreated):
		mmResponse.extend(int(1).to_bytes(4, 'little'))
	else:
		mmResponse.extend(int(0).to_bytes(4, 'little'))
		mmResponse.extend(error.encode())
	return mmResponse

# <summary>
#	Create the room based on Server ip and port
#	Due to ngrok restrictions, one local machine can only create one ngrok ip and port,
#		Client connections have to use the same ip and port with Match making server connection
# 	That means, this function doesn't resquire implementation
# <summary>
async def __createRoom():
	# Write Create room funtion here
	#
	#	
	#
	# return True if succesfully created, and False if unsuccessfully
	#
	#
	#
	return True;

# <summary>
#	When Game server received creating room request from Match making server
#	Firstly, create the room, use the ip and port given by Match making server
#	Then, return the response package which is created based on successful or unsuccessful room creating
# <summary>
async def __responseMMRequest():
	isRoomCreated = await __createRoom()
	error = ""
	if isRoomCreated:	
		print("Room is created")
	else:
		print("Room failed to create")
		error = "Room failed to create"
	return __createMMResponse(isRoomCreated, error)



# <summary>
# 	<para>
# 	Get room creating request from Match making server
#	<para>
#	<param name="mmConnect">Connection to Match making server<param>
#	<param name="mmAddress">Address of Match making server<param>
# <summary>	
async def __getMMRequest(mmConnect, mmAddress):
	request = None
	while (request == None):
		request = mmConnect.recv(1024)
		response = await __responseMMRequest()
		mmConnect.sendall(response)
	return request
		
# <summary>
#	<para>
# 	Get room creating request from Match making server
#	<para>
#	<param name="mmConnect">Connection to Match making server<param>
#	<param name="mmAddress">Address of Match making server<param>
# <summary>
async def __MMserverHandler(mmConnect, mmAddress):
	mmRequest = None
	while (mmRequest is None):
		mmRequest = await __getMMRequest(mmConnect, mmAddress)
	return mmRequest

# <summary>
# 	<para>
#	Create connection to listen Match making server's requests
#	<para>
# <summary>
async def __listenToMMServer(sock):
	mmConnect, mmAddress = sock.accept()
	mmRequest = await __MMserverHandler(mmConnect, mmAddress)
	return mmConnect, mmAddress, mmRequest

def DecodeMMRequest(mmRequest):
	action = int.from_bytes(mmRequest[0:4], 'little')
	matchId = int.from_bytes(mmRequest[4:8], 'little')
	uid1 = int.from_bytes(mmRequest[8:12], 'little')
	uid2 = int.from_bytes(mmRequest[12:16], 'little')
	keyLength = int.from_bytes(mmRequest[16:20], 'little')
	key = ""
	return action, matchId, uid1, uid2, key


def RegisterGame(matchMakingAddress, registerIP, registerPort, socketType, gameName, gameInfo, authString):
	return asyncio.run(__registerGame(matchMakingAddress, registerIP, registerPort, socketType, gameName, gameInfo, authString))

def ListenToMMServer(sock):
	return asyncio.run(__listenToMMServer(sock))





