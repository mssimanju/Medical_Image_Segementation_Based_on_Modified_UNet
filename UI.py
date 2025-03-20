import os
import shutil

from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import cv2
import torch
import os.path as osp
from UNet import UNet
import numpy as np
from test import test


class Stats(QTabWidget):
    filename = ''
    weight_dr = ''

    def __init__(self):
        super().__init__()
        select_img = QPixmap("ui_img/liver_in.png")
        size = QSize(512, 512)
        select_img = select_img.scaled(size)
        self.ui = uic.loadUi("Main.ui")
        self.ui.img_select.clicked.connect(self.select_img)
        self.ui.img_submit.clicked.connect(self.submit_img)
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.ui.label_3.setPixmap(select_img)
        self.ui.label_3.setScaledContents(True)

    def select_img(self):

        Stats.filename, filetype = QFileDialog.getOpenFileName(self, 'Choose file', '.', '*.jpg *.png *.tif *.jpeg')

        select_img = QPixmap(Stats.filename)
        size = QSize(512, 512)
        select_img = select_img.scaled(size)
        self.ui.label_2.setPixmap(select_img)
        self.ui.label_2.setScaledContents(True)

        QMessageBox.about(self.ui,
                          'Succeed ',
                          'Image Selected' + Stats.filename
                          )

    def submit_img(self):
        QMessageBox.about(self.ui,
                          'Succeed ',
                          'Image Submitted!' + Stats.filename
                          )

        test("Stats.filename", "./checkpoint_DRIVE.pth", "./test/outputs/19_test.tif")

        QMessageBox.about(self.ui,
                          'Succeed ',
                          'Succeed! '
                          )

    def selectionchange(self):
        selection = self.ui.comboBox.currentText()
        if selection == '眼球血管分割':
            self.ui.label_3.setPixmap(QPixmap("ui_img/eye_in.tif"))
            self.ui.label_3.setScaledContents(True)
            Stats.weight_dr = 'checkpoint_DRIVE.pth'
        if selection == '肾脏CT图分割':
            self.ui.label_3.setPixmap(QPixmap("ui_img/liver_in.png"))
            self.ui.label_3.setScaledContents(True)

        QMessageBox.about(self.ui,
                          'Succeed ',
                          'Selection changed to ' + selection
                          )


if __name__ == "__main__":
    app = QApplication([])



    app.setWindowIcon(QIcon('120739.png'))
    stats = Stats()
    stats.ui.show()
    app.exec_()
