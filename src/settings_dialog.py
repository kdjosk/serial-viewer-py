from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QVBoxLayout,
    QDialogButtonBox,
    QComboBox,
    QCheckBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import (
    Slot,
    Qt,
    QSettings,
)
from serial_port import (
    SerialPortSettings,
    StandardBaudRates,  
    DataBits,
    ParityChecking,
    StopBits,
)

class OptionalDoubleSpinBox(QWidget):
    """A compound widget to handle an optional float value (None or a number)."""
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        
        self.checkbox = QCheckBox(text)
        self.spinbox = QDoubleSpinBox()
        
        self.spinbox.setRange(0.0, 10000.0) # Set a wide range
        self.spinbox.setDecimals(2) # Set precision
        self.spinbox.setValue(0.0)
        
        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.spinbox)
        self.setLayout(layout)
        
        # Connections
        self.checkbox.stateChanged.connect(self.update_spinbox_state)
        
        # Initial State
        self.checkbox.setChecked(False)
        self.update_spinbox_state()

    @Slot()
    def update_spinbox_state(self):
        """Enable or disable the spinbox based on the checkbox state."""
        is_enabled = self.checkbox.isChecked()
        self.spinbox.setEnabled(is_enabled)

    def value(self) -> float | None:
        """Return the float value if checked, otherwise None."""
        if self.checkbox.isChecked():
            return self.spinbox.value()
        return None

    def setValue(self, value: float | None):
        """Set the value of the widget."""
        if value is None:
            self.checkbox.setChecked(False)
        else:
            self.checkbox.setChecked(True)
            self.spinbox.setValue(value)


class TriStateCheckbox(QWidget):
    """A compound widget to handle an optional float value (None or a number)."""
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        
        self.checkbox = QCheckBox(text, self)
        self.checkbox.setTristate(True)

    def value(self) -> bool | None:
        """Return the float value if checked, otherwise None."""
        match self.checkbox.checkState():
            case Qt.CheckState.Checked:
                return True
            case Qt.CheckState.PartiallyChecked:
                return None
            case Qt.CheckState.Unchecked:
                return False

    def setValue(self, value: bool | None):
        """Set the value of the widget."""
        match value:
            case True:
                self.checkbox.setCheckState(Qt.CheckState.Checked)
            case False:
                self.checkbox.setCheckState(Qt.CheckState.Unchecked)
            case None:
                self.checkbox.setCheckState(Qt.CheckState.PartiallyChecked)


class SettingsDialog(QDialog):
    def __init__(self, current_settings: SerialPortSettings | None = None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        
        self.settings = SerialPortSettings.default() if current_settings is None else current_settings
        
        # Dialog buttons
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok 
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Create widgets
        self.baudrate_choice = QComboBox()
        self.baudrate_choice.addItems(
            [str(v) for v in StandardBaudRates]
        )
        self.baudrate_choice.setCurrentText(
            str(self.settings.baudrate)
        )
        
        self.bytesize_choice = QComboBox()
        self.bytesize_choice.addItems(
            [str(v) for v in DataBits]
        )
        self.bytesize_choice.setCurrentText(
            str(self.settings.bytesize)
        )

        self.parity_choice = QComboBox()
        self.parity_choice.addItems(
            [str(m.name).lower() for m in ParityChecking]
        )
        self.parity_choice.setCurrentText(
            str(self.settings.parity.name).lower()
        )

        self.stopbits_choice = QComboBox()
        self.stopbits_choice.addItems(
            [str(m.value) for m in StopBits]
        )
        self.stopbits_choice.setCurrentText(
            str(self.settings.stopbits.value)
        )

        self.timeout_choice = OptionalDoubleSpinBox("Enable")
        self.timeout_choice.setValue(self.settings.timeout)

        self.xonxoff_choice = QCheckBox("Enable")
        self.xonxoff_choice.setChecked(self.settings.xonxoff)

        self.rtscts_choice = QCheckBox("Enable")
        self.rtscts_choice.setChecked(self.settings.rtscts)

        self.dsrdtr_choice = QCheckBox("Enable")
        self.dsrdtr_choice.setChecked(self.settings.dsrdtr)

        self.write_timeout_choice = OptionalDoubleSpinBox("Enable")
        self.write_timeout_choice.setValue(self.settings.write_timeout)

        self.inter_byte_timeout_choice = OptionalDoubleSpinBox("Enable")
        self.inter_byte_timeout_choice.setValue(self.settings.inter_byte_timeout)

        self.exclusive_choice = TriStateCheckbox("Enable")
        self.exclusive_choice.setValue(self.settings.exclusive)

        # Set the layout
        form_layout = QFormLayout()
        form_layout.addRow("Baud rate", self.baudrate_choice)
        form_layout.addRow("Data bits", self.bytesize_choice)
        form_layout.addRow("Parity checking", self.parity_choice)
        form_layout.addRow("Stop bits", self.stopbits_choice)
        form_layout.addRow("Timeout", self.timeout_choice)
        form_layout.addRow("Software XON/XOFF", self.xonxoff_choice)
        form_layout.addRow("Hardware RTS/CTS", self.rtscts_choice)
        form_layout.addRow("Hardware DSR/DTR", self.dsrdtr_choice)
        form_layout.addRow("Write timeout", self.write_timeout_choice)
        form_layout.addRow("Inter byte timeout", self.inter_byte_timeout_choice)
        form_layout.addRow("Exclusive", self.exclusive_choice)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.buttonBox)

        self.setLayout(main_layout)

    def accept(self): 
        self.settings = SerialPortSettings(
            baudrate=int(self.baudrate_choice.currentText()),
            bytesize=DataBits(int(self.bytesize_choice.currentText())),
            parity=ParityChecking[self.parity_choice.currentText().upper()],
            stopbits=StopBits(float(self.stopbits_choice.currentText())),
            timeout=self.timeout_choice.value(),
            xonxoff=self.xonxoff_choice.isChecked(),
            rtscts=self.rtscts_choice.isChecked(),
            write_timeout=self.write_timeout_choice.value(),
            dsrdtr=self.dsrdtr_choice.isChecked(),
            inter_byte_timeout=self.inter_byte_timeout_choice.value(),
            exclusive=self.exclusive_choice.value(),
        )

        super().accept()


def save_serial_settings(settings: QSettings, config: SerialPortSettings):
    """Saves the SerialSettings dataclass into a settings group."""
    print("Saving serial settings...")
    settings.beginGroup("serial_port")
    
    settings.setValue("baudrate", config.baudrate)
    settings.setValue("bytesize", config.bytesize.name)
    settings.setValue("parity", config.parity.name)
    settings.setValue("stopbits", config.stopbits.name)
    settings.setValue("timeout", config.timeout)
    settings.setValue("xonxoff", config.xonxoff)
    settings.setValue("rtscts", config.rtscts)
    settings.setValue("write_timeout", config.write_timeout)
    settings.setValue("dsrdtr", config.dsrdtr)
    settings.setValue("inter_byte_timeout", config.inter_byte_timeout)
    settings.setValue("exclusive", config.exclusive)
    
    settings.endGroup()
    print("Settings saved.")


def load_serial_settings(settings: QSettings) -> SerialPortSettings:
    """Loads and reconstructs the SerialSettings dataclass from a settings group."""
    print("Loading serial settings...")
    settings.beginGroup("serial_port")
    
    # For nullable types, we get the value and check if it's valid.
    # QSettings returns None for missing keys or ones saved as None

    default = SerialPortSettings.default()
    timeout = settings.value("timeout", default.timeout)
    write_timeout = settings.value("write_timeout", default.write_timeout)
    inter_byte_timeout = settings.value("inter_byte_timeout", default.inter_byte_timeout)
    exclusive = settings.value("exclusive", default.exclusive)

    config = SerialPortSettings(
        baudrate=StandardBaudRates(settings.value("baudrate", default.baudrate, type=int)),
        bytesize=DataBits[settings.value("bytesize", default.bytesize, type=str)],
        parity=ParityChecking[settings.value("parity", default.parity, type=str)],
        stopbits=StopBits[settings.value("stopbits", default.stopbits, type=str)],
        timeout=float(timeout) if timeout is not None else None,
        xonxoff=settings.value("xonxoff", default.xonxoff, type=bool),
        rtscts=settings.value("rtscts", default.rtscts, type=bool),
        write_timeout=float(write_timeout) if write_timeout is not None else None,
        dsrdtr=settings.value("dsrdtr", default.dsrdtr, type=bool),
        inter_byte_timeout=float(inter_byte_timeout) if inter_byte_timeout is not None else None,
        exclusive=bool(exclusive) if exclusive is not None else None
    )
    settings.endGroup()
    print("Settings loaded.")
    return config