from __future__ import unicode_literals
from django.db import connection, connections
from django.db import models
from enum import Enum
from rest_framework import status
from rest_framework.response import Response


def cursor_to_dict(cursor, many=True):
    """
    Retorna los objetos de una consulta en lista o diccionario

    :param cursor: (cursor) Cursor de la base de datos
    :param many: (boolean) Estableque si se recuperan todos o solo uno de los datos
    :return:
    """
    columns = [column[0] for column in cursor.description]
    if many:
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    else:
        data = cursor.fetchone()
        if data is None:
            data = {}
        return dict(zip(columns, data))


class DataBaseResponseGeneric(object):
    def __init__(self):
        pass


class DBResponse(DataBaseResponseGeneric):
    """
    Representa un mensaje de la base datos
    """
    def __init__(self, data):
        """
        Representa un mensaje de la base de datos
        :param data: Resultado de la funcion que se ejecuto
        """
        super(DBResponse, self).__init__()
        self.message = data['message']
        self.type = data['type']
        self.content = data['result'] if 'result' in data else data['data']
        self.status = status.HTTP_200_OK

    def is_success(self):
        """
        Verifica el mensaje sea del tipo success

        :return: (boolean)
        """
        if self.type in ('S', 's'):
            return True
        return False

    def is_error(self):
        """
        Verifica el mensaje sea del tipo success

        :return: (boolean)
        """
        if self.type in ('E', 'e'):
            return True
        return False

    def is_warning(self):
        """
        Verifica que el mensaje sera de tipo warning

        :return: (boolean)
        """
        if self.type in ('W', 'w'):
            return True
        return False

    def get_message(self):
        """
        Retorna el mensage como un diccionario
        :return:
        """
        if self.is_success():
            msg_type = 'success'
            self.status = status.HTTP_200_OK
        elif self.is_warning():
            msg_type = 'warning'
            self.status = status.HTTP_202_ACCEPTED
        else:
            msg_type = 'error'
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"type": msg_type, "message": self.message, "data": self.content}

    def get_response(self, status_code=None):
        """
        Retorna el mensaje de la base de datos como un Response para enviar directamente
        desde una vista

        :param status_code:
        :return:
        """
        data = self.get_message()
        status_code = self.status if status_code is None else status_code
        data['status'] = status_code
        return Response(data, status_code)


def json_procedure(procedure_name, *proc_params, **kwargs):
    """
    Ejecuta y retorna un procedimiento de retorna un objetivo
    de tipo json como un string

    :param procedure_name: (string) Nombre de la funcion a ejecutarse
    :param proc_parmas: (lista) es la lista de los parametros que recibe
        elos procedimientos almacenados
    :return: (string) El json el forma de string
    """
    smallint = True if 'smallint' in kwargs else False
    if smallint:
        query = (
            """ SELECT * FROM %s(%s); """ %
            (
                procedure_name,
                ', '.join(('\'' + str(x) + '\'') if type(x) == str else str(x) + '::SMALLINT' for x in proc_params)
            )
        )
    else:
        query = (
            """ SELECT * FROM %s(%s); """ %
            (
                procedure_name,
                ', '.join(('\'' + str(x) + '\'') if type(x) == str else str(x) for x in proc_params)
            )
        )
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchone()[0]
    return data


def procedure(procedure_name, *proc_params):
    """
    Ejecuta el procedimiento almacenado y retorna la informacion
    como un diccionario
    """
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM %s (%s);" %
        (
            procedure_name,
            ', '.join(('\'' + str(x) + '\'') if type(x) == str else str(x) for x in proc_params)
        )
    )
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def single_procedure(procedure_name, *proc_params):
    """
    Ejecuta un procedimiento almacenado y retorna la informacion como una lista.
    """
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM %s (%s);" %
        (
            procedure_name,
            ', '.join(('\'' + str(x) + '\'') if type(x) == str else str(x) for x in proc_params)
        )
    )
    results = cursor.fetchall()
    return results


def complex_procedure(fields, procedure_name, *proc_params):
    """
    Ejecuta un procedimiento almacenado especificando los campos a ser devuletos,
    retorna una lista
    """
    cursor = connection.cursor()
    cursor.execute(
        "SELECT %s FROM %s (%s);" %
        (
            ', '.join(field for field in fields),
            procedure_name,
            ', '.join(('\'' + str(x) + '\'') if type(x) == str else str(x) for x in proc_params)
        )
    )
    results = cursor.fetchall()
    return results


def full_complex_procedure(fields, procedure_name, *proc_params):
    """
    Ejecuta un procedimiento almacenado especificando los campos a ser devuletos,
    retorna una diccionario
    """
    cursor = connection.cursor()
    cursor.execute(
        "SELECT %s FROM %s (%s);" %
        (
            ', '.join(field for field in fields),
            procedure_name,
            ', '.join(('\'' + str(x) + '\'') if type(x) == str else str(x) for x in proc_params)
        )
    )
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def wh_procedure(procedure_name, wh, *proc_params):
    """Retorna un procedimiento almacenado con una condicion de where"""
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM %s (%s) WHERE %s LIKE  '%s%s%s';" %
        (
            procedure_name,
            ', '.join(('\'' + str(x) + '\'') if type(x) == str else str(x) for x in proc_params),
            wh[0],
            '%',
            wh[1],
            '%'
        )
    )
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def simple_view(view_name, **kwargs):
    """Llama a una vista o tabla y retorna los datos de la misma
    como un diccionario
    parametros
    :view_name: Nombre de la vista o tabla a la cual se desea realizar la consulta
    :order_by: Los Campos de ordenamiento tupla (CAMPO, TIPO)
    """
    cursor = connection.cursor()
    # Ser verifica que se envio un order by
    if 'order_by' in kwargs:
        view_name += ' ORDER BY %s %s' % kwargs['order_by']
    cursor.execute(
        "SELECT * FROM %s" %
        (
            view_name,
        )
    )
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


class DataBaseGeneric(object):
    """
    Objeto generica para la gestion de procedimiento almacenados y vistas
    """

    def __init__(self, connection_name=None):
        """
        Objeto Generico de para la interacion de la base de datos sin utilizar el ORM
        :param connection_name: (string) Nombre de la cadena de conexion que se utilizara
        """
        if connection_name is None:
            self.connection = connection
        else:
            self.connection = connections[connection_name]


class DataBaseView(DataBaseGeneric):
    def __init__(self, view_name=None, connection_name=None):
        """
        Se encarga de llmar a una vista dentro de la base de datos
        :param view_name: (string) Nombre de la vista que se ha de ejecutar
        :param connection_name: (string) Nombre de la cadena de connecion que se utilizara
        """
        super(DataBaseView, self).__init__(connection_name=connection_name)
        self._view_name = view_name
        self.query = ''
        self._values = '*'
        self._str_where = ''
        self._order = []

    def view_name(self, view_name: str):
        """
        Establece el nombre de la vista
        :param view_name: (string) Nombre de la vista
        :return: (DataBaseView)
        """
        self._view_name = view_name
        return self

    def filter(self, **kwargs):
        pass

    def str_where(self, str_where: str):
        """
        Estable la condicion que se utlizara al momento de utilizar la vista
        :param str_where: (string) Condicion hecha en string
        :return: (DatBaseView)
        """
        self._str_where = str_where
        return self

    def add_order(self, colname: str, order: str):
        if order not in ('DESC', 'ASC'):
            raise ValueError('Parameter order must be DESC or ASC')
        self._order.append((colname, order))
        return self

    def values(self, *args):
        """
        Establece los valores que retornara la vista
        :param args: (list)
        :return: (DatBaseView)
        """
        self._values = [x for x in args]
        return self

    def get_data(self):
        """
        Retorna los datos que se solicitaron de la vista
        :return: (dict) Valores de la vista
        """
        list_values = ''
        if self._values == '*':
            list_values = self._values
        else:
            list_values = ','.join("''%s" % val for val in self._values)

        if self._str_where == '':
            self.query = """
                SELECT %s FROM %s
            """ % (
                list_values,
                self._view_name
            )
        else:
            self.query = """
               SELECT %s FROM %s WHERE %s
                       """ % (
                list_values,
                self._view_name,
                self._str_where
            )

        if self._order:
            str_order = ', '.join('{} {}'.format(*x) for x in self._order)

            if str_order:
                self.query += ' ORDER BY {}'.format(str_order)

        cursor = self.connection.cursor()
        cursor.execute(self.query)
        results = []
        columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        return results


class PgParameter(Enum):
    PG_CHAR = 1
    PG_DATE = 2
    PG_DATETIME = 3
    PG_INT = 4
    PG_SMALLINT = 5
    PG_JSON = 6
    PG_TEXT = 7
    PG_BOOL = 8
    PG_INET = 9
    PG_ARRAY = 10
    PG_STR_ARRAY = 11
    PG_INT_ARRAY = 12


class DataBaseProcedure(DataBaseGeneric):
    """
    Se Encarga de llamar a un procedimiento alamcenado
    """

    def __init__(self, procedure_name: str, database=None):
        """
        Se encarga de gestionar una llamada a un procedimiento almacenado
        de postgres

        :param procedure_name: (string) Nombre de la funcion que se desea llamar
        :param database: (string) Nombre la base de datos que se ha de utilizar
        """
        if database is None:
            super(DataBaseProcedure, self).__init__()
        else:
            super(DataBaseProcedure, self).__init__(database)

        self._procedure_name = procedure_name
        self._parameters = []

    def add_parameter(self, value, tipo):
        """
        Agregar un parametros es importante hacerlo de acuerdo al orden
        que se estrablecio dentro de la funcion

        :param value: (any) Valor del parametro
        :param tipo: (int) Tipo de parametro
        :return: (DatoBaseProcedure)
        """
        if value is None:
            self._parameters.append('NULL')
            return self
        if tipo == PgParameter.PG_CHAR:
            self._parameters.append('\'%s\'::CHARACTER  VARYING' % value)
        if tipo == PgParameter.PG_TEXT:
            self._parameters.append('\'' + value + '\'::TEXT')
        elif tipo == PgParameter.PG_DATE:
            self._parameters.append('\'%s\'::DATE' % str(value))
        elif tipo == PgParameter.PG_DATETIME:
            self._parameters.append('\'%s\'::TIMESTAMP' % str(value))
        elif tipo == PgParameter.PG_INT:
            self._parameters.append('%s::INT' % str(value))
        elif tipo == PgParameter.PG_SMALLINT:
            self._parameters.append('%s::SMALLINT' % str(value))
        elif tipo == PgParameter.PG_JSON:
            import json
            self._parameters.append('\'%s\'::JSON' % str(json.dumps(value)))
        elif tipo == PgParameter.PG_INET:
            self._parameters.append('\'%s\'::INET' % str(value))
        elif tipo == PgParameter.PG_ARRAY:
            if not isinstance(value, list):
                raise TypeError('Para PG_ARRAY solo se admite tipo list no %s' % type(value))
            self._parameters.append('ARRAY%s' % value)
        elif tipo == PgParameter.PG_STR_ARRAY:
            if not isinstance(value, list):
                raise TypeError('Para PG_ARRAY solo se admite tipo list no %s' % type(value))
            self._parameters.append('ARRAY%s' % [str(val) for val in value])
        elif tipo == PgParameter.PG_INT_ARRAY:
            if not isinstance(value, list):
                raise TypeError('Para PG_ARRAY solo se admite tipo list no %s' % type(value))
            self._parameters.append('ARRAY%s::INT[]' % [str(val) for val in value])
        elif tipo == PgParameter.PG_BOOL:
            if isinstance(value, bool):
                if value:
                    self._parameters.append('TRUE')
                else:
                    self._parameters.append('FALSE')
            else:
                raise TypeError('Para PG_BOOL solo se admite tipos booleanos no %s' % type(value))
        return self

    def get_data(self, many=False):
        """
        Retorna los datos que se obtuvieron

        :param many:
        :return:
        """
        query = """
            SELECT * FROM %s (%s)
        """ % (
            self._procedure_name,
            ', '.join(x for x in self._parameters)
        )
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        if many:
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
        else:
            data = cursor.fetchone()
            if data is None:
                data = {}
            return dict(zip(columns, data))

        return results

    @property
    def data(self, many=False):
        """
            Retorna los datos que se obtuvieron

            :param many:
            :return:
            """
        query = """
                SELECT * FROM %s (%s)
            """ % (
            self._procedure_name,
            ', '.join(x for x in self._parameters)
        )
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        if many:
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
        else:
            data = cursor.fetchone()
            if data is None:
                data = {}
            result = (dict(zip(columns, data)))
            if self._procedure_name in result:
                return result[self._procedure_name]
            else:
                return result
        return results[self._procedure_name]

    def get_message(self):
        """
        Retorna el mensaje asociado en caso que el procedimiento alamcneado retorne
        un tipo result_msg
        :return: (MessageResponse)
        """
        query = """
           SELECT * FROM %s (%s)
               """ % (
            self._procedure_name,
            ', '.join(x for x in self._parameters)
        )
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]

        data = cursor.fetchone()
        if data is None:
            data = {}
        message = DBResponse(dict(zip(columns, data)))
        return message


class UpperCharField(models.CharField):
    """Es un Field que se encarga de guardar la informacion en Mayusculas"""
    def __init__(self, *args, **kwargs):
        self.is_uppercase = kwargs.pop('uppercase', False)
        super(UpperCharField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper() if self.is_uppercase else value
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperCharField, self).pre_save(model_instance, add)


class UpperTextField(models.TextField):
    """Es un Field que se encarga de guardar la informacion en Mayusculas"""
    def __init__(self, *args, **kwargs):
        self.is_uppercase = kwargs.pop('uppercase', False)
        super(UpperTextField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper() if self.is_uppercase else value
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperTextField, self).pre_save(model_instance, add)
