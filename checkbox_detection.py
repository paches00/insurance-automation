import os
import cv2
import csv
import numpy as np


# Read image into array
# image_array = cv2.imread("c.jpg")

def checkbox_detection(image_array):
    image_array = cv2.imread(image_array)

    # Convert image to grayscale
    gray_scale_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    # Image thresholding
    _, img_bin = cv2.threshold(gray_scale_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = cv2.adaptiveThreshold(gray_scale_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 15)

    img_bin = 255 - img_bin

    # Set min width to detect horizontal lines
    line_min_width = 1

    # Kernel to detect horizontal lines
    kernal_h = np.ones((1, line_min_width), np.uint8)

    # Kernel to detect vertical lines
    kernal_v = np.ones((line_min_width, 1), np.uint8)

    # Apply horizontal kernel on the image
    img_bin_horizontal = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)

    # Apply vertical kernel on the image
    img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)

    # Combine the images
    img_bin_final = img_bin_horizontal | img_bin_v

    # cv2.imshow("Greyscale Detection", img_bin_final)
    # cv2.waitKey(0)
    _, labels, stats, _ = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)
    dilation_kernel = np.ones((2, 2), np.uint8)

    names = ["Victima(s) incluso leve(s) — No",
             "Victima(s) incluso leve(s) — Si",
             "Daños materiales: Vehículos distintos de A y B — No",
             "Daños materiales: Vehículos distintos de A y B — Si",
             "Daños materiales:objetos distintos al vehículo — No",
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

    data = []
    counter = 0
    for x, y, w, h, area in stats[2:]:
        aspect_ratio = w / h
        size = w * h

        # Apply filters
        if aspect_ratio > 0.9 and aspect_ratio < 1.3 and size > 80 and size < 500:
            # Check if the checkbox is ticked
            checkbox_roi = img_bin[y:y + h, x:x + w]
            checkbox_roi_dilated = cv2.dilate(checkbox_roi, dilation_kernel, iterations=1)
            black_pixels_count = np.sum(checkbox_roi_dilated == 0)
            total_pixels = checkbox_roi_dilated.shape[0] * checkbox_roi_dilated.shape[1]
            black_pixels_ratio = black_pixels_count / total_pixels

            # Set a threshold for black pixels ratio to determine if the checkbox is ticked
            if black_pixels_ratio > 0.94:
                ticked = ""
                # print(f"Checkbox at ({x}, {y}) is not ticked")
                cv2.rectangle(image_array, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw a green rectangle
            else:
                ticked = "X"
                # print(f"Checkbox at ({x}, {y}) is ticked")
                cv2.rectangle(image_array, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a red rectangle
            # Create a list of lists to represent the rows of the CSV file
            try:
                # print([names[counter], x, y, w, h, ticked])
                data.append([names[counter], x, y, w, h, ticked])
            except IndexError:
                pass

            counter += 1

    # Show the resulting image
    #cv2.imshow("Checkbox Detection", image_array)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cv2.imwrite('images/checkbox_detected.jpg', image_array)

    with open("data/checkbox_detected.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row (optional)
        writer.writerow(['campo', 'x', 'y', 'w', 'h', "text"])
        # Write each row of data to the file
        for row in data:
            writer.writerow(row)