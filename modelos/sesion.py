# -*- coding: utf-8 -*-

from bd import BaseDatos


bd = BaseDatos()


class Sesion(object):
    '''
    Controla el inicio de sesion y manda los datos para que Flask los guarde en cache.
    '''
    def __init__(self):
        self.base = bd
        self._id = None

    def inicio_sesion(self, usuario, contra):
        base = self.base
        base.conectar()
        res = None
        usuario = base.buscar([('usuario', '=', usuario), ('contra', '=', contra)])
        if usuario:
            res = True
            self._id = usuario[0]
        else:
            res = False
        return res

    def get_nombre(self):
        base = self.base
        base.conectar()
        nombre = base.encontrar_por_id([('id', '=', self._id)])
        return nombre

    @property
    def nombre(self):
        return self.get_nombre()
