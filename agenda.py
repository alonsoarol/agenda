from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic
import sqlite3 as sql
from re import split


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("agenda.ui", self)
        self.key = ''
        self.cargaLista()

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

        

    def delete(self):
        item = self.lista.currentItem().text()
        id = split('\D+', item)
        conn = sql.connect('agenda.db')
        cursor = conn.cursor()
        instruccion = f'DELETE FROM contactos WHERE id = {id[0]}'
        carga = cursor.execute(instruccion)
        conn.commit()
        conn.close()
        self.cargaLista()
    
    def accept(self):
        if self.key == 1:
            nombre = self.nombre.text()
            apelllido = self.apellido.text()
            email = self.email.text()
            tel = self.telefono.text()
            dir = self.direccion.text()
            fecha = self.fechanac.text()
            altura = self.altura.text()
            peso = self.peso.text()

            conn = sql.connect('agenda.db')
            cursor = conn.cursor()
            instruccion = f"INSERT INTO contactos VALUES(NULL, '{nombre}', '{apelllido}', '{email}', {tel}, '{dir}', '{fecha}', {altura}, {peso})"
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
            self.cargaLista()
            self.fieldsClear()
            self.fieldDisabled()
            self.bNuevo.setEnabled(True)
            self.bAceptar.setEnabled(False)
            self.bCancelar.setEnabled(False)

        elif self.key == 2:
            nombre = self.nombre.text()
            apelllido = self.apellido.text()
            email = self.email.text()
            tel = self.telefono.text()
            dir = self.direccion.text()
            fecha = self.fechanac.text()
            altura = self.altura.text()
            peso = self.peso.text()

            item = self.lista.currentItem().text()
            id = split('\D+', item)
            conn = sql.connect('agenda.db')
            cursor = conn.cursor()
            instruccion = f"""UPDATE contactos SET nombre ='{nombre}', apellido ='{apelllido}', 
            email ='{email}', telefono ={tel}, direccion ='{dir}', fecha_nacimiento ='{fecha}', 
            altura ={altura}, peso ={peso} WHERE id ='{id[0]}'"""

            cursor.execute(instruccion)
            conn.commit()
            conn.close()
            self.cargaLista()
            self.fieldsClear()
            self.fieldDisabled()
            self.bNuevo.setEnabled(True)
            self.bAceptar.setEnabled(False)
            self.bCancelar.setEnabled(False)

    def cancel(self):
        self.cargaLista()
        self.fieldsClear()
        self.fieldDisabled()
        self.bNuevo.setEnabled(True)
        self.bAceptar.setEnabled(False)
        self.bCancelar.setEnabled(False)
        self.bEditar.setEnabled(False)
        self.bEliminar.setEnabled(False)




    def new(self):
        self.bNuevo.setEnabled(False)
        self.bAceptar.setEnabled(True)
        self.bCancelar.setEnabled(True)
        self.lista.currentItem().setSelected(False)
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

    def cargaLista(self):
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
