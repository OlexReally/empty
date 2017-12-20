from api_functional.rest_request.connector import Connector
from lxml import objectify
from lxml import etree


class XML_Tool:
    __URL = "http://petstore.swagger.io/v2/pet/"

    def get_xml_from_file(self, file='D:/PetStore/api_functional/tool/pet.xml'):
        with open(file, 'r') as f:
            return f.read()

    def get_xml_from_webapi(self, id):
        return Connector.get(url=(self.__URL + str(id)), headers={'accept': 'application/xml'}).content

    def create_objectify(self, dataxml):
        return objectify.fromstring(dataxml)

    def create_tree(self, dataxml):
        return etree.XML(dataxml)
