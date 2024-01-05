from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QInputDialog
import subprocess

class UserGroupManagementModule(QWidget):
    def __init__(self, sudo_password):
        super(UserGroupManagementModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        add_user_button = QPushButton('Add User')
        add_user_button.clicked.connect(self.add_user)
        layout.addWidget(add_user_button)

        modify_user_button = QPushButton('Rename User')
        modify_user_button.clicked.connect(self.modify_user)
        layout.addWidget(modify_user_button)

        delete_user_button = QPushButton('Delete User')
        delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_user_button)

        add_group_button = QPushButton('Add Group')
        add_group_button.clicked.connect(self.add_group)
        layout.addWidget(add_group_button)

        modify_group_button = QPushButton('Rename Group')
        modify_group_button.clicked.connect(self.modify_group)
        layout.addWidget(modify_group_button)

        delete_group_button = QPushButton('Delete Group')
        delete_group_button.clicked.connect(self.delete_group)
        layout.addWidget(delete_group_button)

        change_group_button = QPushButton('Change Group Ownership')
        change_group_button.clicked.connect(self.change_group_ownership)
        layout.addWidget(change_group_button)

        change_passwd_button = QPushButton('Change User Password')
        change_passwd_button.clicked.connect(self.change_user_password)
        layout.addWidget(change_passwd_button)

        change_group_passwd_button = QPushButton('Change Group Password')
        change_group_passwd_button.clicked.connect(self.change_group_password)
        layout.addWidget(change_group_passwd_button)

        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"sudo -S bash -c '{command}'"
        process = subprocess.Popen(full_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)
        sudo_password = str(self.sudo_password) + '\n'
        stdout, stderr = process.communicate(input=sudo_password)

        if process.returncode == 0:
            self.result_label.setText(stdout)
        else:
            self.result_label.setText(f"Error: {stderr}")

    def add_user(self):
        username, ok = QInputDialog.getText(self, 'Add User', 'Enter the username:')
        if ok:
            self.run_script(f"sudo useradd -m {username}")
            QMessageBox.information(self, 'Success', f"User {username} added successfully.")

    def modify_user(self):
        old_username, ok = QInputDialog.getText(self, 'Modify User', 'Enter the current username to modify:')
        if ok:
            new_username, ok = QInputDialog.getText(self, 'Modify User', 'Enter the new username:')
            if ok:
                self.run_script(f"sudo usermod -l {new_username} {old_username}")
                QMessageBox.information(self, 'Success',
                                        f"User {old_username} modified to {new_username} successfully.")

    def delete_user(self):
        username, ok = QInputDialog.getText(self, 'Delete User', 'Enter the username to delete:')
        if ok:
            self.run_script(f"sudo userdel -r {username}")
            QMessageBox.information(self, 'Success', f"User {username} deleted successfully.")

    def add_group(self):
        groupname, ok = QInputDialog.getText(self, 'Add Group', 'Enter the group name:')
        if ok:
            self.run_script(f"sudo groupadd {groupname}")
            QMessageBox.information(self, 'Success', f"Group {groupname} added successfully.")

    def modify_group(self):
        old_groupname, ok = QInputDialog.getText(self, 'Modify Group', 'Enter the current group name to modify:')
        if ok:
            new_groupname, ok = QInputDialog.getText(self, 'Modify Group', 'Enter the new group name:')
            if ok:
                self.run_script(f"sudo groupmod -n {new_groupname} {old_groupname}")
                QMessageBox.information(self, 'Success',
                                        f"Group {old_groupname} modified to {new_groupname} successfully.")

    def delete_group(self):
        groupname, ok = QInputDialog.getText(self, 'Delete Group', 'Enter the group name to delete:')
        if ok:
            self.run_script(f"sudo groupdel {groupname}")
            QMessageBox.information(self, 'Success', f"Group {groupname} deleted successfully.")

    def change_group_ownership(self):
        groupname, ok1 = QInputDialog.getText(self, 'Change Group Ownership', 'Enter the group name:')
        path, ok2 = QInputDialog.getText(self, 'Change Group Ownership', 'Enter the file or directory path:')
        if ok1 and ok2:
            self.run_script(f"sudo chgrp {groupname} {path}")
            QMessageBox.information(self, 'Success', f"Group ownership of {path} changed to {groupname}.")

    def change_user_password(self):
        username, ok = QInputDialog.getText(self, 'Change User Password', 'Enter the username:')
        if ok:
            # Use QInputDialog for password input with EchoMode set to Password
            password, ok = QInputDialog.getText(self, 'Change User Password', 'Enter the new password:',
                                                QLineEdit.Password)
            if ok:
                # Use sudo passwd --stdin to set the user's password non-interactively
                self.run_script(f"echo '{password}' | sudo passwd --stdin {username}")
                QMessageBox.information(self, 'Success', f"Password for user {username} changed successfully.")

    def change_group_password(self):
        groupname, ok = QInputDialog.getText(self, 'Change Group Password', 'Enter the group name:')
        if ok:
            password, ok = QInputDialog.getText(self, 'Change Group Password', 'Enter the new password:')
            if ok:
                self.run_script(f"sudo gpasswd --delete {groupname} && sudo gpasswd {groupname}")
                QMessageBox.information(self, 'Success', f"Password for group {groupname} changed successfully.")
