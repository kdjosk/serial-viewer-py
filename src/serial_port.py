from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from dataclasses import dataclass
import random
import time

import serial

class SerialPort(ABC):

    @abstractmethod
    def read_byte(self) -> bytes: ...

    @abstractmethod
    def send_line(self, line: str) -> None: ...


class StandardBaudRates(IntEnum):
    """
    An enumeration of standard serial communication baud rates.
    
    The member names follow the clib termios convention (B prefix).
    The member values are the integer baud rates.
    """
    # Well-supported standard values on all platforms
    B50 = 50
    B75 = 75
    B110 = 110
    B134 = 134
    B150 = 150
    B200 = 200
    B300 = 300
    B600 = 600
    B1200 = 1200
    B1800 = 1800
    B2400 = 2400
    B4800 = 4800
    B9600 = 9600
    B19200 = 19200
    B38400 = 38400
    B57600 = 57600
    B115200 = 115200

    # Extended values that work on many platforms and devices
    B230400 = 230400
    B460800 = 460800
    B500000 = 500000
    B576000 = 576000
    B921600 = 921600
    B1000000 = 1000000
    B1152000 = 1152000
    B1500000 = 1500000
    B2000000 = 2000000
    B2500000 = 2500000
    B3000000 = 3000000
    B3500000 = 3500000
    B4000000 = 4000000


class DataBits(IntEnum):
    FIVE = serial.FIVEBITS
    SIX = serial.SIXBITS
    SEVEN = serial.SEVENBITS
    EIGHT = serial.EIGHTBITS


class ParityChecking(Enum):
    NONE = serial.PARITY_NONE
    EVEN = serial.PARITY_EVEN
    ODD = serial.PARITY_ODD
    MARK = serial.PARITY_MARK
    SPACE = serial.PARITY_SPACE


class StopBits(Enum):
    ONE = serial.STOPBITS_ONE
    ONE_POINT_FIVE = serial.STOPBITS_ONE_POINT_FIVE
    TWO = serial.STOPBITS_TWO


@dataclass
class SerialPortSettings:
    """
    Configuration settings for a serial port connection.

    Attributes:        
        baudrate (int): 
            The baud rate for the connection. Common values include 9600, 19200, 115200, etc.
        
        bytesize (int): 
            Number of data bits. 
            Possible values (usually from serial module constants): 
            FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS.
        
        parity (str): 
            Parity checking mode. 
            Possible values: 'PARITY_NONE', 'PARITY_EVEN', 'PARITY_ODD', 'PARITY_MARK', 'PARITY_SPACE'.
        
        stopbits (float): 
            Number of stop bits. 
            Possible values: STOPBITS_ONE (1), STOPBITS_ONE_POINT_FIVE (1.5), STOPBITS_TWO (2).
        
        timeout (float | None): 
            Read timeout in seconds. 
            Use None for blocking mode, or a float value to specify a timeout.
        
        xonxoff (bool): 
            Whether software flow control (XON/XOFF) is enabled.
        
        rtscts (bool): 
            Whether hardware RTS/CTS flow control is enabled.
        
        dsrdtr (bool): 
            Whether hardware DSR/DTR flow control is enabled.
        
        write_timeout (float | None): 
            Timeout for write operations in seconds. 
            Use None for blocking writes.
        
        inter_byte_timeout (float | None): 
            Inter-character timeout in seconds. 
            Use None to disable.
        
        exclusive (bool | None): 
            Set exclusive access mode to the port. 
            Not all platforms support this. Use None to leave at default behavior.
    """

    baudrate: int
    bytesize: DataBits
    parity: ParityChecking
    stopbits: StopBits
    timeout: float | None
    xonxoff: bool
    rtscts: bool
    write_timeout: float | None
    dsrdtr: bool
    inter_byte_timeout: float | None
    exclusive: bool | None

    @staticmethod
    def default() -> SerialPortSettings:
        return SerialPortSettings(
            baudrate=StandardBaudRates.B9600,
            bytesize=DataBits.EIGHT,
            parity=ParityChecking.NONE,
            stopbits=StopBits.ONE,
            timeout=None,
            xonxoff=False,
            rtscts=False,
            write_timeout=None,
            dsrdtr=False,
            inter_byte_timeout=None,
            exclusive=None,
        )


class RealSerialPort(SerialPort):

    def __init__(self, port: str, settings: SerialPortSettings) -> None:
        self._port = serial.Serial(
            port=port,
            baudrate=settings.baudrate,
            bytesize=settings.bytesize.value,
            parity=settings.parity.value,
            stopbits=settings.stopbits.value,
            timeout=settings.timeout,
            xonxoff=settings.xonxoff,
            rtscts=settings.rtscts,
            write_timeout=settings.write_timeout,
            dsrdtr=settings.dsrdtr,
            inter_byte_timeout=settings.inter_byte_timeout,
            exclusive=settings.exclusive,
        )

    def set_port(self, port: str) -> None:
        """ Will open the port with the new setting """
        self._port.port = port

    def read_byte(self) -> bytes:
        return self._port.read(size=1)
    
    def send_line(self, line: str) -> None:
        self._port.write(line.encode())
    

class FakeSerialPort(SerialPort):
    def read_byte(self) -> bytes:
        time.sleep(0.01)
        ascii_chars = list(range(32, 126))
        return bytes(
            [random.choice(ascii_chars + [10])]
        )
    
    def send_line(self, line: str) -> None:
        print(line.encode())
