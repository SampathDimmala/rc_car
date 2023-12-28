
import socket
import network
import steer
import motorControl_i2c


def initI2c1():
    i2c = I2C(id=1, scl=Pin(3), sda=Pin(2))
    return i2c

#Initialize the I2C bus for communicating with the pca9685
i2c_1 = initI2c1() 
print("setting up i2c0")
sda = Pin(0)
scl = Pin(1)
id = 0

#initialize i2c0
i2c_0 = I2C(id=id, sda=sda, scl=scl)
print(i2c_0.scan())
steer_tof = steer.SteeringControl(i2c_1)

#Initialize the pca9685 class, servo class and steering control class
currentPosition = 90
steer_obj = steer.SteeringControl(i2c_1)

drive = motorControl_i2c.motorControl_i2c_module(i2c_1)



def actSTA():
    sta = network.WLAN(network.STA_IF)
    if sta.active() and sta.isconnected():
      sta.disconnect()
    sta.active(True)
    return sta

def connectToAP():
    sta = actSTA()
    print(sta.isconnected())
    if not sta.isconnected():
      print("connecting .....")
      sta.connect("MARKHFR", "MARKHFR11")
      while not sta.isconnected():
        pass
      print("connected to AP MARKHFR")
      return sta

def processPathLine(path):
  action = "halt"
  pwm_Val =0
  fron_wheel_servo_index =0
  #GEt the action = backward, forward, halt and pwmVal = 0-4095

  processJob = {}
  try:
    mainFun, subPath = path.split("?")
  except:
    return
  subFunList = subPath.split("&")
  for item in subFunList:
    print("subfun" + item)
    prop,value = item.split("=")
    processJob[prop] = value
  print({ "mainFun" : mainFun, "subFuns" : processJob })
  if mainFun == "steer":
    position = processJob["position"]
    steer_obj.turn(fron_wheel_servo_index, int(position))
  if(mainFun == "drive"):
    operation = processJob["operation"]
    pwm_Val = 2000
    global drive
    drive.control_motors(operation, pwm_Val); #Control the motor functions 
    


def startServer():
  connectToAP()
  addrInfo = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
  soc = socket.socket()
  soc.bind(addrInfo)
  soc.listen(5)
  listenToServer()
  return soc
  
def listenToServer(soc):
  cl, addr = soc.accept()
  print(addr)
  req = cl.recv(1024)
  req = str(req)
  reqLines = req.split("\\r\\n")
  pathLine = reqLines[0][7:-9]
  processPathLine(pathLine)
  html_sequence = """
      <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Ctrl</title><style>button{padding:10px 20px;margin:5px;font-size:16px}</style></head><body><button onclick="sp(35)">Max L (35掳)</button><button onclick="sp(92)">Ctr (92掳)</button><button onclick="sp(150)">Max R (150掳)</button><button onclick="cm('forward')">Fwd</button><button onclick="cm('backward')">Bwd</button><button onclick="cm('halt')">Hlt</button><script>function sp(p){var x=new XMLHttpRequest();x.open('GET','/steer?position='+p,true);x.send();}function cm(o){var x=new XMLHttpRequest();x.open('GET','/drive?operation='+o,true);x.send();}</script></body></html>
  """
  response = html_sequence
  cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
  cl.send(response)
  cl.close()







startServer()
listenToServer()



