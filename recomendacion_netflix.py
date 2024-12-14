from customtkinter import *
import pandas as pd

# Creamos la ventana principal del programa
raiz = CTk()
raiz.title("Sistema de Recomendación de Netflix")
raiz.geometry("800x600")
set_appearance_mode("dark")

# Cargamos todos los datos que contiene el csv de netflix
df = pd.read_csv('netflixData.csv')

entrada_usuario = StringVar()

# Creamos una funcion para que el programa nos facilite recomendaciones 
def recomendaciones_pelicula():
    usuario_texto = entrada_usuario.get().lower()

    # Borramos los resultados anteriores
    resultados.delete("1.0", "end")

    # Buscamos la pelicula que el usuario ha introducido 
    pelicula_usuario = df[df['Title'].str.lower() == usuario_texto]

    if pelicula_usuario.empty:
        resultados.insert("insert", "La película ingresada no se encuentra en la base de datos. Inténtalo de nuevo.\n")
        return

    # Aquí obtenemos el director,actor y genero de la pelicula introducida por el usuario
    director_pelicula = pelicula_usuario['Director'].values[0]
    actores_pelicula = pelicula_usuario['Cast'].values[0]
    genero_pelicula = pelicula_usuario['Genres'].values[0]

    # Generamos diferentes recomendaciones en base a diferentes condiciones
    recomendaciones = []

    # Condición 1: Coincidencia de director, actores y género
    if not pd.isna(director_pelicula) and not pd.isna(actores_pelicula) and not pd.isna(genero_pelicula):
        recomendaciones += df[
            (df['Genres'].str.contains(genero_pelicula, case=False, na=False)) &
            (df['Director'].str.contains(director_pelicula, case=False, na=False)) &
            (df['Cast'].str.contains(actores_pelicula, case=False, na=False))
        ]['Title'].tolist()

    # Condición 2: Coincidencia de director y género
    if not pd.isna(director_pelicula) and not pd.isna(genero_pelicula):
        recomendaciones += df[
            (df['Genres'].str.contains(genero_pelicula, case=False, na=False)) &
            (df['Director'].str.contains(director_pelicula, case=False, na=False))
        ]['Title'].tolist()

    # Condición 3: Coincidencia de actores y genero
    if not pd.isna(actores_pelicula) and not pd.isna(genero_pelicula):
        recomendaciones += df[
            (df['Genres'].str.contains(genero_pelicula, case=False, na=False)) &
            (df['Cast'].str.contains(actores_pelicula, case=False, na=False))
        ]['Title'].tolist()

    # Condición 4: Coincidencia de genero
    if not pd.isna(genero_pelicula):
        recomendaciones += df[
            (df['Genres'].str.contains(genero_pelicula, case=False, na=False))
        ]['Title'].tolist()

    # Eliminamos las peliculas duplicadas y tambien la pelicula base
    recomendaciones = list(set(recomendaciones))
    if usuario_texto.capitalize() in recomendaciones:
        recomendaciones.remove(usuario_texto.capitalize())

    # Vamos a mostrar los resultados de la busqueda
    if recomendaciones:
        resultados.insert("insert", "Recomendaciones basadas en tu elección:\n")
        resultados.insert("insert", "\n".join(recomendaciones))
    else:
        resultados.insert("insert", "No se encontraron recomendaciones basadas en tu elección.\n")

# Creamos una funcion para limpiar la busqueda actual
def limpiar_busqueda():
    entrada_usuario.set("")
    resultados.delete("1.0", "end")

# Vamos a crear la interfaz grafica con la cual el usuario va a interactuar
netflix_label = CTkLabel(raiz, text="NETFLIX", font=("Arial", 60,"bold"),text_color="red")
netflix_label.place(relx=0.5,rely=0.10,relheight=1,relwidth=0.5,anchor="center")

entrada_label = CTkLabel(raiz, text="Ingresa el título de una película o serie", font=("arial",18,"bold"),text_color="red")
entrada_label.place(relx=0.5,rely=0.20,relheight=0.06,relwidth=0.65,anchor="center")

entrada = CTkEntry(raiz, textvariable=entrada_usuario, font=("Arial", 14))
entrada.place(relx=0.5,rely=0.32,relheight=0.05,relwidth=0.4,anchor="center")

boton_buscar = CTkButton(raiz, text="Buscar Recomendaciones", command=recomendaciones_pelicula,fg_color="red",font=("arial",12,"bold"))
boton_buscar.place(relx=0.5,rely=0.42,relheight=0.05,relwidth=0.25,anchor="center")

boton_limpiar = CTkButton(raiz, text="Limpiar", command=limpiar_busqueda,fg_color="red",font=("arial",12,"bold"))
boton_limpiar.place(relx=0.5,rely=0.5,relheight=0.05,relwidth=0.1,anchor="center")

resultados = CTkTextbox(raiz)
resultados.place(relx=0.5,rely=0.75,relheight=0.4,relwidth=0.72,anchor="center")

# Por ultimo ejecutamos la aplicacion
raiz.mainloop()
