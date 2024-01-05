from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QInputDialog
import subprocess
import os

class CryptographyModule(QWidget):
    def __init__(self, sudo_password):
        super(CryptographyModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        self.filename_edit = QLineEdit()
        layout.addWidget(self.filename_edit)

        select_file_button = QPushButton('Select File')
        select_file_button.clicked.connect(self.select_file)
        layout.addWidget(select_file_button)

        self.encrypt_button = QPushButton('Encrypt')
        self.encrypt_button.clicked.connect(self.run_encrypt_script)
        self.encrypt_button.setEnabled(False)  # Initially, set the "Encrypt" button as disabled
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Decrypt')
        self.decrypt_button.clicked.connect(self.run_decrypt_script)
        self.decrypt_button.setEnabled(False)  # Initially, set the "Decrypt" button as disabled
        layout.addWidget(self.decrypt_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filename, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt);;Python Files (*.py)", options=options)
        if filename:
            self.filename_edit.setText(filename)
            self.encrypt_button.setEnabled(True)  # Enable the "Encrypt" button
            self.decrypt_button.setEnabled(True)  # Enable the "Decrypt" button

    def run_script(self, command, input_text=None):
        full_command = f"echo {self.sudo_password} | sudo -S {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True, input=input_text)

        if result.returncode == 0:
            self.result_label.setText(result.stdout)
        else:
            error_message = f"Error ({result.returncode}): {result.stderr}"
            self.result_label.setText(error_message)

    def run_encrypt_script(self):
        filename = self.filename_edit.text()

        # Check if the filename is provided
        if not filename:
            self.result_label.setText("Please select a file.")
            return

        # Get the GnuPG passphrase from the user
        passphrase, ok = QInputDialog.getText(self, 'Enter GnuPG Passphrase', 'Please enter the GnuPG passphrase:', echo=QLineEdit.Password)

        if ok:
            # Encrypt the file using GPG
            encrypt_command = f'gpg --passphrase "{passphrase}" --output "{filename}.gpg" --symmetric --batch --yes "{filename}"'
            self.run_script(encrypt_command)

            # Delete the original file if encryption is successful
            if os.path.exists(filename):
                os.remove(filename)
                self.result_label.setText(f"File '{filename}' successfully encrypted.")
        else:
            self.result_label.setText("Encryption cancelled.")

    def run_decrypt_script(self):
        filename = self.filename_edit.text()

        # Check if the filename is provided
        if not filename:
            self.result_label.setText("Please select a file.")
            return

        # Get the GnuPG passphrase from the user
        passphrase, ok = QInputDialog.getText(self, 'Enter GnuPG Passphrase', 'Please enter the GnuPG passphrase:', echo=QLineEdit.Password)

        if ok:
            # Decrypt the file using GPG
            decrypt_command = f'gpg --passphrase "{passphrase}" --output "{filename[:-4]}" --decrypt --batch --yes "{filename}"'
            self.run_script(decrypt_command)

            # Delete the encrypted file if decryption is successful
            if os.path.exists(f"{filename[:-4]}"):
                os.remove(filename)
                self.result_label.setText(f"File '{filename}' successfully decrypted.")
        else:
            self.result_label.setText("Decryption cancelled.")
