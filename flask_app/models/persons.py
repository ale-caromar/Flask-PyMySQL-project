
# Definir la clase Person
class Person:
    #Inicializa una instancia de la clase Person con los datos proporcionados.
    def __init__(self, data): # data es un diccionario que contiene la información de la persona. 
        #Self permite acceder a los atributos y métodos de la instancia actual.
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.docu_type = data['docu_type']
        self.docu_number = data['docu_number']
        self.email = data['email']
        self.phone = data['phone']
        self.address = data['address']


