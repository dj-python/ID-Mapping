import time
from ID_Mapping_Test_UI import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import pyqtSignal, QThread
import socket


# 이 프로그램은 TCP 통신의 서버임.

class UDPReceiver(QThread):
    data_received = pyqtSignal(str)  # 데이터 수신 시그널 정의

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('166.79.25.100', self.port))                     # 12345 포트에서 수신
        self.sock.listen(1)                                              # 연결 대기
        self.conn = None

    def receive_data(self):
        self.conn, addr = self.sock.accept()                                     # 클라이언트 연결 수락
        while self._running:
            try :
                data = self.conn.recv(1024)                           # 최대 1024바이트 수신
                if not data :
                    break
                self.data_received.emit(data.decode('utf-8'))                # 데이터 수신 시그널 발생
            except Exception as e :
                self.data_received.emit(f"Error: {str(e)}")
            time.sleep(0.1)
        self.conn.close()

    def stop(self):
        self._running = False
        if self.conn:
            self.conn.close()
        self.sock.close()

    def send_data(self, target: tuple, msg: str) -> None:
        try :
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           # 서버 소켓과 데이터 전송 소켓을 분리하기 위해 별도 변수 사용.
            temp_sock.connect(target)
            temp_sock.sendall(msg.encode())
            temp_sock.close()
        except Exception as e :
            print(f"Error : {str(e)}")




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

        sys.exit(app.exec_())


    # txt 파일로부터 읽어온 Info 리스트를 각 변수에 할당
    def read_Sensor_info(self):
        self.file_open = open('Sensor Info.txt', 'r')
        self.All_Info_data = self.file_open.readlines()
        self.file_open.close()
        print(self.All_Info_data)

    # 텍스트 파일에서 '0x' 이후의 문자열만 추출하여 변수에 저장
        if '0x' in self.All_Info_data[4]:
            # '0x' 이후의 두 문자 추출
            start_index1 = self.All_Info_data[4].index('0x')
            d = self.All_Info_data[4][start_index1:start_index1 + 2]
            print(d)
            self.Slave_sensor = self.All_Info_data[4][-5:-1]
        else:
            print('조건이 충족되지 않았습니다')

        if '0x' in self.All_Info_data[5]:
            # '0x' 이후의 두 문자 추출
            start_index2 = self.All_Info_data[5].index('0x')
            d = self.All_Info_data[5][start_index2:start_index2 + 2]
            print(d)
            self.Slave_eeprom = self.All_Info_data[5][-5:-1]
        else:
            print('조건이 충족되지 않았습니다')



        self.Slave_sensor = self.All_Info_data[4][-5:-1]
        self.Slave_eeprom = self.All_Info_data[5][-5:-1]
        self.Slave_AFDriverIC = self.All_Info_data[6][-5:-1]
        self.Slave_OISDriverIC = self.All_Info_data[7][-5:-1]
        self.Slave_str = self.Slave_sensor + self.Slave_eeprom + self.Slave_AFDriverIC + self.Slave_OISDriverIC

        self.adr_write1 = self.All_Info_data[13][-5:-1]
        self.adr_write2 = self.All_Info_data[14][-5:-1]
        self.adr_write3 = self.All_Info_data[15][-5:-1]
        self.adr_write4 = self.All_Info_data[16][-5:-1]
        self.adr_write5 = self.All_Info_data[17][-5:-1]

        sender = UDPReceiver(self.writeCardIp, 6561)
        sender.senddata(self.writeCardIpPort, self.Slave_str)


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
