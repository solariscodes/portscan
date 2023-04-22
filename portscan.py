import sys
import socket
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar, QRadioButton, QGroupBox, QGridLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class SocketThread(QThread):
    update_progress = pyqtSignal(int)
    update_result = pyqtSignal(str)

    def __init__(self, ip, protocol, port_range, max_workers=100):
        super(SocketThread, self).__init__()
        self.ip = ip
        self.protocol = protocol
        self.start_port, self.end_port = map(int, port_range.split('-'))
        self.max_workers = max_workers
        self.completed_ports = 0

    def check_port(self, port):
        try:
            if self.protocol == 'TCP':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.ip, port))
                sock.close()
                if result == 0:
                    response = f'Port {port}: OPEN'
                    self.update_result.emit(response)
        except Exception as e:
            pass
        finally:
            self.completed_ports += 1
            progress = int(self.completed_ports / (self.end_port - self.start_port + 1) * 100)
            self.update_progress.emit(progress)

    def run(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.check_port, port) for port in range(self.start_port, self.end_port+1)]

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TCP/UDP Socket Tester')

        layout = QVBoxLayout()

        self.label = QLabel('IP Address:')
        layout.addWidget(self.label)

        self.ip_input = QLineEdit()
        layout.addWidget(self.ip_input)

        self.port_label = QLabel('Port Range (start-end):')
        layout.addWidget(self.port_label)

        self.port_input = QLineEdit()
        layout.addWidget(self.port_input)

        self.protocol_group = QGroupBox("Protocol")
        self.protocol_layout = QGridLayout()
        self.tcp_radio = QRadioButton("TCP")
        self.udp_radio = QRadioButton("UDP")
        self.tcp_radio.setChecked(True)
        self.protocol_layout.addWidget(self.tcp_radio, 0, 0)
        self.protocol_layout.addWidget(self.udp_radio, 0, 1)
        self.protocol_group.setLayout(self.protocol_layout)
        layout.addWidget(self.protocol_group)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.check_button = QPushButton('Check Connection')
        self.check_button.clicked.connect(self.check_connection)
        layout.addWidget(self.check_button)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def check_connection(self):
        ip = self.ip_input.text()
        port_range = self.port_input.text()
        protocol = 'TCP' if self.tcp_radio.isChecked() else 'UDP'
        self.progress.setValue(0)
        self.result.clear()
        self.result.append(f'Checking {protocol} connection to {ip} on ports {port_range}...')

        self.thread = SocketThread(ip, protocol, port_range)
        self.thread.update_progress.connect(self.progress.setValue)
        self.thread.update_result.connect(self.show_result)
        self.thread.start()

    def show_result(self, response):
        self.result.append(f'{response}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
