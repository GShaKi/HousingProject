from PyQt5 import QtCore, QtWidgets

class Ui_SearchHouse(object):
    def setupUi(self, SearchHouse):
        SearchHouse.setObjectName("SearchHouse")
        SearchHouse.resize(390, 400)
        SearchHouse.setMaximumSize(QtCore.QSize(390, 400))
        self.verticalLayoutWidget = QtWidgets.QWidget(SearchHouse)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 40, 261, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.formLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.sizeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.sizeLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.sizeLabel.setObjectName("sizeLabel")
        self.formLayout.addWidget(self.sizeLabel)
        self.sizeTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.sizeTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.sizeTextEdit.setObjectName("sizeTextEdit")
        self.formLayout.addWidget(self.sizeTextEdit)
        self.priceLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.priceLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.priceLabel.setObjectName("priceLabel")
        self.formLayout.addWidget(self.priceLabel)
        self.priceTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.priceTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.priceTextEdit.setObjectName("priceTextEdit")
        self.formLayout.addWidget(self.priceTextEdit)
        self.rentPriceLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.rentPriceLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.rentPriceLabel.setObjectName("rentPriceLabel")
        self.formLayout.addWidget(self.rentPriceLabel)
        self.rentPriceTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.rentPriceTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.rentPriceTextEdit.setObjectName("rentPriceTextEdit")
        self.formLayout.addWidget(self.rentPriceTextEdit)
        self.bedroomCountLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.bedroomCountLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.bedroomCountLabel.setObjectName("bedroomCountLabel")
        self.formLayout.addWidget(self.bedroomCountLabel)
        self.bedroomCountTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.bedroomCountTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.bedroomCountTextEdit.setObjectName("bedroomCountTextEdit")
        self.formLayout.addWidget(self.bedroomCountTextEdit)
        self.furnishedLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.furnishedLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.furnishedLabel.setObjectName("furnishedLabel")
        self.formLayout.addWidget(self.furnishedLabel)
        self.furnishedTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.furnishedTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.furnishedTextEdit.setObjectName("furnishedTextEdit")
        self.formLayout.addWidget(self.furnishedTextEdit)
        self.searchHouseButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.searchHouseButton.setObjectName("searchHouseButton")
        self.formLayout.addWidget(self.searchHouseButton)

        self.retranslateUi(SearchHouse)
        QtCore.QMetaObject.connectSlotsByName(SearchHouse)

    def retranslateUi(self, SearchHouse):
        _translate = QtCore.QCoreApplication.translate
        SearchHouse.setWindowTitle(_translate("SearchHouse", "Saha Housings - Search for a House"))
        self.sizeLabel.setText(_translate("SearchHouse", "Size"))
        self.priceLabel.setText(_translate("SearchHouse", "price"))
        self.rentPriceLabel.setText(_translate("SearchHouse", "Rent price"))
        self.rentPriceTextEdit.setPlaceholderText(_translate("SearchHouse", "(Type 0 if your not looking for renting)"))
        self.bedroomCountLabel.setText(_translate("SearchHouse", "Bedroom Count"))
        self.furnishedLabel.setText(_translate("SearchHouse", "Furnished"))
        self.furnishedTextEdit.setPlaceholderText(_translate("SearchHouse", "(True or False)"))
        self.searchHouseButton.setText(_translate("SearchHouse", "Add House"))