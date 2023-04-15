
class ETLInput:

    def __init__(self, data):
        self.data = data


    def elt_format_input(data):
        # Transform the data to the correct format
        data["input"] = "input"
        data = data.dropna()
        data = data.pivot(index='input',columns='campo', values='text').reset_index()
        data = data.drop(columns=['input'])

        return data

    def etl_input_checkbox(data):
        
        # Si la columna 'victimas si' tiene x o X en la celda, se cambia por 1
        data['A aseguradora danos_propios'] = data['A  aseguradora danos_propios_si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
        data = data.drop(columns=['A  aseguradora danos_propios_si', 'A  aseguradora danos_propios_no'])

        # B aseguradora danos_propios si	B aseguradora danos_propios no
        data['B aseguradora danos_propios'] = data['B aseguradora danos_propios si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
        data = data.drop(columns=['B aseguradora danos_propios si', 'B aseguradora danos_propios no'])

        # danos_materiales objetos no	danos_materiales objetos si	
        data['danos_materiales objetos'] = data['danos_materiales objetos si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
        data = data.drop(columns=['danos_materiales objetos si', 'danos_materiales objetos no'])

        # danos_materiales vehiculos si	danos_materiales vehículos no
        data['danos_materiales vehiculos'] = data['danos_materiales vehiculos si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
        data = data.drop(columns=['danos_materiales vehiculos si', 'danos_materiales vehículos no'])

        # victimas no	victimas si
        data['victimas'] = data['victimas si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
        data = data.drop(columns=['victimas si', 'victimas no'])

        # A 1	A 10	A 11	A 12	A 13	A 14	A 15	A 16	A 17	A 2	A 3	A 4	A 5	A 6	A 7	A 8	A 9
        checkboc_columns = ["Estaba estacionado/parado", "Salia de un estacionamiento/ abriendo puerta", 
        "Iba a estacionar", "Salia de un aparcamiento, de un lugar privado, de un camino de tierra", 
        "Entrada a un aparcamiento, a un lugar privado, a un camino de tierra", 
        "Entrada a una plaza de sentido giratorio", "Circulaba por una plaza de sentido giratorio", 
        "Colisiono en la parte de atras al otro vehiculo que circulaba en el mismo sentido y en el mismo carril", 
        "Circulaba en el mismo sentido y en carril diferente", "Cambiaba de carril", "Adelantada", 
        "Giraba a la derecha", "Giraba a la izquierda", "Daba marcha atras", 
        "Invadia la parte reservada a la circulacion en sentido inverso", 
        "Venia de la derecha (en un cruce)", "No respeto la senal de preferencia o semaforo en rojo"]

        for i in range(17):
            data[f'A {checkboc_columns[i]}'] = data[f'A {i+1}'].apply(lambda x: True if x == 'x' or x == 'X' else False)
            data[f'B {checkboc_columns[i]}'] = data[f'B {i+1}'].apply(lambda x: True if x == 'x' or x == 'X' else False)

            data = data.drop(columns=[f'A {i+1}', f'B {i+1}'])

        # Give me a json format of the data
    
        return data.to_json(orient='records')