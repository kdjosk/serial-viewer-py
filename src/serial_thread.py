from PySide6.QtCore import QThread, Signal, Slot
from queue import Queue

import time
from serial_port import SerialPort

class SerialThread(QThread):

    new_data = Signal(str)
    
    def __init__(self, port: SerialPort):
        super().__init__()
        self._port = port
        self._shutdown_rq = False
        self._pause_rq = False
        self._is_paused = False
        self._lines_to_send = Queue()

    def run(self):
        while not self._shutdown_rq:

            while self._pause_rq:
                self._is_paused = True
                if self._shutdown_rq:
                    return
                time.sleep(0.1)

            self._is_paused = False

            while not self._lines_to_send.empty():
                self._port.send_line(self._lines_to_send.get())

            byte = self._port.read_byte()
            self.new_data.emit(byte.decode())

    @Slot()
    def shutdown(self):
        self._shutdown_rq = True

    @Slot()
    def pause(self):
        self._pause_rq = True

    @Slot()
    def resume(self, new_port: SerialPort | None):
        if new_port is not None:
            self._port = new_port
        self._pause_rq = False

    @Slot(str)
    def send_line(self, line: str):
        self._lines_to_send.put(line)

    def is_paused(self) -> bool:
        return self._is_paused