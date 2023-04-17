def etl_format_input(data):
    # Transform the data to the correct format
    data["input"] = "input"
    # data = data.dropna()
    data = data.pivot(index='input',columns='campo', values='text').reset_index()
    data = data.drop(columns=['input'])
    
    return data

def etl_merge(hand, checkbox):
    return hand.merge(checkbox, left_index=True, right_index=True)

def etl_input_checkbox(data):
    new_names  = ["Victima(s) incluso leve(s) — No",
                    "Victima(s) incluso leve(s) — Si",
                    "Daños materiales: Vehículos distintos de A y B — No",
                    "Daños materiales: Vehículos distintos de A y B — Si",
                    "Daños materiales: objetos distintos al vehículo — No",
                    "Daños materiales: objetos distintos al vehículo — Si",
                    "A Estaba estacionado/parado",
                    "B Estaba estacionado/parado",
                    "A Salía de un estacionamiento abriendo puerta",
                    "B Salía de un estacionamiento abriendo puerta",
                    "A Iba a estacionar",
                    "B Iba a estacionar",
                    "A Salia de un aparcamiento, de un Vehículo lugar privado, de un camino de tierra",
                    "B Salia de un aparcamiento, de un Vehículo lugar privado, de un camino de tierra",
                    "A Entrada a un aparcamiento, a un lugar privado, a un camino de tierra",
                    "B Entrada a un aparcamiento, a un lugar privado, a un camino de tierra",
                    "A Entrada a una plaza de sentido giratorio",
                    "B Entrada a una plaza de sentido giratorio",
                    "A Circulaba por una plaza de sentido giratono",
                    "B Circulaba por una plaza de sentido giratono",
                    "A Colisiono en la parte de atrás al otro vehiculo que circulaba en el mismo sentido y en el mismo carril",
                    "B Colisiono en la parte de atrás al otro vehiculo que circulaba en el mismo sentido y en el mismo carril",
                    "A Circulaba en el mismo sentido y en carril diferente",
                    "B Circulaba en el mismo sentido y en carril diferente",
                    "A Cambiaba de carril",
                    "B Cambiaba de carril",
                    "A Adelantaba",
                    "B Adelantaba",
                    "A Giraba a la derecha",
                    "B Giraba a la derecha",
                    "A Giraba a la izquierda",
                    "B Giraba a la izquierda",
                    "A Daba marcha atrás",
                    "B Daba marcha atrás",
                    "A Invadía la parte reservada a la circulación en sentido inverso",
                    "B Invadía la parte reservada a la circulación en sentido inverso",
                    "Vehiculo A — ¿Los daños propios del vehículo están asegurados? — No",
                    "Vehiculo A — ¿Los daños propios del vehículo están asegurados? — Si",
                    "Vehiculo B — ¿Los daños propios del vehículo están asegurados? — No",
                    "Vehiculo B — ¿Los daños propios del vehículo están asegurados? — Si",
                    "A Venía de la derecha (en un cruce)",
                    "B Venía de la derecha (en un cruce)",
                    "A No respeto la señal de preferencia o sematoro en rojo",
                    "B No respeto la señal de preferencia o sematoro en rojo"
                    ]
    data.columns = new_names
   
    # Si la columna 'victimas si' tiene x o X en la celda, se cambia por 1
    data['Vehiculo A — ¿Los daños propios del vehículo están asegurados?'] = data['Vehiculo A — ¿Los daños propios del vehículo están asegurados? — Si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Vehiculo A — ¿Los daños propios del vehículo están asegurados? — Si', 'Vehiculo A — ¿Los daños propios del vehículo están asegurados? — No'])

    # B aseguradora danos_propios si	B aseguradora danos_propios no
    data['Vehiculo B — ¿Los daños propios del vehículo están asegurados?'] = data['Vehiculo B — ¿Los daños propios del vehículo están asegurados? — Si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Vehiculo B — ¿Los daños propios del vehículo están asegurados? — Si', 'Vehiculo B — ¿Los daños propios del vehículo están asegurados? — No'])

    # danos_materiales objetos no	danos_materiales objetos si	
    data['Daños materiales: Vehículos distintos de A y B'] = data['Daños materiales: Vehículos distintos de A y B — Si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Daños materiales: Vehículos distintos de A y B — Si', 'Daños materiales: Vehículos distintos de A y B — No'])

    # danos_materiales vehiculos si	danos_materiales vehículos no
    data['Daños materiales: objetos distintos al vehículo'] = data['Daños materiales: objetos distintos al vehículo — Si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Daños materiales: objetos distintos al vehículo — Si', 'Daños materiales: objetos distintos al vehículo — No'])

    # victimas no	victimas si
    data['Victima(s) incluso leve(s)'] = data['Victima(s) incluso leve(s) — Si'].apply(lambda x: True if x == 'x' or x == 'X' else False)
    data = data.drop(columns=['Victima(s) incluso leve(s) — Si', 'Victima(s) incluso leve(s) — No'])

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

    return data

def etl_original_data_format(hand_written, check):
    hand_written = hand_written.rename(columns={'classes': 'campo'})
    hand_written = hand_written.rename(columns={'texto': 'text'})
    
    # append checkbox data
    final = hand_written.append(check)
    # final = final.drop(columns=['Unnamed: 0'])
    final.to_csv('data/final.csv')
    return final

def etl_main(hand_written, checkbox):

    hand_written = hand_written.rename(columns={'classes': 'campo'})
    hand_written = hand_written.rename(columns={'texto': 'text'})
    hand_written = etl_format_input(hand_written)

    checkbox = etl_format_input(checkbox)
    checkbox = etl_input_checkbox(checkbox)
    input_file = etl_merge(hand_written, checkbox)

    return input_file.to_json(orient='records')