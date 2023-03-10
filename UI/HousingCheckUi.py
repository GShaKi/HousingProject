from PyQt5 import QtCore, QtWidgets
from UI.HousingCreateUi import Ui_CreateHousing
from UI.HousingSignInUi import Ui_SignInHousing

class Ui_HousingCheck(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(380, 220)
        Form.setMinimumSize(QtCore.QSize(380, 220))
        Form.setMaximumSize(QtCore.QSize(380, 220))
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 50, 280, 110))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.createHousingButton = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked = lambda: self.create_housing())
        self.createHousingButton.setObjectName("createHousingButton")
        self.verticalLayout.addWidget(self.createHousingButton)
        self.signinHousingButton = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked = lambda: self.signin_housing())
        self.signinHousingButton.setObjectName("signinHousingButton")
        self.verticalLayout.addWidget(self.signinHousingButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Saha Housings - Housing Check"))
        self.createHousingButton.setText(_translate("Form", "Create Housing"))
        self.signinHousingButton.setText(_translate("Form", "Sign in to a housing"))

    def create_housing(self):
        self.createHousingWindow = QtWidgets.QWidget()
        self.createHousingUi = Ui_CreateHousing()
        self.createHousingUi.setupUi(self.createHousingWindow)
        self.createHousingWindow.show()
    
    def signin_housing(self):
        self.signinHousingWindow = QtWidgets.QWidget()
        self.signinHousingUi = Ui_SignInHousing()
        self.signinHousingUi.setupUi(self.signinHousingWindow)
        self.signinHousingWindow.show()