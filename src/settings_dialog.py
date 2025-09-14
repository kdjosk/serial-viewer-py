from PySide6.QtWidgets import (
    QDialog,
    QTabWidget,
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
)
from port_settings_tab import PortSettingsWidget


class SettingsDialog(QDialog):
    def __init__(self, port_settings: SerialPortSettings | None = None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")

        self.tabWidget = QTabWidget(self)

        self.portSettings = PortSettingsWidget(port_settings)

        self.tabWidget.addTab(self.portSettings, "Port Settings")

        # Dialog buttons
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok 
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.restoreDefualtsButton = self.buttonBox.button(
            QDialogButtonBox.StandardButton.RestoreDefaults
        )
        self.restoreDefualtsButton.pressed.connect(self.handle_restore_defaults)

        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
   
    def handle_restore_defaults(self):
        self.portSettings.handle_restore_defaults()

    def accept(self) -> None:
        self.settings = self.portSettings.get_settings()

        return super().accept()