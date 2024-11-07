import os
import pandas as pd
from PIL import Image
import base64
from io import BytesIO

# Ruta de la carpeta que contiene los archivos CSV
csv_folder_path = './Archivos CSV'
# Ruta de la carpeta donde se guardarán las imágenes PNG
output_folder_path = './Imagenes'

# Crear la carpeta de salida si no existe
os.makedirs(output_folder_path, exist_ok=True)

# Función para decodificar imágenes
def decode_image(encoded_str):
    # Decodificar la cadena base64
    image_data = base64.b64decode(encoded_str)
    return Image.open(BytesIO(image_data))

# Lista para almacenar datos de imágenes que fallaron
failed_images = []

# Procesar cada archivo CSV en la carpeta
for filename in os.listdir(csv_folder_path):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(csv_folder_path, filename)
        
        # Leer el archivo CSV
        df = pd.read_csv(csv_file_path)
        
        # Procesar cada fila del DataFrame
        for index, row in df.iterrows():
            # Obtener el código de la imagen, el nombre y ref
            id_externo = row [0]
            image_name = row[1]  # Columna 2
            ref_inter = row[2]  # Columna 3
            image_code = row[3]  # Columna 4

            # Decodificar la imagen
            try:
                print(f'Procesando imagen: {ref_inter}{image_name}')
                image = decode_image(image_code)
                # Guardar la imagen como PNG en la carpeta de salida
                image.save(os.path.join(output_folder_path, f'{ref_inter}{image_name}.png'))
                print(f'Imagen guardada: {ref_inter}{image_name}.png')
            except Exception as e:
                print(f'Error al procesar la imagen {ref_inter}{image_name}: {e}')
                # Agregar a la lista de fallos
                failed_images.append({
                    'id_externo' : id_externo,
                    'image_name': image_name,
                    'ref_inter': ref_inter,
                    'image_code': image_code,
                    'error': str(e)
                })

# Guardar los errores en un archivo CSV
if failed_images:
    failed_df = pd.DataFrame(failed_images)
    failed_csv_path = os.path.join(csv_folder_path, 'imag_no_descomprimida.csv')
    failed_df.to_csv(failed_csv_path, index=False)
    print(f'Datos de imágenes fallidas guardados en: {failed_csv_path}')

