
import re
import cx_Oracle
import sys
from datetime import datetime
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QApplication, QMainWindow, QDialog, QWidget, QLabel, \
    QVBoxLayout


# exemple de comenzi in python-sql
def databaseEX():
    dataTuples = [('xyz', datetime(2020, 1, 1), 7685), ('abc', datetime(2020, 12, 12), 85)]
    sqlDelete = 'delete from tabela where atr1=:1 or(atr2=:2 and atr3=:3)'
    sqlText = 'inset into "tabela"(atr1,atr2,atr3) values(:1,:2,:3)'
    curs.execute(sqlText, dataTuples[1])
    curs.execute(sqlText, dataTuples)  # insereaza ambele seturi de date din dataTuples


conStr = 'bd012/parola@bd-dc.cs.tuiasi.ro:1539/orcl'

conn = 0
curs = 0
cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient")
conn = cx_Oracle.connect(user=r"bd012", password="parola", dsn=r"bd-dc.cs.tuiasi.ro:1539/orcl")
curs = conn.cursor()
print("ConexOK")


# try:
#   conn = cx_Oracle.connect(user=r"bd012",password="parola",dsn=r"bd-dc.cs.tuiasi.ro:1539/orcl")
#  curs=conn.cursor()
# except Exception as err:
#   print('Eroare la conectare db')
#  print(err)
# finally:
#  if(conn):
#     print("<-Nu e eroare ->merge")
def conexiune():
    curs.execute('insert into gen_film(nume_gen)'
                 'values(:asdfjasdasdf)')
    curs.commit()
    # curs.execute('select * from combinatie')
    # #curs.execute('insert into gen_film(nume_gen) values(''asdfjasdasdf'')')
    # ui.tableProgram.setRowCount(0)
    # for index, row in enumerate(curs):
    #     ui.tableProgram.insertRow(index)
    #     for colum, cell in enumerate(row):
    #         ui.tableProgram.setItem(index, colum, QTableWidgetItem(str(cell)))


def testare(nr):
    print(nr)


def convertMonth(nr):
    switch = {'1': 'JAN', '2': 'FEB', '3': 'MAR', '4': 'APR', '5': 'MAY', '6': 'JUN', '7': 'JUL', '8': 'AUG',
              '9': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'}
    str = switch[str(nr)]
    return str

def convert_date_format(date_string):
    date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    month_abbr = date.strftime('%b').upper()
    new_date_string = date.strftime(f'%d-{month_abbr}-%y %H:%M:%S')
    return new_date_string

idFilme = []
numeFilme = []
textFilm = []
anFilm = []
minuteFilm=[]
genFilme=[]
numeActor=[]
idActor=[]
numeGen=[]
idGen=[]
class Ui_MainWindow(object):
    def __init__(self):
        self.buttonStergeFilm = None
        self.buttonStergeBilete = None
        self.comboBoxGen = None
        self.comboBoxActor = None
        self.lineEditDataLansare = None
        self.lineEditNumarMinute = None
        self.lineEditNumeFilm = None
        self.tableFilm = None
        self.textBrowser_6 = None
        self.textBrowser_5 = None
        self.textBrowser_4 = None
        self.textBrowser_3 = None
        self.textBrowser_2 = None
        self.textBrowser_1 = None
        self.labelAprobareAchzitie = None
        self.comboBoxCosTip = None
        self.comboBoxCosData = None
        self.labelCosFilm = None
        self.tabADMIN = None
        self.tabWidget = None
        self.comboBoxProgramFilm = None
        self.buttonStergeProgram = None
        self.buttonRefreshProgram = None
        self.tableProgram = None
        self.id_film_buy = None
        self.film_nume_buy=None
        self.numar_sala_buy = None
    def _removeProgramRow(self):
        if self.tableProgram.rowCount() > 0:
            currentRow = self.tableProgram.currentRow()
            id_comb=self.tableProgram.currentItem().text()
            print(id_comb)
            curs.execute("delete from bilet where id_combinatie="+str(id_comb))#sa sterg mai intai toate biletele cumparate la acel film ca sa scap de foreign keyurile din BILET
            conn.commit()
            curs.execute("delete from combinatie where id_combinatie=" + str(id_comb))
            conn.commit()
            self.tableProgram.removeRow(currentRow)
    def _removeBileteRow(self):
        if self.tableBilete.rowCount() > 0:
            currentRow = self.tableBilete.currentRow()
            id_bilet = self.tableBilete.currentItem().text()
            curs.execute("delete from bilet where id_bilet=" + str(id_bilet))
            conn.commit()
            self.tableBilete.removeRow(currentRow)
    def _removeFilmRow(self):
        if self.tableFilm.rowCount() > 0:
            currentRow = self.tableFilm.currentRow()
            id_film = self.tableFilm.currentItem().text()
            curs.execute("delete from bilet where id_film=" + str(id_film))
            conn.commit()
            curs.execute("delete from combinatie where id_film=" + str(id_film))
            conn.commit()
            curs.execute("delete from detalii_film where id_film=" + str(id_film))
            conn.commit()
            curs.execute("delete from film where id_film= " + str(id_film))
            conn.commit()
            self.tableFilm.removeRow(currentRow)
    def _refreshBilete(self):
        curs.execute('select * from bilet')
        result = curs.fetchall()
        self.tableBilete.setRowCount(0)
        for index, row in enumerate(result):
            self.tableBilete.insertRow(index)
            for column, cell in enumerate(row):
                self.tableBilete.setItem(index, column, QTableWidgetItem(str(cell)))
    def _refreshFilme(self):
        curs.execute('select * from film')
        result = curs.fetchall()
        self.tableFilm.setRowCount(0)
        for index, row in enumerate(result):
            self.tableFilm.insertRow(index)
            for column, cell in enumerate(row):
                self.tableFilm.setItem(index, column, QTableWidgetItem(str(cell)))
        nume=curs.execute('select id_actor,nume_actor from actor order by id_actor').fetchall()
        index = 0
        for row in nume:
            numeActor.append(str(row[1]).replace('(', '').replace(')', '').replace(',', '').replace("'", ''))
            idActor.append(row[0])
            self.comboBoxActor.addItem(numeActor[index])  # row[0]
            index += 1
        nume = curs.execute('select id_gen,nume_gen from gen_film order by id_gen').fetchall()
        index = 0
        for row in nume:
            numeGen.append(str(row[1]).replace('(', '').replace(')', '').replace(',', '').replace("'", ''))
            idGen.append(row[0])
            self.comboBoxGen.addItem(numeGen[index])  # row[0]
            index += 1
    def _refreshProgram(self):
        idFilme.clear()
        numeFilme.clear()
        textFilm.clear()
        anFilm.clear()
        minuteFilm.clear()
        genFilme.clear()

        # curs.execute('select * from combinatie')  # use triple quotes if you want to spread your query across multiple lines
        self.comboBoxProgramFilm.clear()
        self.comboBoxProgramSala.clear()
        print("1")
        curs.execute('select * from combinatie')
        result = curs.fetchall()
        self.tableProgram.setRowCount(0)
        print("2")
        for index, row in enumerate(result):
            self.tableProgram.insertRow(index)
            for column, cell in enumerate(row):
                self.tableProgram.setItem(index, column, QTableWidgetItem(str(cell)))

        curs.execute('select id_sala from sala')  # pun nr  salilor in combobox
        result = curs.fetchall()
        for row in enumerate(result):
            self.comboBoxProgramSala.addItem(str(row[1]).replace("(", "").replace(")", "").replace(",", ""), row[1])
        print("3")
        curs.execute('select id_film,data_lansare from film order by id_film')  # iau data de lansare si pun intr-un vector
        nume = curs.fetchall()
        for row in nume:
            anFilm.append(str(row[1]).replace(' 00:00:00', ''))

        curs.execute(
            'select id_film,nume_film,nr_de_minute from film order by id_film')  # iau numele filmelor si le pun intr-un array impreuna cu datile de lansare
        nume = curs.fetchall()
        index = 0
        print("4")
        for row in nume:
            numeFilme.append(str(row[1]).replace('(', '').replace(')', '').replace(',', '').replace("'", ''))
            idFilme.append(row[0])
            minuteFilm.append(row[2])
            textFilm.append(numeFilme[index] + " " + str(anFilm[index])[0:4])
            self.comboBoxProgramFilm.addItem(textFilm[index])  # row[0]
            index += 1
        print("5")
        for i in range(len(idFilme)):
            a = curs.execute(
                "select nume_gen from gen_film where id_gen=(select id_gen from detalii_film where id_film=" + str(
                    idFilme[i]) + ")").fetchone()
            genFilme.append(a[0])
        print("6")
        text=[self.textBrowser_1,self.textBrowser_2,self.textBrowser_3,self.textBrowser_4,self.textBrowser_5,self.textBrowser_6]
        for i in range(len(text)):
            text[i].setText("")
        for i in range(len(numeFilme)):
            text[i].setText("nume: "+str(numeFilme[i])+"   \t\tdata_lansarii:"+str(anFilm[i]) +"\ngen:"+str(genFilme[i])+"\t\t"+str(minuteFilm[i])+" minute")
        print("7")
    def _adaugaProgram(self):
        data = 0
        if self.lineEditProgramData.text() and (self.comboBoxProgramFilm.currentText() != '-') and (
                self.comboBoxProgramSala.currentText() != '-'):
            data = self.lineEditProgramData.text()
            match = re.match(
                r'^(0[1-9]|[12][0-9]|3[01])-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)-\d\d\s(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])$',
                data)
            if match:
                print("string ok ")
            else:
                QMessageBox.about(self.buttonAdaugaProgram, "Title1", "Data introdusa gresit")
                return
        else:
            QMessageBox.about(self.buttonAdaugaProgram, "Title", "Un camp e gol")
            return
        input_id_film = int(idFilme[self.comboBoxProgramFilm.currentIndex() - 1])
        input_id_sala = int(self.comboBoxProgramSala.currentText())
        nr_locuri = curs.execute("select nr_locuri_totale from sala where id_sala=" + str(input_id_sala)).fetchone()  # nr_locuri[0]

        curs.execute('select * from combinatie')
        result = curs.fetchall()
        for row in result:  ##verific daca aceeasi combinatie e in tabel
            if row[1] == input_id_film and row[2] == input_id_sala and data[7:9] == str(row[3])[2:4] and convertMonth(
                    str(row[3])[5:7]) == data[3:6] and str(row[3])[8:10] == data[0:2] and str(row[3])[11:19] == data[
                                                                                                                10:18]:  # an luna zi timp
                QMessageBox.about(self.buttonAdaugaProgram, "Title", "Mai incearca")
                return
        print(input_id_film, input_id_sala, data)
        curs.execute(
            "insert into combinatie(id_film,id_sala,data_ora_film,nr_locuri_libere) values(:B,:C,to_date(:D,'DD-MON-YY HH24:MI:SS'),:E)",
            (input_id_film, input_id_sala, data, nr_locuri[0]))
        conn.commit()
    def _changeTab(self, nr):
        print(len(idFilme),nr)
        if len(idFilme) < nr:
            return
        print("changetab")
        self.comboBoxCosData.clear()
        self.tabWidget.setCurrentIndex(1)
        self.labelCosFilm.setText(textFilm[nr - 1])
        self.numar_sala_buy = nr
        self.id_film_buy = idFilme[nr - 1]
        self.film_nume_buy=numeFilme[nr-1]
        result = curs.execute(
            "select data_ora_film from combinatie where id_film=" + str(self.id_film_buy) + "order by data_ora_film")
        for row in result:
            self.comboBoxCosData.addItem(str(row[0]))
    def _buyBilet(self):
        if self.labelCosFilm.text()!="--":
            data_tmp = convert_date_format(self.comboBoxCosData.currentText()) ##data combinatiei, convertita gata de inserare
            nume_id_tip_tmp=self.comboBoxCosTip.currentText()                  ##numele tipului de bilet=statut
            reducere_tmp=int(curs.execute("select reducere from tip_bilet where nume_tip=\'" + str(nume_id_tip_tmp) + "\'").fetchone()[0])
            id_tip_tmp=curs.execute("select id_tip from tip_bilet where nume_tip=\'" + str(nume_id_tip_tmp) + "\'").fetchone()[0] ##id-ul tipului biletului, de pus in tabela bilet
            varsta=int(self.lineEditVarsta.text())
            rand=int(self.lineEditCosRand.text())
            loc =int(self.lineEditCosLoc.text())

            # teste varsta-statut#
            # copil <14
            # adult >=14
            # student >=18
            # pensionar >=40
            # elev  <=19 and >=6
            # ia ultimul id si punel in bilet
            id_comb = curs.execute("select id_combinatie from combinatie where id_film=" + str(self.id_film_buy) + " and data_ora_film=to_date(\'" + data_tmp + "\','DD-MON-YY HH24:MI:SS')").fetchone()[0]

            curs.execute("select * from bilet ")
            result = curs.fetchall()

            for row in result:  ##verific daca acelasi bilet e in tabel
                print(row[1],row[3],row[7],row[8])
                if row[1] == self.id_film_buy  and row[3]==id_comb and row[7]==loc and row[8]==rand:
                    QMessageBox.about(self.buttonAdaugaProgram, "Title", "Loc ocupat")
                    return

            curs.execute("insert into client(varsta,statut) values("+str(varsta)+",\'"+nume_id_tip_tmp+"\')") ##inserez clientul
            conn.commit()

            pret = 25 - reducere_tmp
            id_client_tmp = curs.execute("SELECT id_client FROM client WHERE ROWID = (SELECT MAX(ROWID) FROM client)").fetchone()[0]

            #print("insert into bilet(id_film,id_sala,id_combinatie,id_client,id_tip,pret,nr_loc,nr_rand) values("+str(self.id_film_buy)+","+str(self.numar_sala_buy)+","+str(id_comb)+","+str(id_client_tmp)+","+str(id_tip_tmp)+","+str(pret)+","+str(loc)+","+str(rand)+")")
            curs.execute("insert into bilet(id_film,id_sala,id_combinatie,id_client,id_tip,pret,nr_loc,nr_rand) "
                         "values("+str(self.id_film_buy)+","+str(self.numar_sala_buy)+","+str(id_comb)+","+str(id_client_tmp)+","+str(id_tip_tmp)+","+str(pret)+","+str(loc)+","+str(rand)+")")
            conn.commit()
            curs.execute("update combinatie set nr_locuri_libere =nr_locuri_libere-1 where id_combinatie="+str(id_comb))
            conn.commit()

            QMessageBox.about(self.buttonAdaugaProgram, "Title", "Biletul achizitionat cu succes")
            id_bilet=curs.execute("SELECT id_bilet FROM bilet WHERE ROWID = (SELECT MAX(ROWID) FROM bilet)").fetchone()[0]
            self.labelAprobareAchzitie.setText( "Biletul cu nr #"+str(id_bilet)+" |  "+str(nume_id_tip_tmp)+" | loc: "+str(loc)+" | rand: "+str(rand)+" | film: "+str(self.film_nume_buy)+" | data: "+str(data_tmp)+" a fost achizitionat cu succes")
        else:
            QMessageBox.about(self.buttonAdaugaProgram, "Title", "Alege un film boo")

    def insertDetalii(self,flm):
        id_film = curs.execute("SELECT id_film FROM film WHERE ROWID = (SELECT MAX(ROWID) FROM film)").fetchone()[0]
        print(id_film)
        id_film = curs.execute("SELECT id_film FROM film WHERE ROWID = (SELECT MAX(ROWID) FROM film)").fetchone()[0]
        print(id_film)
        print("ok")
        input_id_gen = int(idGen[self.comboBoxGen.currentIndex()])
        input_id_actor = int(idActor[self.comboBoxActor.currentIndex()])
        nota = self.lineEditNota.text()
        print("test")
        print("select id_film from film where nume_film=\'" + str(flm)+"\'")
        id_film = curs.execute("select id_film from film where nume_film=\'" + str(flm)+"\'").fetchone()[0]
        print(id_film)

        print("insert into detalii_film(id_film,nota_film,id_actor,id_gen) values(" + str(
            id_film) + "," + nota + "," + str(input_id_actor) + "," + str(input_id_gen) + ")")
        curs.execute("insert into detalii_film(id_film,nota_film,id_actor,id_gen) values(" + str(
            id_film) + "," + nota + "," + str(input_id_actor) + "," + str(input_id_gen) + ")")
        conn.commit()

        print("done")

    def _adaugaFilm(self):
        if  self.tableFilm.rowCount() < 6:
            film=self.lineEditNumeFilm.text()
            data_temp=self.lineEditDataLansare.text()
            match = re.match(
                r'^(0[1-9]|[12][0-9]|3[01])-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)-\d\d\s(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])$',
                data_temp)
            if match:
                print("string ok ")
            else:
                QMessageBox.about(self.buttonAdaugaProgram, "Title1", "Data introdusa gresit")
                return
            nr_min=self.lineEditNumarMinute.text()
            print("insert into film(nume_film,data_lansare,nr_de_minute) values(\'"+film+"\',to_date(\'"+data_temp+"\', 'DD-MON-YY HH24:MI:SS'),"+str(nr_min)+")")

            id_film = curs.execute("SELECT id_film FROM film WHERE ROWID = (SELECT MAX(ROWID) FROM film)").fetchone()[0]

            # 02-DEC-26 13:28:24
            print(id_film)


            curs.execute("insert into film(nume_film,data_lansare,nr_de_minute) values(\'"+str(film)+"\',to_date(\'"+str(data_temp)+"\', 'DD-MON-YY HH24:MI:SS'),"+str(nr_min)+")")
            conn.commit()
            conn.commit()
            for i in range(100000):
                print("-")

            print("intra filmul")

            self.insertDetalii(film)
        else:
            QMessageBox.about(self.buttonAdaugaProgram, "Title", "Numar maxim de filme")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 732)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("font: 16pt \"Open Sans\";")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.tab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1041, 860))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem = QtWidgets.QSpacerItem(393, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label.setStyleSheet("font: 16pt \"Lucida Console\";\n"
                                 "color:rgb(255, 121, 26);")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(393, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 0, 2, 1, 1)
        self.pushButtonRefreshFilme = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.pushButtonRefreshFilme.setObjectName("pushButtonRefreshFilme")
        self.gridLayout_5.addWidget(self.pushButtonRefreshFilme, 0, 3, 1, 1)
        self.pushButtonRefreshFilme.clicked.connect(self._refreshFilme)

        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.frame.setMinimumSize(QtCore.QSize(0, 800))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.textBrowser_1 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_1.setObjectName("textBrowser_1")
        self.horizontalLayout_6.addWidget(self.textBrowser_1)
        self.pushButton_1 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_1.setObjectName("pushButton_1")
        self.horizontalLayout_6.addWidget(self.pushButton_1)
        self.pushButton_1.clicked.connect(lambda: self._changeTab(1))

        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_3)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.horizontalLayout_5.addWidget(self.textBrowser_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_5.addWidget(self.pushButton_2)
        self.pushButton_2.clicked.connect(lambda: self._changeTab(2))

        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.horizontalLayout_4.addWidget(self.textBrowser_3)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_4.addWidget(self.pushButton_3)
        self.pushButton_3.clicked.connect(lambda: self._changeTab(3))

        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.horizontalLayout_3.addWidget(self.textBrowser_4)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        self.pushButton_4.clicked.connect(lambda: self._changeTab(4))

        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.groupBox_5)
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.horizontalLayout_2.addWidget(self.textBrowser_5)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_5.clicked.connect(lambda: self._changeTab(5))

        self.verticalLayout_4.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.groupBox_6)
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.horizontalLayout.addWidget(self.textBrowser_6)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.pushButton_6.clicked.connect(lambda: self._changeTab(6))

        self.verticalLayout_4.addWidget(self.groupBox_6)
        self.gridLayout_5.addWidget(self.frame, 1, 0, 1, 4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.labelVarsta = QtWidgets.QLabel(self.tab_2)
        self.labelVarsta.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelVarsta.setObjectName("labelVarsta")
        self.gridLayout.addWidget(self.labelVarsta, 8, 0, 1, 1)
        self.labelAprobareAchzitie = QtWidgets.QLabel(self.tab_2)
        self.labelAprobareAchzitie.setObjectName("labelAprobareAchzitie")
        self.gridLayout.addWidget(self.labelAprobareAchzitie, 15, 0, 1, 4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 7, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.pushButtonCumpara = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonCumpara.setObjectName("pushButtonCumpara")
        self.gridLayout.addWidget(self.pushButtonCumpara, 14, 4, 1, 1)
        self.pushButtonCumpara.clicked.connect(self._buyBilet)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem3, 9, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 10, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem5, 3, 2, 1, 1)
        self.lineEditCosRand = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditCosRand.setObjectName("lineEditCosRand")
        self.gridLayout.addWidget(self.lineEditCosRand, 10, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem6, 0, 4, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem7, 5, 2, 1, 1)
        self.lineEditCosLoc = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditCosLoc.setObjectName("lineEditCosLoc")
        self.gridLayout.addWidget(self.lineEditCosLoc, 12, 2, 1, 1)
        self.labelCosFilm = QtWidgets.QLabel(self.tab_2)
        self.labelCosFilm.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.labelCosFilm.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelCosFilm.setObjectName("labelCosFilm")
        self.gridLayout.addWidget(self.labelCosFilm, 2, 2, 1, 1)
        self.comboBoxCosData = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxCosData.setObjectName("comboBoxCosData")
        self.gridLayout.addWidget(self.comboBoxCosData, 4, 2, 1, 1)
        self.lineEditVarsta = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditVarsta.setObjectName("lineEditVarsta")
        self.gridLayout.addWidget(self.lineEditVarsta, 8, 2, 1, 1)
        self.comboBoxCosTip = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxCosTip.setObjectName("comboBoxCosTip")
        self.gridLayout.addWidget(self.comboBoxCosTip, 6, 2, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem8, 11, 2, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem9, 13, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 12, 0, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem10, 1, 4, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem11, 1, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem12, 1, 3, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem13, 14, 3, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setMouseTracking(False)
        self.tab_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tabADMIN = QtWidgets.QTabWidget(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tabADMIN.setFont(font)
        self.tabADMIN.setObjectName("tabADMIN")
        self.tabProgram = QtWidgets.QWidget()
        self.tabProgram.setObjectName("tabProgram")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabProgram)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEditProgramData = QtWidgets.QLineEdit(self.tabProgram)
        self.lineEditProgramData.setObjectName("lineEditProgramData")
        self.gridLayout_2.addWidget(self.lineEditProgramData, 7, 2, 1, 2)
        self.buttonStergeProgram = QtWidgets.QPushButton(self.tabProgram)
        self.buttonStergeProgram.setObjectName("buttonStergeProgram")
        self.gridLayout_2.addWidget(self.buttonStergeProgram, 8, 0, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(654, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem14, 8, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.tabProgram)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 6, 2, 1, 2)
        self.buttonAdaugaProgram = QtWidgets.QPushButton(self.tabProgram)
        self.buttonAdaugaProgram.setObjectName("buttonAdaugaProgram")
        self.gridLayout_2.addWidget(self.buttonAdaugaProgram, 8, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.tabProgram)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 4, 2, 1, 1)
        self.tableProgram = QtWidgets.QTableWidget(self.tabProgram)
        self.tableProgram.setMinimumSize(QtCore.QSize(100, 0))
        self.tableProgram.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.tableProgram.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableProgram.setWordWrap(True)
        self.tableProgram.setObjectName("tableProgram")
        self.tableProgram.setColumnCount(5)
        self.tableProgram.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableProgram.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableProgram.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableProgram.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableProgram.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableProgram.setHorizontalHeaderItem(4, item)
        self.gridLayout_2.addWidget(self.tableProgram, 0, 0, 8, 2)
        self.comboBoxProgramFilm = QtWidgets.QComboBox(self.tabProgram)
        self.comboBoxProgramFilm.setObjectName("comboBoxProgramFilm")
        self.gridLayout_2.addWidget(self.comboBoxProgramFilm, 3, 2, 1, 2)
        self.comboBoxProgramSala = QtWidgets.QComboBox(self.tabProgram)
        self.comboBoxProgramSala.setObjectName("comboBoxProgramSala")
        self.gridLayout_2.addWidget(self.comboBoxProgramSala, 5, 2, 1, 2)
        self.label_12 = QtWidgets.QLabel(self.tabProgram)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 2, 2, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem15, 1, 2, 1, 1)
        self.buttonRefreshProgram = QtWidgets.QPushButton(self.tabProgram)
        self.buttonRefreshProgram.setObjectName("buttonRefreshProgram")
        self.gridLayout_2.addWidget(self.buttonRefreshProgram, 0, 2, 1, 1)
        self.buttonRefreshProgram.clicked.connect(self._refreshProgram)

        self.tabADMIN.addTab(self.tabProgram, "")
        self.tabBilete = QtWidgets.QWidget()
        self.tabBilete.setObjectName("tabBilete")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabBilete)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableBilete = QtWidgets.QTableWidget(self.tabBilete)
        self.tableBilete.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.tableBilete.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableBilete.setWordWrap(True)
        self.tableBilete.setObjectName("tableBilete")
        self.tableBilete.setColumnCount(9)
        self.tableBilete.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBilete.setHorizontalHeaderItem(8, item)
        self.gridLayout_3.addWidget(self.tableBilete, 0, 0, 1, 5)
        self.buttonStergeBilete = QtWidgets.QPushButton(self.tabBilete)
        self.buttonStergeBilete.setObjectName("buttonStergeBilete")
        self.gridLayout_3.addWidget(self.buttonStergeBilete, 1, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem16, 1, 1, 1, 1)
        self.buttonRefreshBilete = QtWidgets.QPushButton(self.tabBilete)
        self.buttonRefreshBilete.setObjectName("buttonRefreshBilete")
        self.gridLayout_3.addWidget(self.buttonRefreshBilete, 1, 2, 1, 1)
        self.buttonRefreshBilete.clicked.connect(self._refreshBilete)

        spacerItem17 = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem17, 1, 3, 1, 1)
        spacerItem18 = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem18, 1, 4, 1, 1)
        self.tabADMIN.addTab(self.tabBilete, "")
        self.tabFilm = QtWidgets.QWidget()
        self.tabFilm.setObjectName("tabFilm")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabFilm)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tableFilm = QtWidgets.QTableWidget(self.tabFilm)
        self.tableFilm.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.tableFilm.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableFilm.setWordWrap(True)
        self.tableFilm.setObjectName("tableFilm")
        self.tableFilm.setColumnCount(4)
        self.tableFilm.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableFilm.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableFilm.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableFilm.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableFilm.setHorizontalHeaderItem(3, item)
        self.gridLayout_4.addWidget(self.tableFilm, 0, 0, 14, 4)
        self.label_18 = QtWidgets.QLabel(self.tabFilm)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 0, 4, 1, 1)
        self.lineEditNumeFilm = QtWidgets.QLineEdit(self.tabFilm)
        self.lineEditNumeFilm.setObjectName("lineEditNumeFilm")
        self.gridLayout_4.addWidget(self.lineEditNumeFilm, 1, 4, 1, 3)
        self.label_19 = QtWidgets.QLabel(self.tabFilm)
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 2, 4, 1, 3)
        self.lineEditNumarMinute = QtWidgets.QLineEdit(self.tabFilm)
        self.lineEditNumarMinute.setObjectName("lineEditNumarMinute")
        self.gridLayout_4.addWidget(self.lineEditNumarMinute, 3, 4, 1, 3)
        self.label_8 = QtWidgets.QLabel(self.tabFilm)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 4, 4, 1, 3)
        self.comboBoxGen = QtWidgets.QComboBox(self.tabFilm)
        self.comboBoxGen.setObjectName("comboBoxGen")
        self.gridLayout_4.addWidget(self.comboBoxGen, 5, 4, 1, 3)
        self.label_10 = QtWidgets.QLabel(self.tabFilm)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 6, 4, 1, 3)
        self.comboBoxActor = QtWidgets.QComboBox(self.tabFilm)
        self.comboBoxActor.setObjectName("comboBoxActor")
        self.gridLayout_4.addWidget(self.comboBoxActor, 7, 4, 1, 3)
        self.label_11 = QtWidgets.QLabel(self.tabFilm)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 8, 4, 1, 3)
        self.lineEditNota = QtWidgets.QLineEdit(self.tabFilm)
        self.lineEditNota.setObjectName("lineEditNota")
        self.gridLayout_4.addWidget(self.lineEditNota, 9, 4, 1, 3)
        spacerItem19 = QtWidgets.QSpacerItem(26, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(spacerItem19, 10, 4, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.tabFilm)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("")
        self.label_20.setObjectName("label_20")
        self.gridLayout_4.addWidget(self.label_20, 11, 4, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.tabFilm)
        self.label_9.setStyleSheet("font: 10pt \"Open Sans\";")
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 11, 6, 1, 1)
        self.lineEditDataLansare = QtWidgets.QLineEdit(self.tabFilm)
        self.lineEditDataLansare.setObjectName("lineEditDataLansare")
        self.gridLayout_4.addWidget(self.lineEditDataLansare, 12, 4, 1, 3)
        self.buttonAdaugaFilm = QtWidgets.QPushButton(self.tabFilm)
        self.buttonAdaugaFilm.setObjectName("buttonAdaugaFilm")
        self.gridLayout_4.addWidget(self.buttonAdaugaFilm, 13, 5, 1, 2)
        self.buttonAdaugaFilm.clicked.connect(self._adaugaFilm)

        spacerItem20 = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(spacerItem20, 14, 0, 1, 1)
        self.buttonRefreshFilm = QtWidgets.QPushButton(self.tabFilm)
        self.buttonRefreshFilm.setObjectName("buttonRefreshFilm")
        self.gridLayout_4.addWidget(self.buttonRefreshFilm, 14, 1, 1, 1)
        self.buttonRefreshFilm.clicked.connect(self._refreshFilme)

        spacerItem21 = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(spacerItem21, 14, 2, 1, 1)
        self.buttonStergeFilm = QtWidgets.QPushButton(self.tabFilm)
        self.buttonStergeFilm.setObjectName("buttonStergeFilm")
        self.gridLayout_4.addWidget(self.buttonStergeFilm, 14, 3, 1, 1)
        self.buttonStergeFilm.clicked.connect(self._removeFilmRow)


        self.tabADMIN.addTab(self.tabFilm, "")
        self.verticalLayout_5.addWidget(self.tabADMIN)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        self.tabADMIN.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "CINEMATY "))
        self.pushButtonRefreshFilme.setText(_translate("MainWindow", "REFRESH"))
        self.pushButton_1.setText(_translate("MainWindow", "Cumpara bilet"))
        self.pushButton_2.setText(_translate("MainWindow", "Cumpara bilet"))
        self.pushButton_3.setText(_translate("MainWindow", "Cumpara bilet"))
        self.pushButton_4.setText(_translate("MainWindow", "Cumpara bilet"))
        self.pushButton_5.setText(_translate("MainWindow", "Cumpara bilet"))
        self.pushButton_6.setText(_translate("MainWindow", "Cumpara bilet"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Filme"))
        self.label_2.setText(_translate("MainWindow", "Cumpara bilet"))
        self.labelVarsta.setText(_translate("MainWindow", "Varsta"))
        self.labelAprobareAchzitie.setText(_translate("MainWindow", "----------"))
        self.label_3.setText(_translate("MainWindow", "Film"))
        self.label_5.setText(_translate("MainWindow", "Tipul biletului"))
        self.label_4.setText(_translate("MainWindow", "Data si ora "))
        self.pushButtonCumpara.setText(_translate("MainWindow", "Cumpara"))
        self.label_6.setText(_translate("MainWindow", "Rand"))
        self.labelCosFilm.setText(_translate("MainWindow", "--"))
        self.label_7.setText(_translate("MainWindow", "Loc"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Cos"))
        self.buttonStergeProgram.setText(_translate("MainWindow", "Sterge"))
        self.label_14.setText(_translate("MainWindow", "Data(Ex: 05-DEC-22 13:00:00)"))
        self.buttonAdaugaProgram.setText(_translate("MainWindow", "Adauga"))
        self.label_13.setText(_translate("MainWindow", "Sala"))
        item = self.tableProgram.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableProgram.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "FILM"))
        item = self.tableProgram.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "SALA"))
        item = self.tableProgram.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "DATA"))
        item = self.tableProgram.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "LOCURI"))
        self.label_12.setText(_translate("MainWindow", "FILM:"))
        self.buttonRefreshProgram.setText(_translate("MainWindow", "REFRESH"))
        self.tabADMIN.setTabText(self.tabADMIN.indexOf(self.tabProgram), _translate("MainWindow", "Program"))
        item = self.tableBilete.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID_BILET"))
        item = self.tableBilete.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "FILM"))
        item = self.tableBilete.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "SALA"))
        item = self.tableBilete.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "ID_PROGRAM"))
        item = self.tableBilete.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "CLIENT"))
        item = self.tableBilete.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "TIP"))
        item = self.tableBilete.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "PRET"))
        item = self.tableBilete.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "LOC"))
        item = self.tableBilete.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "RAND"))
        self.buttonStergeBilete.setText(_translate("MainWindow", "Sterge"))
        self.buttonRefreshBilete.setText(_translate("MainWindow", "Refresh"))
        self.tabADMIN.setTabText(self.tabADMIN.indexOf(self.tabBilete), _translate("MainWindow", "Bilete"))
        item = self.tableFilm.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID_FILM"))
        item = self.tableFilm.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "NUME_FILM"))
        item = self.tableFilm.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "DATA_LANSARE"))
        item = self.tableFilm.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "NR_DE_MINUTE"))
        self.label_18.setText(_translate("MainWindow", "Nume film"))
        self.label_19.setText(_translate("MainWindow", "Numar de minute"))
        self.label_8.setText(_translate("MainWindow", "genul filmului"))
        self.label_10.setText(_translate("MainWindow", "actor principal"))
        self.label_11.setText(_translate("MainWindow", "nota film"))
        self.label_20.setText(_translate("MainWindow", "Data lansarii:"))
        self.label_9.setText(_translate("MainWindow", "(Ex: 05-DEC-22 13:00:00)"))
        self.buttonAdaugaFilm.setText(_translate("MainWindow", "Adauga"))
        self.buttonRefreshFilm.setText(_translate("MainWindow", "Resfresh"))
        self.buttonStergeFilm.setText(_translate("MainWindow", "Sterge"))
        self.tabADMIN.setTabText(self.tabADMIN.indexOf(self.tabFilm), _translate("MainWindow", "Film"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "ADMIN"))


if __name__ == '__main__':

    data='02-DEC-26 13:28:24'


    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    id_film = curs.execute("SELECT id_film FROM film WHERE ROWID = (SELECT MAX(ROWID) FROM film)").fetchone()[0]
    print(id_film)
    ui._refreshProgram()
    result = curs.execute('select nume_tip from tip_bilet')  # pun nr  salilor in combobox
    for row in result:
        ui.comboBoxCosTip.addItem(str(row[0]))
    ui._refreshBilete()
    ui._refreshFilme()

    print(textFilm)


###################################################################################################################################


###################################################################################################################################
    sys.exit(app.exec())
    curs.close()
    conn.close()

    # print(dir(cx_Oracle))



