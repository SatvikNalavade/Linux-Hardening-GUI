from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit
from subprocess import Popen, PIPE

def run_sudo_script(password):
    # Replace the following command with your actual sudo script
    # For example, running 'echo $USER' as a sample script
    command = f'echo {password} | sudo -S echo $USER'

    # Run the sudo command
    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    output, error = process.communicate()

    # Check if the sudo script executed successfully
    if process.returncode == 0:
        return True
    else:
        return False

def get_sudo_password():
    # Ask user for sudo password
    password = 'your_default_password'  # Set a default password if needed
    while True:
        password, ok = QInputDialog.getText(None, 'Enter Sudo Password', 'Please enter your sudo password:', QLineEdit.Password)
        if not ok:
            # Handle case when the user cancels the input dialog
            return None

        # Check the password with the sudo script
        if run_sudo_script(password):
            return password
        else:
            QMessageBox.warning(None, 'Fail to Login', 'Fail to login. Please re-enter your sudo password.')
