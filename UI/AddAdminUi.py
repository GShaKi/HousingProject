from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddAdmin(object):
    def setupUi(self, AddAdmin):
        AddAdmin.setObjectName("AddAdmin")
        AddAdmin.resize(390, 460)
        AddAdmin.setMinimumSize(QtCore.QSize(390, 460))
        AddAdmin.setMaximumSize(QtCore.QSize(390, 460))
        self.verticalLayoutWidget = QtWidgets.QWidget(AddAdmin)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 60, 281, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.adminUsernameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.adminUsernameLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.adminUsernameLabel.setObjectName("adminUsernameLabel")
        self.verticalLayout.addWidget(self.adminUsernameLabel)
        self.adminUsernameTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.adminUsernameTextEdit.setMaximumSize(QtCore.QSize(16777212, 30))
        self.adminUsernameTextEdit.setObjectName("adminUsernameTextEdit")
        self.verticalLayout.addWidget(self.adminUsernameTextEdit)
        self.adminPasswordLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.adminPasswordLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.adminPasswordLabel.setObjectName("adminPasswordLabel")
        self.verticalLayout.addWidget(self.adminPasswordLabel)
        self.adminPasswordTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.adminPasswordTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.adminPasswordTextEdit.setObjectName("adminPasswordTextEdit")
        self.verticalLayout.addWidget(self.adminPasswordTextEdit)
        self.adminNameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.adminNameLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.adminNameLabel.setObjectName("adminNameLabel")
        self.verticalLayout.addWidget(self.adminNameLabel)
        self.adminNameTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.adminNameTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.adminNameTextEdit.setObjectName("adminNameTextEdit")
        self.verticalLayout.addWidget(self.adminNameTextEdit)
        self.addAdminButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addAdminButton.setObjectName("addAdminButton")
        self.verticalLayout.addWidget(self.addAdminButton)
        self.crLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.crLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.crLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.crLabel.setObjectName("crLabel")
        self.verticalLayout.addWidget(self.crLabel)

        self.retranslateUi(AddAdmin)
        QtCore.QMetaObject.connectSlotsByName(AddAdmin)

    def retranslateUi(self, AddAdmin):
        _translate = QtCore.QCoreApplication.translate
        AddAdmin.setWindowTitle(_translate("AddAdmin", "Saha Housings - Add an Admin"))
        self.adminUsernameLabel.setText(_translate("AddAdmin", "Username"))
        self.adminPasswordLabel.setText(_translate("AddAdmin", "Password"))
        self.adminNameLabel.setText(_translate("AddAdmin", "Name"))
        self.addAdminButton.setText(_translate("AddAdmin", "Add Admin"))
        self.crLabel.setText(_translate("AddAdmin", "Saha Housings"))