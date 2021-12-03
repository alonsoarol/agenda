from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
import sqlite3 as sql
from re import split



class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("agenda.ui", self)
        self.labelContacto.clear()
        self.telefono.setValidator(QtGui.QIntValidator())
        self.altura.setValidator(QtGui.QIntValidator())
        self.peso.setValidator(QtGui.QIntValidator())
        self.key = ''
        self.loadList()

        self.bEliminar.setEnabled(False)
        self.bEditar.setEnabled(False)
        self.bAceptar.setEnabled(False)
        self.bCancelar.setEnabled(False)


        self.lista.itemSelectionChanged.connect(self.itemChanged)
        self.fieldDisabled()
        self.bEditar.clicked.connect(self.edit)
        self.bNuevo.clicked.connect(self.new)
        self.bAceptar.clicked.connect(self.accept)
        self.bEliminar.clicked.connect(self.delete)
        self.bCancelar.clicked.connect(self.cancel)
        self.bSalir.clicked.connect(self.exit)

    def check(self):
        item = self.lista.currentItem().text()
        id = split('\D+', item)
        nombre = self.nombre.text()
        apelllido = self.apellido.text()
        email = self.email.text()
        tel = self.telefono.text()
        dir = self.direccion.text()
        fecha = self.fechanac.text()
        altura = self.altura.text()
        peso = self.peso.text()
        lista1 = [id[0], nombre, apelllido, email, tel, dir, fecha, altura, peso]
        conn = sql.connect('agenda.db')
        cursor = conn.cursor()
        instruccion = f'SELECT * FROM contactos WHERE id = {id[0]}'
        carga = cursor.execute(instruccion)
        lista2 = []
        for fila in carga:
            lista2.append(str(fila[0]))
            lista2.append(str(fila[1]))
            lista2.append(str(fila[2]))
            lista2.append(str(fila[3]))
            lista2.append(str(fila[4]))
            lista2.append(str(fila[5]))
            lista2.append(str(fila[6]))
            lista2.append(str(fila[7]))
            lista2.append(str(fila[8]))
        if lista1 == lista2:
            return True
        else:
            return False

    def exit(self):
        # self.lista.currentItem().setSelected(False)
        win.close()
        

    def delete(self):
        msg = QMessageBox()
        msg.setText('Esta seguro de eliminar el contacto seleccionado?')
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setIcon(QMessageBox.Question)
        respuesta = msg.exec_()
        if respuesta == QMessageBox.Yes:
            self.labelContacto.clear()
            item = self.lista.currentItem().text()
            id = split('\D+', item)
            conn = sql.connect('agenda.db')
            cursor = conn.cursor()
            instruccion = f'DELETE FROM contactos WHERE id = {id[0]}'
            carga = cursor.execute(instruccion)
            conn.commit()
            conn.close()
            self.loadList()
            self.fieldsClear()
            self.bEditar.setEnabled(False)
            self.bEliminar.setEnabled(False)
    
    def accept(self):
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        email = self.email.text()
        tel = self.telefono.text()
        dir = self.direccion.text()
        fecha = self.fechanac.text()
        altura = self.altura.text()
        peso = self.peso.text()
        if nombre =='' or apellido =='' or email =='' or tel=='' or dir=='' or fecha=='' or altura=='' or peso=='':
                msg = QMessageBox()
                msg.setText('Debe completar todos los campos')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
        
        elif self.key == 1:
            msg = QMessageBox()
            msg.setText('Desea ingresar el nuevo registro?')
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setIcon(QMessageBox.Question)
            respuesta = msg.exec_()
            if respuesta == QMessageBox.Yes: 
                self.labelContacto.clear()
                conn = sql.connect('agenda.db')
                cursor = conn.cursor()
                instruccion = f"INSERT INTO contactos VALUES(NULL, '{nombre}', '{apellido}', '{email}', {tel}, '{dir}', '{fecha}', {altura}, {peso})"
                cursor.execute(instruccion)
                conn.commit()
                conn.close()
                self.loadList()
                self.fieldsClear()
                self.fieldDisabled()
                self.bNuevo.setEnabled(True)
                self.bAceptar.setEnabled(False)
                self.bCancelar.setEnabled(False)
                self.bEditar.setEnabled(False)
                self.bEliminar.setEnabled(False)

        elif self.key == 2:
            flag = self.check()
            if flag == False:
                msg = QMessageBox()
                msg.setText('Desea guardar los cambios?')
                msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
                msg.setIcon(QMessageBox.Question)
                respuesta = msg.exec_()
                if respuesta == QMessageBox.Yes:
                    self.labelContacto.clear()
                    item = self.lista.currentItem().text()
                    id = split('\D+', item)
                    conn = sql.connect('agenda.db')
                    cursor = conn.cursor()
                    instruccion = f"""UPDATE contactos SET nombre ='{nombre}', apellido ='{apellido}', 
                    email ='{email}', telefono ={tel}, direccion ='{dir}', fecha_nacimiento ='{fecha}', 
                    altura ={altura}, peso ={peso} WHERE id ='{id[0]}'"""

                    cursor.execute(instruccion)
                    conn.commit()
                    conn.close()
                    self.loadList()
                    self.fieldsClear()
                    self.fieldDisabled()
                    self.bNuevo.setEnabled(True)
                    self.bAceptar.setEnabled(False)
                    self.bCancelar.setEnabled(False)
                    self.bEditar.setEnabled(False)
                    self.bEliminar.setEnabled(False)

    def cancel(self):
        try:
            self.lista.currentItem().setSelected(False)
            self.labelContacto.clear()
            self.loadList()
            self.fieldsClear()
            self.fieldDisabled()
            self.bNuevo.setEnabled(True)
            self.bAceptar.setEnabled(False)
            self.bCancelar.setEnabled(False)
            self.bEditar.setEnabled(False)
            self.bEliminar.setEnabled(False)
        except:
            self.labelContacto.clear()
            self.loadList()
            self.fieldsClear()
            self.fieldDisabled()
            self.bNuevo.setEnabled(True)
            self.bAceptar.setEnabled(False)
            self.bCancelar.setEnabled(False)
            self.bEditar.setEnabled(False)
            self.bEliminar.setEnabled(False)




    def new(self):
        self.labelContacto.clear()
        self.bEditar.setEnabled(False)
        self.bEliminar.setEnabled(False)
        self.bNuevo.setEnabled(False)
        self.bAceptar.setEnabled(True)
        self.bCancelar.setEnabled(True)
        self.fieldEnabled()
        self.fieldsClear()
        self.nombre.setFocus()
        self.key = 1


    def edit(self):
        self.fieldEnabled()
        self.nombre.setFocus()
        self.bEditar.setEnabled(False)
        self.bEliminar.setEnabled(False)
        self.bNuevo.setEnabled(False)
        self.bAceptar.setEnabled(True)
        self.bCancelar.setEnabled(True)
        self.key = 2


    def fieldsClear(self):
        self.nombre.clear()
        self.apellido.clear()
        self.email.clear()
        self.telefono.clear()
        self.direccion.clear()
        self.fechanac.clear()
        self.altura.clear()
        self.peso.clear()

    def fieldEnabled(self):
        self.nombre.setEnabled(True)
        self.apellido.setEnabled(True)
        self.email.setEnabled(True)
        self.telefono.setEnabled(True)
        self.direccion.setEnabled(True)
        self.fechanac.setEnabled(True)
        self.altura.setEnabled(True)
        self.peso.setEnabled(True)

    def fieldDisabled(self):
        self.nombre.setEnabled(False)
        self.apellido.setEnabled(False)
        self.email.setEnabled(False)
        self.telefono.setEnabled(False)
        self.direccion.setEnabled(False)
        self.fechanac.setEnabled(False)
        self.altura.setEnabled(False)
        self.peso.setEnabled(False)

    def itemChanged(self):
        self.labelContacto.setText(self.lista.currentItem().text())
        self.bNuevo.setEnabled(True)
        self.bAceptar.setEnabled(False)
        self.bCancelar.setEnabled(False)
        self.fieldDisabled()
        self.bEditar.setEnabled(True)
        self.bEliminar.setEnabled(True)
        item = self.lista.currentItem().text()
        id = split('\D+', item)
        conn = sql.connect('agenda.db')
        cursor = conn.cursor()
        instruccion = f'SELECT * FROM contactos WHERE id = {id[0]}'
        carga = cursor.execute(instruccion)
        for fila in carga:
            self.nombre.setText(f'{fila[1]}')
            self.apellido.setText(f'{fila[2]}')
            self.email.setText(f'{fila[3]}')
            self.telefono.setText(f'{fila[4]}')
            self.direccion.setText(f'{fila[5]}')
            self.fechanac.setText(f'{fila[6]}')
            self.altura.setText(f'{fila[7]}')
            self.peso.setText(f'{fila[8]}')
        conn.commit()
        conn.close() 

    def loadList(self):
        self.lista.clear()
        conn = sql.connect('agenda.db')
        cursor = conn.cursor()
        instruccion = f'SELECT * FROM contactos'
        carga = cursor.execute(instruccion)
        for fila in carga:
            self.lista.addItem(f'{fila[0]}.  {fila[1]} {fila[2]}')
        conn.commit()
        conn.close() 
        


app = QApplication([])
win = MiVentana()
win.show()
app.exec_()