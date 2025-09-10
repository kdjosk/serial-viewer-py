from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
import random

import serial

class SerialPort(ABC):

    @abstractmethod
    def read_byte(self) -> bytes: ...


class DataBits(Enum):
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
        port (str | None): 
            Device name (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Unix) or None to leave unspecified.
        
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

    port: str | None
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
    def default(port: str | None) -> SerialPortSettings:
        return SerialPortSettings(
            port=port,
            baudrate=9600,
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

    def __init__(self, settings: SerialPortSettings) -> None:
        self._port = serial.Serial(
            port=settings.port,
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
    

class FakeSerialPort(SerialPort):
    def read_byte(self) -> bytes:
        return bytes([random.randint(32, 126)])
