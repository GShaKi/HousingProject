from PyQt5 import QtCore, QtWidgets, Qt
import sqlite3
import uuid
import hashlib
import sys

conn = sqlite3.connect('HousingDB.db')

"""
1. Request Best Home
"""

class Housing:
    def __init__(self, id, name, username, password, adminname, add_database):
        if add_database == True:
            if id == None:
                self.id = str(uuid.uuid1())
            else:
                self.id = id
            self.name = name
            self.admins = [Admin(None, self.id, username, password, adminname, True)]
            self.users = []
            self.houses = []
            self.house_requests = []
            conn.execute("INSERT INTO Housing VALUES (?, ?, ?, ?, ?)", (self.id, self.name, username, password, adminname, ))
            conn.commit()
        else:
            self.id = id
            self.name = name
            self.admins = []
            self.users = []
            self.houses = []
            self.house_requests = []
            self.requests = []
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE HousingID = (?)" , (self.id ,))
            dusers = cursor.fetchall()
            for u in dusers:
                if u[5] == 1:
                    self.admins.append(Admin(u[0], u[1], u[2], u[3], u[4], False))
                else:
                    self.users.append(User(u[0], u[1], u[2], u[3], u[4], False))
            cursor.execute("SELECT * FROM House WHERE HousingID = (?)" , (self.id ,))
            dhouses = cursor.fetchall()
            for h in dhouses:
                self.houses.append(House(h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11], h[12], False))
            cursor.execute("SELECT * FROM HouseRequest")
            dhouse_requests = cursor.fetchall()
            for r in dhouse_requests:
                self.house_requests.append(r[0])

    def update_values(self):
        self.admins = []
        self.users = []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE ID = (?)", (self.id, ))
        users = cursor.fetchall()
        for u in users:
            if u[6] == 0:
                self.admins.append(Admin(u[0], u[1], u[2], u[3], u[4], False))
            else:
                self.users.append(User(u[0], u[1], u[2], u[3], u[4], False))

    def create_acc(self, username, password, name):
        self.users.append(User(None, self.id, username, password, name, True))
        print(f"Account with the name {name} successfully added.")

    def get_session(self, username, password):
        all_members = self.admins + self.users
        for u in all_members:
            if u.username == username and u.password == str(hashlib.md5(str(password + self.id).encode('utf-8')).hexdigest()):
                return Session(self, u)

class User:
    def __init__(self, id, housingid, username, password, name, add_database):
        if id == None:
            self.id = str(uuid.uuid1())
        else:
            self.id = id
        self.housingid = housingid
        self.username = username
        if add_database == True:
            self.password = str(hashlib.md5(str(password + housingid).encode('utf-8')).hexdigest())
        else:
            self.password = password
        self.name = name
        self.isAdmin = False
        if add_database == True:
            conn.execute("INSERT INTO User VALUES (?, ?, ?, ?, ?, ?)", (self.id, self.housingid, self.username, self.password, self.name, self.isAdmin, ))
            conn.commit()

    def add_house(self, housingid, city, address, size, available, price, bedroomcount, furnish, other, approval, rent_price):
        new_house = House(None , housingid, self.id, city, address, size , available, price, bedroomcount, furnish, other, approval , True , rent_price)
        return new_house

    def remove_user(self, user):
        print("Access Denied!")

    def add_admin(self, id, housingid, username, password, name):
        print("Access Denied!")


class Admin(User):
    def __init__(self, id, housingid, username, password, name, add_database):
        super().__init__(id, housingid, username, password, name, add_database)
        self.isAdmin = True
        if add_database == True:
            conn.execute("UPDATE User SET isAdmin = (?) WHERE ID = (?)", (self.isAdmin, self.id, ))
            conn.commit()
    
    def remove_user(self, user):
        conn.execute("DELETE FROM User WHERE ID = (?)", (user.id, ))
        print(f"User {user.name} removed.")
        del user
        conn.commit()
    
    def add_admin(self, housingid, username, password, name):
        admin = Admin(None, housingid, username, password, name, True)
        return admin

class House:
    def __init__(self, id, housingid, sellerid, city, address, size, available, price, bedroomcount, furnish, other, approval, add_database, rent_price): # if for sell => rent_price = 0
        # apprval -> 1 = Accepted, 2 = Sold or No Action, 3 = Under Review
        # available -> rent_id (database int -> string)
        # apprval -> status
        if id == None:
            self.id = str(uuid.uuid1())
        else:
            self.id = id
        self.housingid = housingid
        self.sellerid = sellerid
        self.city = city
        self.address = address
        self.size = size
        self.available = available
        self.price = price
        self.bedroomcount = bedroomcount
        self.furnish = furnish
        self.other = other
        self.approval = approval
        self.rent_price = rent_price
        if add_database == True:
            conn.execute("INSERT INTO House VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.id, self.housingid, self.sellerid, self.city, self.address, self.size, self.rent_price, self.available, self.price, self.bedroomcount, self.furnish, self.other, self.approval, ))
            conn.commit()

class Session:
    def __init__(self, housing: Housing, user: User):
        self.housing = housing
        self.user = user

    def add_admin(self, username, password, name):
        new_admin = self.user.add_admin(self.housing.id, username, password, name)
        self.housing.admins.append(new_admin)

    def get_status(self):
        if self.user.isAdmin == 1:
            print(self.housing.name + " " + self.housing.id + "\n" + "Houses :" , self.housing.houses , "\n" + "Requests :" , self.housing.house_requests)
        else:
            print("You're not admin.")

    def add_house(self, city, address, size, available, price, bedroomcount, furnish, other, rent_price):
        new_house = self.user.add_house(self.housing.id, city, address, size, available, price, bedroomcount, furnish, other, 2 , rent_price)
        if new_house not in self.housing.houses:
            new_house.approval = 3
            if new_house not in self.housing.houses:
                self.housing.houses.append(new_house)
                self.housing.house_requests.append(new_house)
                conn.execute("INSERT INTO HouseRequest VALUES (?)", (new_house.id, ))
                conn.commit()
                print("Your request has sent to your housing.")
            else:
                print("You have sent request or it's on sell.")
        else:
            (self.housing.houses.index(new_house)).approval = 1
            conn.execute("UPDATE House SET Approval = (?) WHERE HouseID = (?)", (1, h.id, ))
            conn.commit()
            print("Your house is on sell.")

    def remove_user(self, name, all_members):
        all_members = self.housing.users + self.housing.admins
        for u in all_members:
            if u.name == name:
                self.user.remove_user(u)
                self.housing.update_values()

    def check_approval(self, houseid):
        if self.user.isAdmin == True:
            for h in self.housing.houses:
                if h.id == houseid:
                    index = self.housing.houses.index(h)
                    self.housing.houses[index].approval = 1
                    conn.execute("UPDATE House SET Approval = (?) WHERE HouseID = (?)", (1, h.id, ))
                    conn.commit()
                    index2 = self.housing.house_requests.index(h.id)
                    conn.execute("DELETE FROM HouseRequest WHERE HouseID=(?)", (h.id, ))
                    conn.commit()
                    self.housing.house_requests.remove(h.id)
                    print("The house approved.")
                    break
            else:
                print("There is no house with this id.")
        else:
            print("Access Denied!")

    def find_home_list(self, size, price, bedroomcount, furnish, rent_price): #size : min , price : max , furnish : 0 | 1 , bedroomcount : min , rent_price : max
        home_list = []
        for home in self.housing.houses:
            if home.size >= size and home.price <= price and furnish == home.furnish and bedroomcount <= home.bedroomcount and rent_price >= home.rent_price and home.approval == 1:
                home_list.append(home)
        return home_list

    def check_approval_rent(self , house : House):
        house.available = 1

    def find_home(self, size, price, bedroomcount, furnish, rent_price , best_home : int): #best_home : 1 => lower price , 2 => bigger size
        def Size(a : House):
            return a.size
        def Price(a : House):
            return a.price
        home_list = self.find_home_list(size, price, bedroomcount, furnish, rent_price)
        if len(home_list) == 0:
            return "There isn't any house with these choices."
        elif best_home == 1:
            home_list.sort(key=Price , reverse = False)
            if rent_price == 0:
                index = self.housing.houses.index(home_list[0])
                self.housing.houses[index].sellerid = self.user.id
                self.housing.houses[index].approval = 2
                conn.execute("UPDATE House SET SellerID = (?) WHERE HouseID = (?)", (self.user.id, self.housing.houses[index].id, ))
                conn.commit()
            else:
                index = self.housing.houses.index(home_list[0])
                self.housing.houses[index].approval = 2
                self.housing.houses[index].available = self.user.id
            return home_list[0]
        elif best_home == 2:
            home_list.sort(key=Size , reverse = True)
            if rent_price == 0:
                index = self.housing.houses.index(home_list[0])
                self.housing.houses[index].sellerid = self.user.id
                self.housing.houses[index].approval = 2
                conn.execute("UPDATE House SET SellerID = (?) WHERE HouseID = (?)", (self.user.id, self.housing.houses[index].id, ))
                conn.commit()
            else:
                index = self.housing.houses.index(home_list[0])
                self.housing.houses[index].approval = 2
                self.housing.houses[index].available = self.user.id
            return home_list[0]
    def show_my_houses(self):
        for i in self.housing.houses:
            if i.sellerid == self.user.id or i.available == self.user.id:
                print(i)

class Ui_CreateHousing(object):
    def setupUi(self, CreatHousing):
        CreatHousing.setObjectName("CreatHousing")
        CreatHousing.resize(390, 460)
        CreatHousing.setMinimumSize(QtCore.QSize(390, 460))
        CreatHousing.setMaximumSize(QtCore.QSize(390, 460))
        self.verticalLayoutWidget = QtWidgets.QWidget(CreatHousing)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 60, 281, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.nameLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.nameLabel.setObjectName("nameLabel")
        self.verticalLayout.addWidget(self.nameLabel)
        self.housingNameTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.housingNameTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.housingNameTextEdit.setObjectName("housingNameTextEdit")
        self.verticalLayout.addWidget(self.housingNameTextEdit)
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
        self.createHousingButton = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked = lambda: self.create_housing())
        self.createHousingButton.setObjectName("createHousingButton")
        self.verticalLayout.addWidget(self.createHousingButton)
        self.crLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.crLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.crLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.crLabel.setObjectName("crLabel")
        self.verticalLayout.addWidget(self.crLabel)

        self.retranslateUi(CreatHousing)
        QtCore.QMetaObject.connectSlotsByName(CreatHousing)

    def retranslateUi(self, CreatHousing):
        _translate = QtCore.QCoreApplication.translate
        CreatHousing.setWindowTitle(_translate("CreatHousing", "Saha Housings - Create Housing"))
        self.nameLabel.setText(_translate("CreatHousing", "Name"))
        self.adminUsernameLabel.setText(_translate("CreatHousing", "Admin Username"))
        self.adminPasswordLabel.setText(_translate("CreatHousing", "Admin Password"))
        self.adminNameLabel.setText(_translate("CreatHousing", "name"))
        self.createHousingButton.setText(_translate("CreatHousing", "Create "))
        self.crLabel.setText(_translate("CreatHousing", "Saha Housings"))

    def create_housing(self):
        ui.housing = Housing(None, self.housingNameTextEdit.toPlainText(), self.adminUsernameTextEdit.toPlainText(), self.adminPasswordTextEdit.toPlainText(), self.adminNameTextEdit.toPlainText(), True)
        
        succdialog = QtWidgets.QMessageBox()
        succdialog.setWindowTitle("Success")
        succdialog.setText("Your new housing added to our system. Just get back and sign yourself in.")
        button = succdialog.exec()

        if button == QtWidgets.QMessageBox.Ok:
            succdialog.close()

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
        self.signinHousingButton = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked = lambda: self.signin())
        self.signinHousingButton.setObjectName("signinHousingButton")
        self.verticalLayout.addWidget(self.signinHousingButton)
        self.crLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.crLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.crLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.crLabel.setObjectName("crLabel")
        self.verticalLayout.addWidget(self.crLabel)

        self.retranslateUi(SignInHousing)
        QtCore.QMetaObject.connectSlotsByName(SignInHousing)

    def signin(self):
        self.cursor = conn.cursor()
        self.cursor.execute("SELECT * FROM User")
        users = self.cursor.fetchall()
        for u in users:
            if u[2] == self.usernameTextEdit.toPlainText() and u[3] == str(hashlib.md5(str(self.passwordTextEdit.toPlainText() + u[1]).encode('utf-8')).hexdigest()):
                self.cursor.execute("SELECT * FROM Housing WHERE ID = (?)", (u[1], ))
                housings = self.cursor.fetchall()
                ui.housing = Housing(housings[0][0], housings[0][1], housings[0][2], housings[0][3], housings[0][4], False)
                ui.session = ui.housing.get_session(u[2], self.passwordTextEdit.toPlainText())
                succdialog = QtWidgets.QMessageBox()
                succdialog.setWindowTitle("Success")
                succdialog.setText("Your Signed in. Enjoy!")
                button = succdialog.exec()

                if button == QtWidgets.QMessageBox.Ok:
                    succdialog.close()

                break
        else:
            errdialog = QtWidgets.QMessageBox()
            errdialog.setWindowTitle("Error Occurred!")
            errdialog.setText("Username or password is not valid.")
            button = errdialog.exec()

            if button == QtWidgets.QMessageBox.Ok:
                errdialog.close()

    def retranslateUi(self, SignInHousing):
        _translate = QtCore.QCoreApplication.translate
        SignInHousing.setWindowTitle(_translate("SignInHousing", "Saha Housings - Sign In to a Housing"))
        self.housingNameLabel.setText(_translate("SignInHousing", "Housing name"))
        self.usernameLabel.setText(_translate("SignInHousing", "Username"))
        self.passwordLabel.setText(_translate("SignInHousing", "Password"))
        self.signinHousingButton.setText(_translate("SignInHousing", "Sign In"))
        self.crLabel.setText(_translate("SignInHousing", "Saha Housings"))

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

class Ui_MainWindow(object):
    housing = None
    session = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(590, 276)
        MainWindow.setMaximumSize(QtCore.QSize(590, 280))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(30, 10, 531, 201))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.everythingLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.everythingLayout.setContentsMargins(0, 0, 0, 0)
        self.everythingLayout.setSpacing(7)
        self.everythingLayout.setObjectName("everythingLayout")
        self.labelsLayout = QtWidgets.QHBoxLayout()
        self.labelsLayout.setSpacing(7)
        self.labelsLayout.setObjectName("labelsLayout")
        self.housesLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.housesLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.housesLabel.setObjectName("housesLabel")
        self.labelsLayout.addWidget(self.housesLabel)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.labelsLayout.addWidget(self.line_3)
        self.usersLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.usersLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.usersLabel.setObjectName("usersLabel")
        self.labelsLayout.addWidget(self.usersLabel)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.labelsLayout.addWidget(self.line_4)
        self.HousingsLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.HousingsLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.HousingsLabel.setObjectName("HousingsLabel")
        self.labelsLayout.addWidget(self.HousingsLabel)
        self.everythingLayout.addLayout(self.labelsLayout)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.everythingLayout.addWidget(self.line_5)
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setObjectName("buttonsLayout")
        self.housesLayout = QtWidgets.QVBoxLayout()
        self.housesLayout.setSpacing(15)
        self.housesLayout.setObjectName("housesLayout")
        self.addHouseButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4, clicked = lambda: self.add_house())
        self.addHouseButton.setObjectName("addHouseButton")
        self.housesLayout.addWidget(self.addHouseButton)
        self.searchHouseButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.searchHouseButton.setObjectName("searchHouseButton")
        self.housesLayout.addWidget(self.searchHouseButton)
        self.buyHouseButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.buyHouseButton.setObjectName("buyHouseButton")
        self.housesLayout.addWidget(self.buyHouseButton)
        self.checkApprovalButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.checkApprovalButton.setObjectName("checkApprovalButton")
        self.housesLayout.addWidget(self.checkApprovalButton)
        self.buttonsLayout.addLayout(self.housesLayout)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.buttonsLayout.addWidget(self.line)
        self.usersLayout = QtWidgets.QVBoxLayout()
        self.usersLayout.setSpacing(10)
        self.usersLayout.setObjectName("usersLayout")
        self.addAdminButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.addAdminButton.setObjectName("addAdminButton")
        self.usersLayout.addWidget(self.addAdminButton)
        self.removeUserButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.removeUserButton.setObjectName("removeUserButton")
        self.usersLayout.addWidget(self.removeUserButton)
        self.buttonsLayout.addLayout(self.usersLayout)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.buttonsLayout.addWidget(self.line_2)
        self.housingLayout = QtWidgets.QVBoxLayout()
        self.housingLayout.setObjectName("housingLayout")
        self.showHousingInfoButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.showHousingInfoButton.setObjectName("showHousingInfoButton")
        self.housingLayout.addWidget(self.showHousingInfoButton)
        self.buttonsLayout.addLayout(self.housingLayout)
        self.everythingLayout.addLayout(self.buttonsLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 590, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Saha Housings"))
        self.housesLabel.setText(_translate("MainWindow", "Houses Stuff"))
        self.usersLabel.setText(_translate("MainWindow", "Users Stuff"))
        self.HousingsLabel.setText(_translate("MainWindow", "Housing Stuff"))
        self.addHouseButton.setText(_translate("MainWindow", "Add House"))
        self.searchHouseButton.setText(_translate("MainWindow", "Search for Houses"))
        self.buyHouseButton.setText(_translate("MainWindow", "Buy House"))
        self.checkApprovalButton.setText(_translate("MainWindow", "Check Approval"))
        self.addAdminButton.setText(_translate("MainWindow", "Add Admin"))
        self.removeUserButton.setText(_translate("MainWindow", "Remove User"))
        self.showHousingInfoButton.setText(_translate("MainWindow", "Show Housing Info"))

    def check_housing(self):
        self.checkHousingWindow = QtWidgets.QWidget()
        self.checkHousingUi = Ui_HousingCheck()
        self.checkHousingUi.setupUi(self.checkHousingWindow)
        self.checkHousingWindow.show()

    def add_house(self):
        if self.session == None:
            self.check_housing()
        else:
            pass

# main_cursor = conn.cursor()
# main_cursor.execute("SELECT * FROM Housing")
# dmain_housings = main_cursor.fetchall()
# main_housings = []
# for h in dmain_housings:
#     main_housings.append(Housing(h[0], h[1], h[2], h[3], h[4], False))
# housing = Housing(None, "Hello", "Shayan", "Kermani", "ShK", True)
# s3 = housing.get_session("Shayan", "Kermani")
# housing.create_acc("MyAcc", "123", "ShK2")
# s4 = housing.get_session("MyAcc", "123")
# s4.add_house("Tehran", "123", 120, "Sell", 1, 1200, 2, 1, "Nothing")
# s1 = main_housings[0].get_session("Shayan", "Kermani")
# s2 = main_housings[0].get_session("MyAcc", "123")
# s2.add_house("Tehran", "123", 120, 1, 1200, 2, 1, "Nothing", 0)
# s2.add_house("Karaj", "123", 110, 1, 12000, 2, 1, "Nothing", 0)
# s2.add_house("Tehran", "123", 130, 1, 120000, 2, 1, "Nothing", 2000)
# s1.check_approval(main_housings[0].house_requests[0])
# s1.check_approval(main_housings[0].house_requests[0])
# s1.check_approval(main_housings[0].house_requests[0])
# s1.add_admin("AHY", "2007", "Amirhossein")
# print(s2.find_home_list(120, 120000, 0, 1, 2000))

# print(s1.find_home(110, 1300, 0, 1, 0 , 1))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())