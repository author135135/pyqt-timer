#!/usr/bin/python
# encoding: utf-8

import sys
import datetime
from subprocess import Popen
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SleepTimerWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(SleepTimerWidget, self).__init__(parent)
        self.w_width = kwargs.get('w_width', 700)
        self.w_height = kwargs.get('w_height', 500)

        w_center = self.get_window_center()

        # Main widget config
        self.setGeometry(w_center['pos_x'], w_center['pos_y'], self.w_width, self.w_height)
        self.setMaximumSize(self.w_width, self.w_height)
        self.setMinimumSize(self.w_width, self.w_height)
        self.setWindowTitle('Sleep Timer')

        # Timer init
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_close_action)
        self.timer.setSingleShot(True)

        # Timer widgets
        timer_label = QLabel('Work time:')
        timer_label.setStyleSheet("font-size: 18px; color: #333333;")

        # Hour field init
        hour_validator = QIntValidator(0, 23)

        self.hour_field = QLineEdit("0")
        self.hour_field.setValidator(hour_validator)
        self.hour_field.setFixedWidth(45)

        hour_up = QPushButton()
        hour_up.setObjectName('Up')
        hour_up.setProperty('type', 'hour')
        hour_up.setStyleSheet("background: red; outline: none;")
        hour_up.setFixedSize(20, 10)
        hour_up.clicked.connect(self.buttons_click)
        hour_up.setAutoRepeat(True)

        hour_down = QPushButton()
        hour_down.setObjectName('Down')
        hour_down.setProperty('type', 'hour')
        hour_down.setStyleSheet("background: yellow; outline: none;")
        hour_down.setFixedSize(20, 10)
        hour_down.clicked.connect(self.buttons_click)
        hour_down.setAutoRepeat(True)

        hour_buttons_layout = QVBoxLayout()
        hour_buttons_layout.setSpacing(0)
        hour_buttons_layout.addWidget(hour_up)
        hour_buttons_layout.addWidget(hour_down)

        hour_label = QLabel('hour')
        hour_label.setStyleSheet("font-size: 12px; margin: 0px 0px 0px 3px;")

        hour_layout = QHBoxLayout()
        hour_layout.setSpacing(0)
        hour_layout.addWidget(self.hour_field)
        hour_layout.addLayout(hour_buttons_layout)
        hour_layout.addWidget(hour_label)

        # Minute field init
        minute_validator = QIntValidator(0, 59)

        self.minute_field = QLineEdit("0")
        self.minute_field.setValidator(minute_validator)
        self.minute_field.setFixedWidth(45)

        minute_up = QPushButton()
        minute_up.setObjectName('Up')
        minute_up.setProperty('type', 'minute')
        minute_up.setStyleSheet("background: red; outline: none;")
        minute_up.setFixedSize(20, 10)
        minute_up.clicked.connect(self.buttons_click)
        minute_up.setAutoRepeat(True)

        minute_down = QPushButton()
        minute_down.setObjectName('Down')
        minute_down.setProperty('type', 'minute')
        minute_down.setStyleSheet("background: yellow; outline: none;")
        minute_down.setFixedSize(20, 10)
        minute_down.clicked.connect(self.buttons_click)
        minute_down.setAutoRepeat(True)

        minute_buttons_layout = QVBoxLayout()
        minute_buttons_layout.setSpacing(0)
        minute_buttons_layout.addWidget(minute_up)
        minute_buttons_layout.addWidget(minute_down)

        minute_label = QLabel('min')
        minute_label.setStyleSheet("font-size: 12px; margin: 0px 0px 0px 3px;")

        minute_layout = QHBoxLayout()
        minute_layout.setSpacing(0)
        minute_layout.addWidget(self.minute_field)
        minute_layout.addLayout(minute_buttons_layout)
        minute_layout.addWidget(minute_label)

        # Actions dropdown list init
        actions_label = QLabel('Timeout operation:')
        actions_label.setStyleSheet("font-size: 18px; color: #333333;")

        self.actions_list = QComboBox()
        self.actions_list.addItem("Reboot")
        self.actions_list.addItem("Shutdown")

        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 30, 0, 30)
        actions_layout.addWidget(actions_label)
        actions_layout.addWidget(self.actions_list)

        # Control buttons init
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_button_action)

        self.stop_button = QPushButton('Cancel')
        self.stop_button.clicked.connect(self.stop_button_action)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)

        # Main grid config
        grid = QGridLayout(self)
        grid.setAlignment(Qt.AlignVCenter)
        grid.addWidget(timer_label, 0, 0)
        grid.addLayout(hour_layout, 0, 1)
        grid.addLayout(minute_layout, 0, 2)
        grid.addLayout(actions_layout, 1, 0, 1, 3)
        grid.addLayout(buttons_layout, 2, 0, 1, 3)

    def buttons_click(self):
        sender = self.sender()
        field = getattr(self, '%s_field' % sender.property('type').toString())

        try:
            value = int(field.text())
        except ValueError:
            value = 0

        if sender.objectName() == 'Up':
            if field.validator().top() > value:
                field.setText(str(value + 1))
        else:
            if field.validator().bottom() < value:
                field.setText(str(value - 1))

    def start_button_action(self):
        try:
            hours = int(self.hour_field.text())
        except ValueError:
            hours = 0

        try:
            minutes = int(self.minute_field.text())
        except ValueError:
            minutes = 0

        if not hours and not minutes:
            self.hour_field.setStyleSheet("color: red")
            self.minute_field.setStyleSheet("color: red")
        else:
            print "Sleep timer start..."
            self.hour_field.setStyleSheet("color: #000")
            self.minute_field.setStyleSheet("color: #000")
            self.start_button.setDisabled(True)

            ml_seconds = datetime.timedelta(hours=hours, minutes=minutes).seconds * 1000

            self.timer.start(ml_seconds)

    def stop_button_action(self):
        print "Sleep timer abort..."

        self.timer.stop()
        self.start_button.setDisabled(False)

    def timer_close_action(self):
        print "Timer out. System shut down..."

        action_type = str(self.actions_list.currentText()).lower()

        if 'win' in sys.platform:
            platform = 'win'
        elif 'linux' in sys.platform:
            platform = 'linux'

        proc = Popen([self._platform_commands(platform, action_type)], shell=True)

    def _platform_commands(self, platform, command):
        commands = {
            'win': {
                'reboot': '',
                'shutdown': '',
            },
            'linux': {
                'reboot': '/sbin/reboot',
                'shutdown': '/sbin/shutdown',
            },
        }

        return commands[platform][command]

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def get_window_center(self):
        resolution = QDesktopWidget().screenGeometry()

        return {
            'pos_x': (resolution.width() - self.w_width) / 2,
            'pos_y': (resolution.height() - self.w_height) / 2,
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)

    m = SleepTimerWidget(w_width=400, w_height=200)
    m.show()

    sys.exit(app.exec_())
