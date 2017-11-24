# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class BaseDatos(object):
	def __init__(self, dominio=None, basedatos=None, usuario=None, contra=None, puerto=None):
		self.dominio = dominio or '192.168.2.53'
		self.basedatos = basedatos or 'postgres'
		self.usuario = usuario or 'manager'
		self.contra = contra or 'admin00'
		self.puerto = puerto or 5432
		self.conexion = None
		self.cursor = None


	def conectar(self):
		try:
			self.conexion = psycopg2.connect(host=self.dominio, database=self.basedatos, user=self.usuario, password=self.contra)
			cur = self.conexion.cursor()
			self.cursor = cur
		except:
			raise Exception("No se pudo conectar a postgres.")

	def get_cursor(self):
		return self.cursor


	def ejecutar(self, consulta):
		self.conexion.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cr = self.get_cursor()
		if not isinstance(consulta, (str, tuple, dict)):
			raise ValueError("La consulta debe ser una cadena, tupla o diccionario.")
		cr.execute(consulta)

	def get_version(self):
		cur = self.get_cursor()
		consulta = cur.execute('SELECT version()')
		db_ver = cur.fetchone()
		return db_ver

	def crear_bd(self, nombre):
		self.ejecutar('DROP DATABASE IF EXISTS %s' % nombre)
		self.ejecutar('CREATE DATABASE %s' % nombre)

	def buscar(self, args):
		print len(args)
		print args[0]
