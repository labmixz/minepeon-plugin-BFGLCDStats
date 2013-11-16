#
# class to access miner via RPC API
# instantiate class with host and port number of server where miner instance is running
# throws: generic exception message: Exception ("API Connection Error")
import socket
import time
import json

class RPCClient:
    #
    # Class init
    def __init__(self, host, port, minerType):
        self.host = host
        self.port = port
        self.miner = minerType
    

    # execute miner API remote procedure call
    # parms: string containing the desired miner API command
    def command(self, command):
        
        if (self.miner == 1):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host, self.port))
                s.sendall(json.dumps({"command": command})) # send API request formatted as json
                time.sleep(0.02)
        
                # loop until a zero byte indicates we got all the data
                data = ""
                while True:
                    buffer = s.recv(65535)
                    if buffer:
                        data += buffer 
                    else:
                        s.close() 
                        break
                
                s.close() # close the socket
                
            except Exception as e:
                print "API Exception executing command: " + command
                print str(e) # TODO conditional logging?
                raise Exception ("API Connection Error")
          
            if data:                   
                try:
                    data    = data.replace('\x00', '') # the null byte makes json decoding unhappy
                    decoded = json.loads(data)      # we sent a json request, so expect json response
                    return decoded
                except:
                    # TODO conditional loggging
                    print "JSON decoding error - bad JSON sring:"
                    print data
                    pass # swallow the exception (normal use shouldn't throw one ?)
        
        elif (self.miner == 2):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host, self.port))
                s.sendall(json.dumps({"command": command})) # send API request formatted as json
                time.sleep(0.02)
        
                # loop until a zero byte indicates we got all the data
                data = ""
                while True:
                    buffer = s.recv(65535)
                    if '\x00' in buffer:
                        data += buffer # keep the buffer and bail from the loop - we got all the data
                        break # zero found, so we must have all the data TODO break in loop is ugly           
                    else:
                        data += buffer # No zero found yet, append current buffer to data and loop for more 
                
                s.close() # close the socket
                
            except Exception as e:
                print "API Exception executing command: " + command
                print str(e) # TODO conditional logging?
                raise Exception ("API Connection Error")
          
            if data:                   
                try:
                    data = data.replace('\x00', '') # the null byte makes json decoding unhappy
                    decoded = json.loads(data)      # we sent a json request, so expect json response
                    return decoded
                except:
                    # TODO conditional loggging
                    print "JSON decoding error - bad JSON sring:"
                    print data
                    pass # swallow the exception (normal use shouldn't throw one ?)
        
    #END command()