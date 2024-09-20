import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file to inspect its structure
file_path = './data/tp1_data.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataset to understand its structure
data.head()

import pandas as pd
import matplotlib.pyplot as plt

# Asegurarse de que la columna de fechas está en formato datetime
data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')

# Crear un rango completo de fechas desde la primera hasta la última
full_date_range = pd.date_range(start=data['date'].min(), end=data['date'].max())

# Agrupar los datos por fecha y contar el número de canciones, incluyendo los días sin canciones
songs_per_date_total = data.groupby('date').size().reindex(full_date_range, fill_value=0).reset_index(name='total_song_count')
songs_per_date_total.columns = ['date', 'total_song_count']

# Generar el gráfico de líneas con los días vacíos
plt.figure(figsize=(10,6))
plt.plot(songs_per_date_total['date'], songs_per_date_total['total_song_count'], marker='o', color='skyblue')

# Formatear las etiquetas de las fechas como "Sep 04"
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %d'))

# Mostrar todas las fechas
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator())

# Añadir los valores numéricos sobre cada marcador
for i, value in enumerate(songs_per_date_total['total_song_count']):
    plt.annotate(str(value), (songs_per_date_total['date'][i], songs_per_date_total['total_song_count'][i]), 
                 textcoords="offset points", xytext=(0,5), ha='center')

# Agregar etiquetas y título
plt.xlabel('Fecha')
plt.ylabel('Cantidad de canciones')
plt.title('Cantidad de canciones escuchadas por fecha')

# Rotar las etiquetas de las fechas para que se vean mejor
plt.xticks()

# Mostrar el gráfico
plt.tight_layout()
plt.show()
