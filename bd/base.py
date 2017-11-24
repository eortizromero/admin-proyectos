# -*- coding: utf-8 -*-

import psycopg2


class BaseDatos(object):
	def __init__(self, dominio=None, basedatos=None, usuario=None, contra=None, puerto=None):
		self.dominio = dominio or '192.168.2.53'
		self.basedatos = basedatos or 'postgres'
		self.usuario = usuario or 'manager'
		self.contra = contra or 'admin00'
		self.puerto = puerto or 5432
		self.conexion = {}
		self.cursor = None


	def conectar(self):
		try:
			conex = psycopg2.connect(host=self.dominio, database=self.basedatos, user=self.usuario, password=self.contra)
			cur = conex.cursor()
			self.cursor = cur
		except:
			raise Exception("No se pudo conectar a postgres.")

	def get_cursor(self):
		return self.cursor

	def get_version(self):
		cur = self.get_cursor()
		consulta = cur.execute('SELECT version()')
		db_ver = cur.fetchone()
		return db_ver

