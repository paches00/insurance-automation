def elt_format_input(data):
    # Transform the data to the correct format
    data["input"] = "input"
    data = data.dropna()
    data = data.pivot(index='input',columns='campo', values='text').reset_index()
    data = data.drop(columns=['input'])

    return data

def etl_merge(handwritten_data, checkbox_data):
    # add checkbox data to handwritten data, merge on index
    data = handwritten_data.merge(checkbox_data, left_index=True, right_index=True)

    return data
    

def etl_input_checkbox(data):
    
    # Si la columna 'victimas si' tiene x o X en la celda, se cambia por 1
    data['Vehiculo A — ¿Los daños propios del vehículo están asegurados?'] = data['Vehiculo A — ¿Los daños propios del vehículo están asegurados? — Si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Vehiculo A — ¿Los daños propios del vehículo están asegurados? — Si', 'Vehiculo A — ¿Los daños propios del vehículo están asegurados? — No'])

    # B aseguradora danos_propios si	B aseguradora danos_propios no
    data['Vehiculo B — ¿Los daños propios del vehículo están asegurados?'] = data['Vehiculo B — ¿Los daños propios del vehículo están asegurados? — Si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Vehiculo B — ¿Los daños propios del vehículo están asegurados? — Si', 'Vehiculo B — ¿Los daños propios del vehículo están asegurados? — No'])

    # danos_materiales objetos no	danos_materiales objetos si	
    data['Daños materiales: Vehículos distintos de A y B'] = data['Daños materiales: Vehículos distintos de A y B — si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Daños materiales: Vehículos distintos de A y B — si', 'Daños materiales: Vehículos distintos de A y B — No'])

    # danos_materiales vehiculos si	danos_materiales vehículos no
    data['Daños materiales: objetos distintos al vehículo'] = data['Daños materiales: objetos distintos al vehículo — Si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Daños materiales: objetos distintos al vehículo — Si', 'Daños materiales:objetos distintos al vehículo — No'])

    # victimas no	victimas si
    data['Victima(s) incluso leve(s)'] = data['Victima(s) incluso leve(s) — si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Victima(s) incluso leve(s) — si', 'Victima(s) incluso leve(s) — no'])

    # A 1	A 10	A 11	A 12	A 13	A 14	A 15	A 16	A 17	A 2	A 3	A 4	A 5	A 6	A 7	A 8	A 9
    checkboc_columns = ["Estaba estacionado/parado",
                        "Salía de un estacionamiento abriendo puerta",
                        "Iba a estacionar",
                        "Salia de un aparcamiento, de un Vehículo lugar privado, de un camino de tierra",
                        "Entrada a un aparcamiento, a un lugar privado, a un camino de tierra",
                        "Entrada a una plaza de sentido giratorio",
                        "Circulaba por una plaza de sentido giratono",
                        "Colisiono en la parte de atrás al otro vehiculo que circulaba en el mismo sentido y en el mismo carril",
                        "Circulaba en el mismo sentido y en carril diferente",
                        "Cambiaba de carril",
                        "Adelantaba",
                        "Giraba a la derecha",
                        "Giraba a la izquierda",
                        "Daba marcha atrás",
                        "Invadía la parte reservada a la circulación en sentido inverso",
                        "Venía de la derecha (en un cruce)",        
                        "No respeto la señal de preferencia o sematoro en rojo"]


    for i in range(17):
        data[f'A {checkboc_columns[i]}'] = data[f'A {checkboc_columns[i]}'].apply(lambda x: True if x == 'x' or x == 'X' else False)
        data[f'B {checkboc_columns[i]}'] = data[f'B {checkboc_columns[i]}'].apply(lambda x: True if x == 'x' or x == 'X' else False)

        # data = data.drop(columns=[f'A {i+1}', f'B {i+1}'])

    # Count trues for A and B
    data["A indicar el numero de casillas marcadas"] = data[[f'A {checkboc_columns[i]}' for i in range(17)]].sum(axis=1)
    data["B indicar el numero de casillas marcadas"] = data[[f'B {checkboc_columns[i]}' for i in range(17)]].sum(axis=1)

    # Give me a json format of the data
    data = data.to_json(orient='split')

    return data
