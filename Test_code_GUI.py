import time
from ID_Mapping_Test_UI import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import pyqtSignal, QThread
import socket

class UDPReceiver(QThread):
    data_received = pyqtSignal(str)  # 데이터 수신 시그널 정의

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('166.79.25.100', self.port))  # 12345 포트에서 수신
        self._running = True

    def run(self):
        while self._running:
            try :
                data, _ = self.sock.recvfrom(1024)  # 최대 1024바이트 수신
                self.data_received.emit(data.decode('utf-8'))  # 데이터 수신 시그널 발생
            except Exception as e :
                self.data_received.emit(f"Error: {str(e)}")
            time.sleep(0.1)

    def stop(self):
        self._running = False
        self.sock.close()

    def senddata(self, target: tuple, msg: str) -> None:
        self.sock.sendto(msg.encode(), target)


class MainGUI:
    def __init__(self):
        super().__init__()
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.update_widgets()
        self.MainWindow.show()
        self.currentTime = ''

        # region MainPC 에서 변수로 입력받을 레지스터, 데이터 주소
        self.adr_write1 = None
        self.adr_write2 = None
        self.adr_write3 = None
        self.adr_write4 = None
        self.adr_write5 = None
        self.adr_write6 = None
        self.adr_write7 = None
        self.adr_write8 = None
        self.adr_write9 = None
        self.adr_write10 = None
        self.adr_read1 = None
        self.adr_read2 = None
        self.adr_read3 = None
        self.adr_read4 = None
        self.adr_read5 = None
        self.adr_read6 = None
        self.adr_read7 = None
        self.adr_read8 = None
        self.adr_read9 = None
        self.adr_read10 = None

        self.data_write1 = None
        self.data_write2 = None
        self.data_write3 = None
        self.data_write4 = None
        self.data_write5 = None
        self.data_write6 = None
        self.data_write7 = None
        self.data_write8 = None
        self.data_write9 = None
        self.data_write10 = None
        self.data_read1 = None
        self.data_read2 = None
        self.data_read3 = None
        self.data_read4 = None
        self.data_read5 = None
        self.data_read6 = None
        self.data_read7 = None
        self.data_read8 = None
        self.data_read9 = None
        self.data_read10 = None

        # 16비트 data split을 위한 리스트 생성.
        self.adr_list = []

        self.high_adr_write1 = None
        self.low_adr_write1 = None
        self.high_adr_write2 = None
        self.low_adr_write2 = None
        self.high_adr_write3 = None
        self.low_adr_write3 = None
        self.high_adr_write4 = None
        self.low_adr_write4 = None
        self.high_adr_write5 = None
        self.low_adr_write5 = None
        self.high_adr_write6 = None
        self.low_adr_write6 = None
        self.high_adr_write7 = None
        self.low_adr_write7 = None
        self.high_adr_read1 = None
        self.low_adr_read1 = None
        self.high_adr_read2 = None
        self.low_adr_read2 = None
        self.high_adr_read3 = None
        self.low_adr_read3 = None
        self.high_adr_read4 = None
        self.low_adr_read4 = None
        self.high_adr_read5 = None
        self.low_adr_read5 = None
        self.high_adr_read6 = None
        self.low_adr_read6 = None
        self.high_adr_read7 = None
        self.low_adr_read7 = None

        # Main PC로부터 받은 바코드 정보
        self.barcode = None

        # 취득한 Sensor ID 변수 : 두번 확인해서 비교해야 하므로 2개씩 할당
        self.SensorID1 = None
        self.SensorID2 = None

        # MainPC 에서 변수로 입력받을 Slave address
        self.Slave_sensor = None
        self.Slave_eeprom = None
        self.Slave_AFDriverIC = None
        self.Slave_OISDriverIC = None
        self.Slave_str = ''
        # end region

        # 연속실행 변수
        self.isExecProcess = False
        self.writeCardIp = '166.79.25.110'
        self.writeCardIpPort = ('166.79.25.110', 6561)

        # region button clicked
        self.ui.pushButton_Load_Model_data.clicked.connect(self.read_Sensor_info)

        # txt 파일로부터 읽어오는 Info 변수
        self.file_open = None
        self.All_Info_data = None

    # txt 파일로부터 읽어온 Info 리스트를 각 변수에 할당
    def read_Sensor_info(self):
        self.file_open = open('Sensor Info.txt', 'r')
        self.All_Info_data = self.file_open.readlines()
        self.file_open.close()
        print(self.All_Info_data)


    def send_slave(self):
        self.Slave_sensor =
        self.Slave_eeprom =
        self.Slave_AFDriverIC =
        self.Slave_OISDriverIC =

        sender = UDPReceiver(self.writeCardIp, 6561)
        sender.senddata(self.writeCardIpPort, self.Slave_str)

    def send_sensor_res(self):
        self.adr_write1 =
        self.adr_write2 =
        self.adr_write3 =
        self.adr_write4 =
        self.adr_write5 =
        pass

    def send_EEPROM(self):
        pass

    def get_sensorID(self):
        pass





    def split_16bit_data(data_list):
        result = []

        for value in data_list:
            if value is not None:
                high_byte = (value >> 8) & 0xFF
                low_byte = value & 0xFF
                result.append((high_byte, low_byte))
            return result



    # Region 16비트 데이터를 상위와 하위 바이트로 분리
    def data_devide(self):
         try:
             self.high_adr_write1 = (self.adr_write1 >>8 ) & 0xFF
             self.low_adr_write1 = self.adr_write1 & 0xFF
         except Exception as e:
             print("I2C 통신 오류", e)

    def data_HighLow(self):
        pass

    def update_widgets(self):
        self.MainWindow.setWindowTitle('PyQt5 GUI')

