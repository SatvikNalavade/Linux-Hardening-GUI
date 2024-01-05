from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
import subprocess
import hashlib

class FileIntegrityCheckModule(QWidget):
    def __init__(self, sudo_password=None):
        super(FileIntegrityCheckModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        selectFile_button = QPushButton('Select File')
        selectFile_button.clicked.connect(self.select_file)
        layout.addWidget(selectFile_button)

        checkIntegrity_button = QPushButton('Check File Integrity')
        checkIntegrity_button.clicked.connect(self.run_integrity_check)
        layout.addWidget(checkIntegrity_button)

        self.result_label = QLabel('')  # Label to display the result of the integrity check
        layout.addWidget(self.result_label)

        self.selected_file_path = ''  # Store the selected file path

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")
        if file_dialog.exec_():
            self.selected_file_path = file_dialog.selectedFiles()[0]
            self.result_label.setText(f'Selected File: {self.selected_file_path}')

    def run_integrity_check(self):
        if not self.selected_file_path:
            self.result_label.setText('Please select a file first.')
            return

        command = f'sha256sum "{self.selected_file_path}" > "{self.selected_file_path}.sha256"'
        process = subprocess.Popen(self.get_command_with_sudo(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            self.result_label.setText(f'File integrity checksum generated: {self.selected_file_path}.sha256')
            self.compare_checksums()
        else:
            self.result_label.setText(f'Error generating checksum: {stderr}')

    def get_command_with_sudo(self, command):
        if self.sudo_password:
            return f"echo '{self.sudo_password}' | sudo -S bash -c '{command}'"
        return command

    def compare_checksums(self):
        generated_checksum = ''
        try:
            with open(f'{self.selected_file_path}.sha256', 'r') as file:
                generated_checksum = file.read().split()[0]
        except FileNotFoundError:
            self.result_label.setText('Error: Generated checksum file not found.')
            return

        current_checksum = self.compute_file_checksum(self.selected_file_path)

        print(f'Generated Checksum: {generated_checksum}')
        print(f'Current Checksum: {current_checksum}')

        if generated_checksum == current_checksum:
            self.result_label.setText('File integrity check passed. No changes detected.')
        else:
            self.result_label.setText('File integrity check failed. Changes detected.')

    def compute_file_checksum(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

