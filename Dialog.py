from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class InputDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("dialog.ui", self)

        self.buttonBox.accepted.connect(self.onOkClicked)
        self.buttonBox.rejected.connect(self.rejected)

        self.sbRadius.valueChanged.connect(self.radiusChanged)
        self.show()

    def onOkClicked(self):
        self.radius = self.sbRadius.value()
        self.sigma = self.dsbSigma.value()
        self.close()

    def radiusChanged(self):
        self.dsbSigma.setMinimum(self.sbRadius.value())
