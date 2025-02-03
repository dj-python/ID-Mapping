import time
from ID_Mapping_Test_UI import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import pyqtSignal, QThread
import socket


# 이 프로그램은 TCP 통신의 서버임.

class TCPReceiver(QThread):
    data_received = pyqtSignal(str)  # 데이터 수신 시그널 정의

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self._running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('166.79.25.100', self.port))                     # 12345 포트에서 수신
        self.sock.listen(1)                                              # 연결 대기
        self.conn = None

    def run(self):
        try:
            print(f"[*] TCP 서버 대기 중... ({self.ip}:{self.port}")
            self.conn, addr = self.sock.accept()
            print(f"[+] 클라이언트 연결됨: {addr}")
            while self._running:
                try :
                    data = self.conn.recv(1024)                           # 최대 1024바이트 수신
                    if not data :
                        break
                    self.data_received.emit(data.decode('utf-8'))                # 데이터 수신 시그널 발생
                except Exception as e :
                    self.data_received.emit(f"Error: {str(e)}")
                time.sleep(0.1)
        except Exception as e :
            print(f"Error in TCP server: {str(e)}")
        finally :
            if self.conn:
                self.conn.close()
            self.sock.close()

    def stop(self):
        self._running = False
        if self.conn:
            self.conn.close()
        self.sock.close()
        print("[*] TCP 서버 종료")

    def send_data(self, target: tuple, msg: str) -> None:
        try :
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           # 서버 소켓과 데이터 전송 소켓을 분리하기 위해 별도 변수 사용.
            temp_sock.connect(target)
            temp_sock.sendall(msg.encode())
            temp_sock.close()
            print(f"[+] 데이터 전송 완료: {msg}")
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
        self.Sensor_Streaming_Resister_Address1 = None
        self.Sensor_Streaming_Resister_Address2 = None
        self.Sensor_Streaming_Resister_Address3 = None
        self.Sensor_Streaming_Resister_Address4 = None
        self.Sensor_Streaming_Resister_Address5 = None
        self.Sensor_Streaming_Resister = ''

        self.Sensor_Streaming_Write_Data1 = None
        self.Sensor_Streaming_Write_Data2 = None
        self.Sensor_Streaming_Write_Data3 = None
        self.Sensor_Streaming_Write_Data4 = None
        self.Sensor_Streaming_Write_Data5 = None
        self.Sensor_Streaming_Data = ''

        self.Sensor_Reading_Resister_Address1 = None
        self.Sensor_Reading_Resister_Address2 = None
        self.Sensor_Reading_Resister_Address3 = None

        self.Sensor_Write_Resister_Address1 = None
        self.Sensor_Write_Resister_Address2 = None
        self.Sensor_Write_Resister_Address3 = None
        self.Sensor_Write_Resister_Address4 = None
        self.Sensor_Write_Resister_Address5 = None

        self.Sensor_Write_Data1 = None
        self.Sensor_Write_Data2 = None
        self.Sensor_Write_Data3 = None
        self.Sensor_Write_Data4 = None
        self.Sensor_Write_Data5 = None

        self.Sensor_Read_Resister1 = None
        self.Sensor_Read_Resister2 = None
        self.Sensor_Read_Resister3 = None
        self.Sensor_Read_Resister4 = None
        self.Sensor_Read_Resister5 = None
        self.Sensor_Read_Resister6 = None
        self.Sensor_Read_Resister7 = None

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
        self.ui.pushButton_Get_SensorID.clicked.connect(self.Get_Sensor_ID)
        self.ui.pushButton_Write_EEPROM.clicked.connect(self.Write_EEPROM)
        self.ui.pushButton_Check_EEPROM.clicked.connect(self.Check_EEPROM)

        # txt 파일로부터 읽어오는 Info 변수
        self.file_open = None
        self.All_Info_data = None

        sys.exit(app.exec_())

    # txt 파일로부터 읽어온 Info 리스트를 각 변수에 할당
    def read_Sensor_info(self, index):
        self.file_open = open('Sensor Info.txt', 'r')
        self.All_Info_data = self.file_open.readlines()
        self.file_open.close()
        print(self.All_Info_data)

    # 텍스트 파일에서 '0x' 이후의 문자열만 추출하여 변수에 저장
        if '0x' in self.All_Info_data[index]:
            start_index = self.All_Info_data[index].index('0x')
            extracted_value = self.All_Info_data[index][start_index+2:start_index+4]
            if extracted_value is not None:
                print(extracted_value)
                return extracted_value
            else :
                pass
        else :
            print('조건이 충족되지 않았습니다')

    def load_model_data(self):
        self.Slave_sensor = self.read_Sensor_info(4)
        self.Slave_eeprom = self.read_Sensor_info(5)
        self.Slave_AFDriverIC = self.read_Sensor_info(6)
        self.Slave_OISDriverIC = self.read_Sensor_info(7)

        self.Sensor_Streaming_Resister_Address1 = self.read_Sensor_info(13)
        self.Sensor_Streaming_Resister_Address2 = self.read_Sensor_info(14)
        self.Sensor_Streaming_Resister_Address3 = self.read_Sensor_info(15)
        self.Sensor_Streaming_Resister_Address4 = self.read_Sensor_info(16)
        self.Sensor_Streaming_Resister_Address5 = self.read_Sensor_info(17)

        self.Sensor_Streaming_Write_Data1 = self.read_Sensor_info(19)
        self.Sensor_Streaming_Write_Data2 = self.read_Sensor_info(20)
        self.Sensor_Streaming_Write_Data3 = self.read_Sensor_info(21)
        self.Sensor_Streaming_Write_Data4 = self.read_Sensor_info(22)
        self.Sensor_Streaming_Write_Data5 = self.read_Sensor_info(23)

        self.Sensor_Reading_Resister_Address1 = self.read_Sensor_info(25)
        self.Sensor_Reading_Resister_Address2 = self.read_Sensor_info(26)
        self.Sensor_Reading_Resister_Address3 = self.read_Sensor_info(27)

        self.Sensor_Write_Data1 = self.read_Sensor_info(32)
        self.Sensor_Write_Data2 = self.read_Sensor_info(33)
        self.Sensor_Write_Data3 = self.read_Sensor_info(34)
        self.Sensor_Write_Data4 = self.read_Sensor_info(35)
        self.Sensor_Write_Data5 = self.read_Sensor_info(36)

        self.Sensor_Read_Resister1 = self.read_Sensor_info(37)
        self.Sensor_Read_Resister2 = self.read_Sensor_info(38)
        self.Sensor_Read_Resister3 = self.read_Sensor_info(39)
        self.Sensor_Read_Resister4 = self.read_Sensor_info(40)
        self.Sensor_Read_Resister5 = self.read_Sensor_info(41)
        self.Sensor_Read_Resister6 = self.read_Sensor_info(42)
        self.Sensor_Read_Resister7 = self.read_Sensor_info(43)

        self.ui.textBrowser_model_data.append('Slave_sensor' + self.Slave_sensor)
        self.ui.textBrowser_model_data.append('Slave_eeprom' + self.Slave_eeprom)
        self.ui.textBrowser_model_data.append('Slave_AF Driver' + self.Slave_AFDriverIC)
        self.ui.textBrowser_model_data.append('Slave_OIS Driver' + self.Slave_OISDriverIC)
        self.ui.textBrowser_model_data.append('Sensor Streaming Resister Address 1' + self.Sensor_Streaming_Resister_Address1)
        self.ui.textBrowser_model_data.append('Sensor Streaming Resister Address 2' + self.Sensor_Streaming_Resister_Address2)
        self.ui.textBrowser_model_data.append('Sensor Streaming Resister Address 3' + self.Sensor_Streaming_Resister_Address3)
        self.ui.textBrowser_model_data.append('Sensor Streaming Resister Address 4' + self.Sensor_Streaming_Resister_Address4)
        self.ui.textBrowser_model_data.append('Sensor Streaming Resister Address 5' + self.Sensor_Streaming_Resister_Address5)
        self.ui.textBrowser_model_data.append('Sensor Streaming Data 1' + self.Sensor_Streaming_Write_Data1)
        self.ui.textBrowser_model_data.append('Sensor Streaming Data 2' + self.Sensor_Streaming_Write_Data2)
        self.ui.textBrowser_model_data.append('Sensor Streaming Data 3' + self.Sensor_Streaming_Write_Data3)
        self.ui.textBrowser_model_data.append('Sensor Streaming Data 4' + self.Sensor_Streaming_Write_Data4)
        self.ui.textBrowser_model_data.append('Sensor Streaming Data 5' + self.Sensor_Streaming_Write_Data5)

        self.Slave_str = self.Slave_sensor + self.Slave_eeprom + self.Slave_AFDriverIC + self.Slave_OISDriverIC
        self.Sensor_Streaming_Resister = self.Sensor_Streaming_Resister_Address1 + self.Sensor_Streaming_Resister_Address2 + self.Sensor_Streaming_Resister_Address3 + self.Sensor_Streaming_Resister_Address4 + self.Sensor_Streaming_Resister_Address5
        self.Sensor_Streaming_Data = self.Sensor_Streaming_Write_Data1 + self.Sensor_Streaming_Write_Data2 + self.Sensor_Streaming_Write_Data3 + self.Sensor_Streaming_Write_Data4 + self.Sensor_Streaming_Write_Data5


    def Get_Sensor_ID(self):
        sender = TCPReceiver(self.writeCardIp, 6561)
        sender.send_data(self.writeCardIpPort, self.Slave_str)
        time.sleep(0.1)
        sender.send_data(self.writeCardIpPort, self.Sensor_Streaming_Resister)
        time.sleep(0.1)
        sender.send_data(self.writeCardIpPort, self.Sensor_Streaming_Data)
        pass

    def Write_EEPROM(self):
        pass

    def Check_EEPROM(self):
        pass

    def update_widgets(self):
        self.MainWindow.setWindowTitle('PyQt5 GUI')
