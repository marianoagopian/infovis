import pandas as pd
import matplotlib.pyplot as plt

# Cargar el CSV
file_path = './data/tp1_data.csv'
data = pd.read_csv(file_path)

# Asegurarse de que la columna de fechas está en formato datetime
data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')

# Crear un rango completo de fechas desde la primera hasta la última
full_date_range = pd.date_range(start=data['date'].min(), end=data['date'].max())

# Agrupar los datos por fecha y contar el número de canciones, incluyendo los días sin canciones
songs_per_date_total = data.groupby('date').size().reindex(full_date_range, fill_value=0).reset_index(name='total_song_count')
songs_per_date_total.columns = ['date', 'total_song_count']

# Gráfico de líneas con los días vacíos
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
plt.xticks(rotation=45)

# Guardar el gráfico de líneas como archivo PNG
plt.tight_layout()
plt.savefig('./data/canciones_por_fecha.png', format='png', bbox_inches='tight')

# Mostrar el gráfico
plt.show()

# Convertir la duración de las canciones de segundos a minutos
data['duration_min'] = data['duration'] / 60

# Agrupar los datos por género y sumar la duración en minutos por cada género
minutes_per_genre = data.groupby('genre')['duration_min'].sum().reset_index()

# Calcular el total de minutos escuchados
total_minutes = minutes_per_genre['duration_min'].sum()

# Calcular el total de horas y minutos
total_hours = int(total_minutes // 60)
remaining_minutes = int(total_minutes % 60)

# Ordenar los datos por duración en minutos de mayor a menor
minutes_per_genre = minutes_per_genre.sort_values(by='duration_min', ascending=False).reset_index(drop=True)

# Generar una lista de colores únicos utilizando el cmap 'hsv' que tiene una amplia gama de colores
colors = plt.cm.get_cmap('hsv', len(minutes_per_genre))

# Generar el gráfico de torta (pie chart)
plt.figure(figsize=(10,6))

# Crear el gráfico de torta con colores ordenados acorde a los porcentajes
plt.pie(minutes_per_genre['duration_min'], 
        startangle=90, 
        colors=[colors(i) for i in range(len(minutes_per_genre))], 
        wedgeprops=dict(edgecolor='w'))

# Crear las etiquetas de la leyenda que incluyen el porcentaje y el total de minutos
labels = [f"{genre}: {minutes:.1f} min ({minutes/total_minutes:.1%})" 
          for genre, minutes in zip(minutes_per_genre['genre'], minutes_per_genre['duration_min'])]

# Añadir la leyenda ordenada por porcentaje
plt.legend(labels, title="Género", loc="center left", bbox_to_anchor=(1, 0.5))

# Asegurar que el gráfico sea un círculo
plt.axis('equal')

# Título con el total de horas y minutos
plt.title(f'Distribución de minutos escuchados por género (Total: {total_hours}h {remaining_minutes}min)')


# Guardar el gráfico de torta como archivo PNG
plt.tight_layout()
plt.savefig('./data/distribucion_minutos_genero.png', format='png', bbox_inches='tight')

# Mostrar el gráfico
plt.show()
