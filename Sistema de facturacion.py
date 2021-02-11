#!/usr/bin/env python
# -*- coding: utf-8 -*-


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# que la tabla contemple el ID y el nombre del producto y agregar una columna de stock
#agregar el stock cuando se agrega el producto
#agregar otra opcion 4 que descuente stock

import pymysql

conn = pymysql.connect(host ="localhost", port = 3306 , user = "root", passwd="", db="python")

cursor = conn.cursor()

i = 1

def consulta():
	cursor.execute("SELECT * from productos")
	tabla = cursor.fetchall()
	cursor.execute("SELECT * from stock")
	stock = cursor.fetchall()
	p = 0
	print('ID  Nombre  Precio   Stock')
	for n,name,price in tabla:
		print(n,name,price,stock[p][1])
		p = p + 1

try:
	cursor.execute("CREATE TABLE ventas(id INT, cantidad INT,monto INT)")
	cursor.execute("CREATE TABLE productos(id INT, nombre VARCHAR(20), precio INT)")
	cursor.execute("CREATE TABLE stock(id INT, stock INT)")

except:
	print("Las tablas ya existen\n")
	cursor.execute("SELECT * FROM productos")
	aux = cursor.fetchall()
	i = aux[-1][0] + 1

while True:
	print ("""
	1 - Ingresar Producto
	2 - Ver Productos
	3 - Cantidad de productos en venta
	4 - Realizar venta
	5 - Modificar stock
	6 - Salir
	""")
	op = input ("Ingrese una Opcion \n")
	if op == "1":
		nombre = input("Ingrese nombre: \n")
		nombre = str(nombre)
		precio = input("Ingrese precio: \n")
		precio = int(precio)
		stock = input("Ingrese Stock: \n")
		stock = int(stock)
		i = int(i)
		cursor.execute("INSERT INTO productos (id,nombre,precio) VALUES (%s,%s,%s)",(i,nombre,precio))
		cursor.execute("INSERT INTO stock (id,stock) VALUES (%s,%s)",(i,stock))
		i = i + 1
		conn.commit()
	if op == "2":
		consulta()
	if op == "3":
		cursor.execute ("SELECT * from productos")
		tabla = cursor.fetchall()
		print("Productos en venta : ", len(tabla))
	if op == "4":
		cursor.execute("SELECT * from productos")
		tabla = cursor.fetchall()
		cursor.execute("SELECT * from stock")
		stock = cursor.fetchall()
		p = 0
		print('ID  Nombre  Precio   Stock')
		for n,name,price in tabla:
			print(n,name,price,stock[p][1])
			p = p + 1
		productoId = input("Elija un producto a vender (Id): \n")
		productoId = int(productoId)
		cursor.execute ("SELECT * FROM productos where id = " + str(productoId))
		consultaPrecio = cursor.fetchall()
		cursor.execute ("SELECT * FROM stock where id = " + str(productoId))
		consultaStock = cursor.fetchall()
		if consultaStock[0][1] == 0 or consultaStock[0][1] < 0:
			print("el producto no posee stock \n")
		else:
			cantVend = input("Indique la cantidad de productos a vender: \n")
			cantVend = int(cantVend)
			montoFinal = consultaPrecio[0][2]
			montoFinal = montoFinal * cantVend
			montoFinal = int(montoFinal)
			cursor.execute("UPDATE stock SET stock = stock -" + str(cantVend) + " where id = "+ str(productoId))
			cursor.execute("INSERT INTO ventas (id,cantidad,monto) VALUES (%s,%s,%s)",(productoId,cantVend,montoFinal))
			conn.commit()
	if op == "5":
		print ("Productos a la venta: \n")
		consulta()
		producto = input("ingrese producto a modificar: \n")
		producto = int(producto)
		stock = input("ingrese nuevo stock \n")
		stock = int(stock)
		cursor.execute("UPDATE stock SET stock =" + str(stock)+ " where id = " + str(producto))
		conn.commit()
	if op == "6":
		break
conn.commit()
conn.close
