import serial
import time

class UART:
    def __init__(self, port_name, timeout_value):
        self.port = port_name
        self.serial = serial.Serial(
            port=str(port_name),
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout_value)

        self.port_name = port_name

        # setup xmodem for image transfers
        self.modem = XMODEM(self.getc, self.putc)

    def getc(self, size, timeout=1):
        return self.serial(size) or None

    def putc(self, data, timeout=1):
        return self.serial.write(data) # note that this ignores the timeout

    def transfer_image(self):
        try:
            stream = open("~/images/image.jpg", 'wb')
            response = modem.recv(stream)
            if response is None:
                self.logger("Error xmodem reading stream: Got None return code.")
                return False
            else:
                return True, []
        except Exception as e:
            self.logger("Exception {} trying to read xmodem file stream: {}".format(type(e).__name__,str(e)))
            return False

    # send message to hardware over uart
    def write(self, message):
        try:
            # open uart port
            self.serial.close()
            self.serial.open()

            if self.serial.isOpen():
                # if uart port is open, try to send encoded string message
                self.serial.write(str(message).encode('utf-8'))
                self.serial.close()
                self.logger.debug("UART port {} is open. Sent message: {}".format(self.port, str(message)))
                return True
            else:
                # if could not open uart port, return failure
                self.serial.close()
                self.logger.warn("Could not open serial port: {}".format(self.port))
                return False

        # return failure if exception during write/encoding
        except Exception as e:
            self.logger.warn("Error sending message {} over uart port {}: {}".format(str(message), self.port, str(e)))
            return False

    # get message from hardware over uart
    def read(self):
        try:
            self.serial.close()
            self.serial.open()

            if self.serial.isOpen():
                # if uart port is open, try to read something
                message = self.serial.readline()
                message = message.decode('utf-8')
                self.logger.debug("Uart port {} is open. Read line: {}".format(message))
                self.serial.close()
                return True, message
            else:
                # if could not open uart port, return failure
                self.serial.close()
                self.logger.warn("Could not open serial port: {}".format(self.port))
                return False, None

        # return failure if exception during read/decoding
        except Exception as e:
            self.logger.warn("Error sending message over uart port {}: {}".format(self.port, str(e)))
            return False, None

class UART_fake:
    def __init__(self):
        pass
    
    def write(self, message):
        return True
    
    def read(self):
        return True, None

    def transfer_image(self):
        return True

UART_PORT = '/dev/ttyAMA0' 
TIMEOUT = 1
try:
    uart1 = UART(UART_PORT, TIMEOUT)
except serial.SerialException as e:
    uart1 = UART_fake()
