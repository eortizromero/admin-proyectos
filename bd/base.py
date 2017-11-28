# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Sesion(object):
	"""
		Adminitra la sesión actual, y la guarda en caché
	"""
	def __init__(self):
		pass


class ConexionPostgres(object):
	def __init__(self, dominio=None, basedatos=None, usuario=None, contra=None, puerto=None):
		self.dominio = dominio or 'localhost'
		self.basedatos = basedatos or 'manager'
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
		'''
		:params opciones: argumentos de consulta.

		Ejemplo:
			self.buscar([('nombre', '=', 'Edgar')])
		: returns

		'''
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
						res.append((fila))
						print "Res una opcion: ", str(res)
				else:
					print "No hay un registro con el %s de %s" %(opcion[0], opcion[2])
			elif len(opciones) >= 2:
				campos = self.get_campos(opcion[0])
				operadores = self.get_operadores(opcion[1])
				valores = self.get_valores(opcion[2])
				args.append((campos, operadores, valores))
				consulta = "SELECT * FROM tbl_users WHERE " + " AND ".join(("%s%s'%s'" % (campo, operador, valor) for campo, operador, valor in args))
			else:
				consulta = "SELECT * FROM tbl_users"
				# cr.execute(consulta)
				# filas = cr.fetchall()
				# for fila in filas:
				# 	print fila
		if len(opciones) >= 2:
			if isinstance(res, (tuple, list)):
				cr.execute(consulta)
				r = cr.fetchall()

				def _uniquify_lista(seq):
					v = set()
					return [x for x in seq if x not in v and not v.add(x)]
				_u_list = _uniquify_lista([x[0] for x in r])
				print " Uniquify Lista", _u_list
				return _u_list
		elif len(opciones) and opcion:
			if isinstance(res, (tuple, list)):
				# res = "".join(res)
				pass
			print consulta
		else:
			print consulta
		return res

	def encontrar_por_id(self, valores):
		return self._encontrar_por_id(valores)

	def _encontrar_por_id(self, valores=None):
		valores = valores if valores is not None else []
		consulta = None
		res = []
		cr = self.conexion_postgres.get_cursor()
		for valor in valores:
			if len(valores) and valor:
				consulta = "SELECT * FROM tbl_users WHERE %s%s%s" %(valor[0], valor[1], valor[2])
				cr.execute(consulta)
				filas = cr.fetchall()
				if filas:
					for fila in filas:
						res.append((fila[3])) # FIXME: get name by form field because data can be change
		return "".join(res)
		