"""
    Contains functionality of Pet's
"""

from lxml import etree
from pet_store.rest_request.connector import Connector
from pet_store.pet_func.pet import Pet
from lxml import objectify
from pet_store.pet_func.pet_status import PetStatus
import logging as log


class PetDriver:
    """
        Contains each each action, which we can do with Pet

        Constants:
            __URL: end of the original link
            __HEADERS_SINGLE: single header for simple request
            __HEADERS_UPDATE: headers for update pet by post request
            __HEADERS_DOUBLE: header for creating pet by post request
    """
    __URL = "v2/pet/"
    __HEADERS_SINGLE = {'accept': 'application/xml'}
    __HEADERS_UPDATE = {'accept': 'application/xml', 'Content-Type': 'application/x-www-form-urlencoded'}
    __HEADERS_DOUBLE = {'accept': 'application/xml', 'Content-Type': 'application/xml'}

    def __init__(self, url):
        """
        Create url for requests

        :param url: original host URL
        """
        self.__URL = url + self.__URL
        log.debug("Create new link")

    def create_pet(self, obj):
        """
        Create new pet on the server

        :param obj: "objectify" of pet
        :return Pet: new "objectify" from created pet on the server
        """
        log.debug('Send POST Request with obj as XML')
        new_xml = etree.tostring(obj, pretty_print=True, xml_declaration=True)
        connect = Connector()
        answer = connect.post(self.__URL, new_xml, headers=self.__HEADERS_DOUBLE)

        return Pet(objectify.fromstring(answer.content))

    def update(self, id_, name: str=None, status: PetStatus=None):
        """
        Update existing pet on the server

        :param id_: pet's ID
        :param name: new pet name
        :param status: new status for pet from pet_status enum
        """
        connect = Connector()
        data = None
        if name is not None:
            data = 'name=' + name
        if status is not None and data is None:
            data = 'status=' + status.value
        if status is not None:
            data = data + '&status=' + status.value

        log.debug('Send POST(update) request for pet with: id= ' + str(id_) + ' name= ' + str(name)
                  + ' status= ' + str(status))
        connect.post((self.__URL + str(id_)), data, self.__HEADERS_UPDATE)

    def get_pet(self, id_):
        """
        Get existing pet from Server

        :param id_: pet's ID
        :return Pet: return Pet
        """
        log.debug('Send GET request for pet with: id= %s', id_)
        data_xml = Connector.get(self.__URL+str(id_), self.__HEADERS_SINGLE).content
        return Pet(objectify.fromstring(data_xml))

    def delete_pet(self, id_):
        """
        Delete existing pet from server

        :param id_: pet's ID
        :return: answer of deleting pet
        """
        log.debug('Send DELETE request for pet with: id= %s', id_)
        return Connector.delete(self.__URL+str(id_), self.__HEADERS_SINGLE)

    def get_xml(self, id_):
        """
        Get XML of existing Pet from the server

        :param id_: pet's ID
        :return: Pet's XML
        """
        log.debug('Try to get XML from server for pet with: id= %s', id_)
        return Connector.get(url=(self.__URL + str(id_)), headers=self.__HEADERS_SINGLE).content
