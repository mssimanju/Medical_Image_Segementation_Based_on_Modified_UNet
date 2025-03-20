import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_mask = None
        self.mask_img = None
        self.new_img = None
        self.setWindowTitle("Modify")
        self.setGeometry(100, 100, 512, 512)
        self.realimage = QImage(self.size(), QImage.Format_RGB32)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        self.initUI()

    def initUI(self):
        saveAction = QAction("保存", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.save)

        loadAction = QAction("打开", self)
        loadAction.setShortcut("Ctrl+O")
        loadAction.triggered.connect(self.load)

        clearAction = QAction("清空", self)
        clearAction.setShortcut("Ctrl+C")
        clearAction.triggered.connect(self.clear)

        blackAction = QAction("黑色", self)
        blackAction.setShortcut("Ctrl+B")
        blackAction.triggered.connect(lambda: self.setColor(Qt.black))

        whiteAction = QAction("白色", self)
        whiteAction.setShortcut("Ctrl+W")
        whiteAction.triggered.connect(lambda: self.setColor(Qt.white))

        thickerAction = QAction("加粗", self)
        thickerAction.setShortcut("Ctrl++")
        thickerAction.triggered.connect(self.thicker)

        thinnerAction = QAction("减细", self)
        thinnerAction.setShortcut("Ctrl+-")
        thinnerAction.triggered.connect(self.thinner)

        loadrealAction = QAction("选择实物", self)
        loadrealAction.setShortcut("Ctrl+r")
        loadrealAction.triggered.connect(self.loadreal)

        applyrealAction = QAction("分割实物", self)
        applyrealAction.setShortcut("Ctrl+x")
        applyrealAction.triggered.connect(self.open_images)

        returnAction = QAction("返回掩膜", self)
        returnAction.setShortcut("Ctrl+z")
        returnAction.triggered.connect(self.return_to_mask)

        saverealAction = QAction("保存实物分割", self)
        saverealAction.setShortcut("Ctrl+r")
        saverealAction.triggered.connect(self.savereal)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("文件")
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        fileMenu.addAction(saverealAction)

        editMenu = menubar.addMenu("编辑")
        editMenu.addAction(clearAction)
        editMenu.addAction(blackAction)
        editMenu.addAction(whiteAction)

        brushMenu = menubar.addMenu("笔刷")
        brushMenu.addAction(thickerAction)
        brushMenu.addAction(thinnerAction)

        fileMenu = menubar.addMenu("分割")
        fileMenu.addAction(loadrealAction)
        fileMenu.addAction(applyrealAction)
        fileMenu.addAction(returnAction)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "保存画板", "", "PNG(*.png);;JPEG(*.jpg *.jpeg)")
        if filePath == "":
            return
        self.image.save(filePath)

    def savereal(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "保存实物分割", "", "PNG(*.png);;JPEG(*.jpg *.jpeg)")
        if filePath == "":
            return
        self.new_img.save(filePath)

    def load(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "打开画板", "", "PNG(*.png);JPEG(*.jpg *.jpeg);All Files(*.*)")
        if filePath == "":
            return
        loadedImage = QImage(filePath)
        if loadedImage.isNull():
            return
        self.image = loadedImage
        self.update()

    def loadreal(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "打开画板", "", "PNG(*.png);JPEG(*.jpg *.jpeg);All Files(*.*)")
        if filePath == "":
            return
        loadedImage = QImage(filePath)
        if loadedImage.isNull():
            return
        self.realimage = loadedImage

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def setColor(self, color):
        self.brushColor = color

    def thicker(self):
        self.brushSize += 1

    def thinner(self):
        if self.brushSize > 1:
            self.brushSize -= 1

    def open_images(self):
        self.original_mask = self.image
        self.mask_img = self.image.scaled(self.realimage.width(), self.realimage.height())
        self.new_img = QImage(self.realimage.size(), QImage.Format_RGB32)
        self.new_img.fill(Qt.white)
        for x in range(self.realimage.width()):
            for y in range(self.realimage.height()):
                if self.mask_img.pixelColor(x, y).red() > 0:
                    self.new_img.setPixelColor(x, y, self.realimage.pixelColor(x, y))
        self.image = self.new_img
        self.update()

    def return_to_mask(self):
        self.image = self.original_mask
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
