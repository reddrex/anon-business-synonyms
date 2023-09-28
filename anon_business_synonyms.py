# -*- coding: utf-8 -*-
""" from synonyms_anon_business.ipynb
by Jorge Zamora """

""" Dependencias y librerías """
import pandas as pd

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

""" Preprocesamiento """
#leemos con pandas el archivo csv
data = pd.read_csv("/content/Tier5_AB_lemas19.csv", encoding="latin1", sep=";")
#separamos las columnas del archivo csv y las convertimos en listas
l=data["Lemas"].tolist()
f=data["Flexionadas"].tolist()

""" Sinónimos """
#importamos el wordnet, la librería que nos va a ayudar a encontrar las relaciones entre palabras
from nltk.corpus import wordnet

#creamos una lista vacía para los sinónimos, a partir de la cual crearemos luego un dataframe nuevo
sin2=[]

#por cada oración/celda en la lista de lemas
for x in l:
  #aquí almacenamos los sinónimos de cada celda
  sin=""
  #queremos operar sobre cada palabra dentro de ella, lo tokenizamos y quitamos las barras bajas
  tk = x.replace("_", "")
  tk2 = nltk.tokenize.word_tokenize(tk, language='spanish')
  #por cada palabra en cada una de las oraciones tokenizadas
  for y in tk2:
    #queremos obtener todos los lemas/sinónimos dentro de cada set de sinónimos para cada uno de los sentidos de la palabra
    synonym_groups = wordnet.synsets(y, lang="spa")
    #necesitamos saber cuántos grupos de sinónimos (tantos como el nº de sentidos) hay
    n=len(synonym_groups)
    #si la palabra tiene más de una letra, buscamos sus sinónimos
    if len(y) > 1:
      #si tiene algún set de sinónimos
      if n > 0:
        sin3=""
        #por cada sentido en el grupo de sinónimos
        for z in range(n):
          #cogemos cada uno de los sinónimos [lemma_names] dentro de cada sentido [z]
          synonyms=synonym_groups[z].lemma_names(lang="spa") #el tipo de dato es lista, así que tenemos que convertirlo a str
          for k in synonyms: #por cada sinónimo en el grupo de sinónimos de un sentido concreto
            if k==y: #si el sinónimo es el mismo que la palabra, lo dejamos igual
              sin3=f"{sin3}"
            elif k in sin3: #si el sinónimo ya estaba antes en la variable donde guardamos los sinónimos de una palabra (sin3), lo dejamos igual
              sin3=f"{sin3}"
            else:
              sin3=f"{sin3}{k} / "
        sin=f"{sin}'{y}': {sin3} | "
      else:
        sin=f"{sin}'{y}': none | "
    else:
      sin=f"{sin}'{y}': none | "
  #aquí añadimos los sinónimos de cada celda a la lista que creamos antes, cada elemento de la lista será una str, que corresponde a cada celda
  sin2.append(sin)
print(sin2[0]) #imprimimos para comprobar el resultado, con el primer element basta

""" Conversión a formato csv """
ab=pd.DataFrame({"Flex":f, "Lem":l, "Sin":sin2})
print(ab)

ab.to_csv("PRUEBA1.csv", encoding="latin1", sep=";")
