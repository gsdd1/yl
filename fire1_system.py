import sys
from pathlib import Path
import cv2
import torch
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from LoginUi import Ui_LoginWindow
from interface import Ui_MainWindow


# from PyQt5.uic import loadUi
# from pyqt5_plugins.examplebuttonplugin import QtGui


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QtCore.Qt.black)
        self.ui.frame.setGraphicsEffect(self.shadow)
        self.ui.pushButton_Login.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_Register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_L_sure.clicked.connect(self.login_in)  # 连接登录按钮的点击信号到 login_in 方法
        self.show()

    def login_in(self):
        account = self.ui.lineEdit_L_account.text()
        password = self.ui.lineEdit_L_password.text()
        if account == "www" and password == "123":
            self.win = MainWindow()
            self.close()
        else:
            QMessageBox.warning(self, "登录错误", "账号或密码错误！")



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # 初始化UI
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QtCore.Qt.black)
        self.ui.frame.setGraphicsEffect(self.shadow)
        self.bind_slots()  # 在这里绑定信号和槽
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPosition().toPoint()
            self.isPressed = True

    def mouseMoveEvent(self, event):
        if self.isPressed:
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isPressed = False

        # ================================ 按钮功能函数 ================================ #
            # 注册


    # 按钮功能
    def open_image(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, '选择图片', r'D:\Bishe\yolov5-master\data\images', 'Image Files (*.png *.jpg *.jpeg)')
            if file_path:
                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaled(self.ui.label_in.size(), Qt.KeepAspectRatio)
                self.ui.label_in.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开图片时发生错误: {e}")

    def open_video(self):
         try:
             file_path, _ = (QFileDialog.getOpenFileName(self, '选择视频', r'D:\Bishe\yolov5-master\data\\videos',
                                                        'Video Files (*.mp4 *.avi)'))
             if file_path:
                self.cap = cv2.VideoCapture(file_path)
                if self.cap.isOpened():
                  self.timer = QTimer()
                  self.timer.timeout.connect(self.update_label)
                  self.timer.start(20)  # 20毫秒更新一次
             else:
                print("没有选择视频文件")
                QMessageBox.critical(self, "错误", "没有选择视频文件")
         except Exception as e:
             QMessageBox.critical(self, "错误", f"播放视频时发生错误: {e}")
             print('111')

    def update_label(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                qt_image = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                # 缩放QPixmap以适应QLabel的大小，并保持宽高比
                scaled_pixmap = pixmap.scaled(self.ui.label_in.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # 设置QLabel的居中对齐
                self.ui.label_in.setAlignment(Qt.AlignCenter)
                self.ui.label_in.setPixmap(scaled_pixmap)
            else:
                # 视频播放完毕，停止定时器
                self.timer.stop()
                # 重置视频捕获对象
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 将视频帧位置重置为0
                # 如果需要循环播放，可以再次启动定时器
                # self.timer.start(20)
        else:
            print("视频捕获对象未打开")

    def open_canmer(self):
        try:
            file_path = QFileDialog.getOpenFileName(self, '选择摄像头', '/Data')
            if file_path:
                print(f'选择的图片路径: {file_path[0]}')
                # 在这里处理文件路径，例如显示图片
        except Exception as e:
            print(f'发生异常: {e}')

    def open_model(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, '选择模型', r'D:\Bishe\yolov5-master\runs\train')
            if file_path:
                # 确保 file_path 是一个有效的模型文件路径
                if file_path.endswith('.pt'):
                    # 尝试加载模型
                    # 根据您的环境选择 'cpu' 或 'cuda'
                    device = 'cuda' if torch.cuda.is_available() else 'cpu'
                    self.model = torch.load(file_path, map_location=device)
                    self.ui.pushButton_5_M(file_path)
                else:
                    QMessageBox.critical(self, "错误", "选择的文件不是有效的模型文件")
                self.ui.pushButton_5_M.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
            else:
                QMessageBox.critical(self, "错误", "没有选择模型文件")
        except Exception as e:
            # 打印异常信息以帮助调试
            print(f"加载模型时发生错误: {e}")
            QMessageBox.critical(self, "错误", f"加载模型时发生错误: {e}")

    def open_start(self):
        # 加载模型
        model_path = Path('\runs\train\exp10\weights\best.pt')
        self.model = self.load_model(model_path)
        # 这里可以添加一些代码来使用模型，例如预测

    def bind_slots(self):  # 设置了信号和槽的连接
        # 确保在 setupUi 之后访问 UI 元素
        self.ui.pushButton_P.clicked.connect(self.open_image)
        self.ui.pushButton_2_V.clicked.connect(self.open_video)
        self.ui.pushButton_3_CM.clicked.connect(self.open_canmer)
        self.ui.pushButton_5_M.clicked.connect(self.open_model)
        self.ui.pushButton_4_S.clicked.connect(self.open_start)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
