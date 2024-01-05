from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QPlainTextEdit
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess


class UpdateThread(QThread):
    log_received = pyqtSignal(str)

    def __init__(self, sudo_password):
        super(UpdateThread, self).__init__()
        self.sudo_password = sudo_password

    def run(self):
        command = f"echo {self.sudo_password} | sudo -S apt update"
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        while process.poll() is None:
            line = process.stdout.readline().strip()
            self.log_received.emit(line)

        if process.returncode == 0:
            self.log_received.emit(f"Update completed successfully.")
        else:
            self.log_received.emit(f"Error: Update failed with return code {process.returncode}.")


class UpgradeThread(QThread):
    log_received = pyqtSignal(str)

    def __init__(self, sudo_password):
        super(UpgradeThread, self).__init__()
        self.sudo_password = sudo_password

    def run(self):
        command = f"echo {self.sudo_password} | sudo -S apt upgrade -y"
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        while process.poll() is None:
            line = process.stdout.readline().strip()
            self.log_received.emit(line)

        if process.returncode == 0:
            self.log_received.emit(f"Upgrade completed successfully.")
        else:
            self.log_received.emit(f"Error: Upgrade failed with return code {process.returncode}.")

class PatchManagementModule(QWidget):
    def __init__(self, sudo_password):
        super(PatchManagementModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        update_button = QPushButton('Update')
        update_button.clicked.connect(self.run_update_script)
        layout.addWidget(update_button)

        upgrade_button = QPushButton('Upgrade')
        upgrade_button.clicked.connect(self.run_upgrade_script)
        layout.addWidget(upgrade_button)

        clear_cache_button = QPushButton('Free Disk Space and Clear Cache')
        clear_cache_button.clicked.connect(self.run_clear_cache_script)
        layout.addWidget(clear_cache_button)

        autoremove_button = QPushButton('Remove Orphaned Dependencies')
        autoremove_button.clicked.connect(self.run_autoremove_script)
        layout.addWidget(autoremove_button)

        self.log_textbox = QPlainTextEdit()
        self.log_textbox.setStyleSheet("color: #3498db")  # Set text color to blue
        layout.addWidget(self.log_textbox)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"echo {self.sudo_password} | sudo -S {command}"
        process = subprocess.Popen(
            full_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        while process.poll() is None:
            line = process.stdout.readline().strip()
            self.log_textbox.appendPlainText(line)

        if process.returncode == 0:
            self.log_textbox.appendPlainText(f"{command} completed successfully.")
        else:
            self.log_textbox.appendPlainText(f"Error: {command} failed with return code {process.returncode}.")

    def run_update_script(self):
        self.update_thread = UpdateThread(self.sudo_password)
        self.update_thread.log_received.connect(self.handle_log_received)
        self.update_thread.start()

    def run_upgrade_script(self):
        self.upgrade_thread = UpgradeThread(self.sudo_password)
        self.upgrade_thread.log_received.connect(self.handle_log_received)
        self.upgrade_thread.start()

    def handle_log_received(self, log_line):
        self.log_textbox.appendPlainText(log_line)

    def run_clear_cache_script(self):
        self.run_script("apt clean")

    def run_autoremove_script(self):
        self.run_script("apt autoremove --purge -y")
