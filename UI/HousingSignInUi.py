from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SignInHousing(object):
    def setupUi(self, SignInHousing):
        SignInHousing.setObjectName("SignInHousing")
        SignInHousing.resize(390, 460)
        SignInHousing.setMinimumSize(QtCore.QSize(390, 460))
        SignInHousing.setMaximumSize(QtCore.QSize(390, 460))
        self.verticalLayoutWidget = QtWidgets.QWidget(SignInHousing)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 60, 281, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.housingNameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.housingNameLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.housingNameLabel.setObjectName("housingNameLabel")
        self.verticalLayout.addWidget(self.housingNameLabel)
        self.housingNameTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.housingNameTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.housingNameTextEdit.setObjectName("housingNameTextEdit")
        self.verticalLayout.addWidget(self.housingNameTextEdit)
        self.usernameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.usernameLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.usernameLabel.setObjectName("usernameLabel")
        self.verticalLayout.addWidget(self.usernameLabel)
        self.usernameTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.usernameTextEdit.setMaximumSize(QtCore.QSize(16777212, 30))
        self.usernameTextEdit.setObjectName("usernameTextEdit")
        self.verticalLayout.addWidget(self.usernameTextEdit)
        self.passwordLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.passwordLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.passwordLabel.setObjectName("passwordLabel")
        self.verticalLayout.addWidget(self.passwordLabel)
        self.passwordTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.passwordTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.passwordTextEdit.setObjectName("passwordTextEdit")
        self.verticalLayout.addWidget(self.passwordTextEdit)
        self.signinHousingButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.signinHousingButton.setObjectName("signinHousingButton")
        self.verticalLayout.addWidget(self.signinHousingButton)
        self.crLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.crLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.crLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.crLabel.setObjectName("crLabel")
        self.verticalLayout.addWidget(self.crLabel)

        self.retranslateUi(SignInHousing)
        QtCore.QMetaObject.connectSlotsByName(SignInHousing)

    def retranslateUi(self, SignInHousing):
        _translate = QtCore.QCoreApplication.translate
        SignInHousing.setWindowTitle(_translate("SignInHousing", "Saha Housings - Sign In to a Housing"))
        self.housingNameLabel.setText(_translate("SignInHousing", "Housing name"))
        self.usernameLabel.setText(_translate("SignInHousing", "Username"))
        self.passwordLabel.setText(_translate("SignInHousing", "Password"))
        self.signinHousingButton.setText(_translate("SignInHousing", "Sign In"))
        self.crLabel.setText(_translate("SignInHousing", "Saha Housings"))