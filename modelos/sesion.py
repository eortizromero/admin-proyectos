# -*- coding: utf-8 -*-

from bd import BaseDatos


def inicio_sesion(usuario, contra):
	base = BaseDatos()
	base.conectar()
	usuario = base.buscar([('usuario', '=', usuario), ('contra', '=', contra)])
	# base.buscar([('usuario', '=', usuario)])
	return usuario