#Grupo 13

María de los Angeles Portal 13196/1
Catalina Ratto 13023/9
Jose Miguel Silva 13630/8
Florencia Paredes 14598/0


# Documentacion API

## Ruta:

```bash
├── app
│   ├── db.py
│   ├── helpers
│   │   ├── auth.py
│   │   └── handler.py
│   ├── __init__.py
│   ├── models
│   │   ├── centro.py
│   │   ├── configuracion.py
│   │   ├── __init__.py
│   │   └── models.py
│   ├── resources  
│   │   ├── api
│   │   │   ├── centros.py
│   │   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── centro.py

```

## Tools:
 [Marshmallow](https://marshmallow.readthedocs.io/en/stable/): Es una libreria que nos ayuda a convertir tipos de datos complejos, como objetos a tipos de datos nativos de Python y viceversa.
Con esto podemos serializar y deserializar JSON para ser añadido a la BD.

 [flask_marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) : Es una libreria que integra Flask y Marshmallow.

 [Postman](https://www.postman.com/) Postman es una aplicacion que nos ayuda a probar el funcionamiento de las Apis, podemos hacer solicitudes de diferente tipo a cualquier endpoint especificado.


## Cambios en el Modelo:
Para adaptar el modelo al uso de Marshmallow, tenemos que definir un Schema, esto sirve para representar el formato que tendra nuestro modelo cuando se hace la conversion a través de marshmallow.


## Definición de formato de respuesta para todos los enpoints
El formatode respues viene dado en formato JSON.
JSON es un formato que almacena información estructurada y se utiliza principalmente para transferir datos entre un servidor y un cliente.
Un objeto comienza con { llave de apertura y termina con llave de cierre }. Cada nombre es seguido por :dos puntos y los pares nombre/valor están separados por ,coma.

## Creación de un ejemplo

Usando Postman usamos el endpoint http://127.0.0.1:5000/api/centros y como metodo usamos POST, esto añadirá un nuevo centro a nuestra base de datos
Seleccionamos body y luego Raw y el tipo debe ser JSON, luego copiamos el codigo:

```bash
{
            "apertura": "09:00:00",
            "cierre": "20:00:00",
            "direccion": "Calle 24 y 12",
            "email": "pruebajson@gmail.com",
            "nombre": "Centro los alamos",
            "telefono": "112233123",
            "tipo_centro": "ropa",
            "web": "centrolosalamos.com",
            "municipio": "La Plata"
}
```
Al pulsar send deberiamos obtener la respuesta:
```bash
[
    {
        "centro": {
            "apertura": "09:00:00",
            "cierre": "20:00:00",
            "direccion": "Calle 24 y 12",
            "email": "pruebajson@gmail.com",
            "municipio": "La Plata",
            "nombre": "Centro los alamos",
            "telefono": "112233123",
            "tipo_centro": "COMIDA",
            "web": "centrolosalamos.com"
        }
    },
    201
]

```

Esto retorna el centro añadido y el codigo 201.
En caso de querer introducir un centro ya existente:
```bash
{
    "message": "El centro ya existe"
}
```

Si queremos ver los centros, habría que cambiar el metodo a GET con el mismo endpoint:
```bash

{
            "apertura": "09:00:00",
            "cierre": "20:00:00",
            "direccion": "Calle 24 y 12",
            "email": "pruebajson@gmail.com",
            "municipio": "La Plata",
            "nombre": "Centro los alamos",
            "telefono": "112233123",
            "tipo_centro": "COMIDA",
            "web": "centrolosalamos.com"
        }
    ],
    "pages": 8,
    "per_page": 2
}
```
Y vemos el centro creado previamente, además de las paginas y los elementos por página tomados de la configuración.

Si queremos buscar un centro en concreto seleccionamos GET como método y cambiamos el endpoind a:
http://127.0.0.1:5000/api/centros/:id 

```bash

[
    {
        "centro": {
            "apertura": "09:00:00",
            "cierre": "20:00:00",
            "direccion": "Calle 24 y 12",
            "email": "pruebajson@gmail.com",
            "municipio": "La Plata",
            "nombre": "Centro los alamos",
            "telefono": "112233123",
            "tipo_centro": "COMIDA",
            "web": "centrolosalamos.com"
        }
    },
    200
]


```
