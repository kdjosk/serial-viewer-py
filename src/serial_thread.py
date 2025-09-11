from PySide6.QtCore import QThread, Signal, Slot

import time
from serial_port import SerialPort

class SerialThread(QThread):

    new_data = Signal(str)
    
    def __init__(self, port: SerialPort):
        super().__init__()
        self._port = port
        self._shutdown_set = False
        self._is_paused = False

    def run(self):
        while not self._shutdown_set:

            while self._is_paused:
                if self._shutdown_set:
                    return
                time.sleep(0.1)

            byte = self._port.read_byte()
            self.new_data.emit(byte.decode())

    @Slot()
    def shutdown(self):
        self._shutdown_set = True

    @Slot()
    def pause(self):
        self._is_paused = True

    @Slot()
    def resume(self):
        self._is_paused = False

    def is_paused(self) -> bool:
        return self._is_paused