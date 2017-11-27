# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Sesion(object):
	def __init__(self):
		pass


class ConexionPostgres(object):
	def __init__(self, dominio=None, basedatos=None, usuario=None, contra=None, puerto=None):
		self.dominio = dominio or 'localhost'
		self.basedatos = basedatos or 'postgres'
		self.usuario = usuario or 'manager'
		self.contra = contra or 'admin00'
		self.puerto = puerto or 5432
		self.conexion = None
		self.cursor = None
		self.argumentos = []

	def conectar(self):
		try:
			self.conexion = psycopg2.connect(host=self.dominio, database=self.basedatos, user=self.usuario, password=self.contra)
			cur = self.conexion.cursor()
			self.cursor = cur
		except:
			raise Exception("No se pudo conectar a postgres.")
		return self.conexion

	def get_cursor(self):
		return self.cursor


conex_postgres = ConexionPostgres()


class BaseDatos(object):
	def __init__(self):
		self.conexion_postgres = conex_postgres

	# def ejecutar(self, consulta):
	# 	self.conexion.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	# 	cr = self.conexion_postgres.get_cursor()
	# 	if not isinstance(consulta, (str, tuple, dict)):
	# 		raise ValueError("La consulta debe ser una cadena, tupla o diccionario.")
	# 	cr.execute(consulta)

	def conectar(self):
		return self.conexion_postgres.conectar()

	def get_version(self):
		cur = self.conexion_postgres.get_cursor()
		consulta = cur.execute('SELECT version()')
		db_ver = cur.fetchone()
		return db_ver

	# def crear_bd(self, nombre):
	# 	self.ejecutar('DROP DATABASE IF EXISTS %s' % nombre)
	# 	self.ejecutar('CREATE DATABASE %s' % nombre)


	def get_campos(self, opcion):
		campo = opcion
		return campo

	def get_operadores(self, opcion):
		operador = opcion
		return operador

	def get_valores(self, opcion):
		valor = opcion 
		return valor

	def buscar(self, opciones):
		return self._buscar(opciones)

	def _buscar(self, opciones=None):
		opciones = opciones if opciones is not None else []
		cr = self.conexion_postgres.get_cursor()
		args = []
		consulta = None
		res = []
		for opcion in opciones:
			if not isinstance(opcion, (tuple, dict)):
				raise TypeError("La consulta debe ser una tupla o diccionario.")
			if len(opciones) == 1 and opcion:
				consulta = "SELECT %s FROM tbl_users WHERE %s%s'%s'" % (opcion[0], opcion[0], opcion[1], opcion[2])
				cr.execute(consulta)
				filas = cr.fetchall()
				if filas:
					for fila in filas:
						res.append((fila[0]))
				else:
					print "No hay un registro con el %s de %s" %(opcion[0], opcion[2])
			elif len(opciones) >= 2:
				campos = self.get_campos(opcion[0])
				operadores = self.get_operadores(opcion[1])
				valores = self.get_valores(opcion[2])
				args.append((campos, operadores, valores))
				consulta = "SELECT * FROM usuarios WHERE " + " AND ".join(("%s %s %s" % (campo, operador, valor) for campo, operador, valor in args))
			else:
				consulta = "SELECT * FROM tbl_users"
				# cr.execute(consulta)
				# filas = cr.fetchall()
				# for fila in filas:
				# 	print fila
		if len(opciones) >= 2:
			print consulta
		elif len(opciones) and opcion:
			if isinstance(res, (tuple, list)):
				res = "".join(res)
			print consulta
		else:
			print consulta
		return res



