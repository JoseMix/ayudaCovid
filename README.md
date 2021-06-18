# Introdución
Lenguaje usado:Python 3.  
Frameworks:Flask y Vue.
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
│   │   │   └── turno.py


```

## Tools:

[Marshmallow](https://marshmallow.readthedocs.io/en/stable/): Es una libreria que nos ayuda a convertir tipos de datos complejos, como objetos a tipos de datos nativos de Python y viceversa.
Con esto podemos serializar y deserializar JSON para ser añadido a la BD.

[flask_marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) : Es una libreria que integra Flask y Marshmallow.

[Postman](https://www.postman.com/) Postman es una aplicacion que nos ayuda a probar el funcionamiento de las Apis, podemos hacer solicitudes de diferente tipo a cualquier endpoint especificado.

## Cambios en el Modelo:

Para adaptar el modelo al uso de Marshmallow, tenemos que definir un Schema, esto sirve para representar el formato que tendra nuestro modelo cuando se hace la conversion a través de marshmallow.

## Definición de formato de respuesta para todos los enpoints

El formato de respuesta viene dado en formato JSON.
JSON es un formato que almacena información estructurada y se utiliza principalmente para transferir datos entre un servidor y un cliente.
Un objeto comienza con { llave de apertura y termina con llave de cierre }. Cada nombre es seguido por :dos puntos y los pares nombre/valor están separados por ,coma.

## Creación de un ejemplo

**Centros**  
Usando Postman usamos el endpoint http://127.0.0.1:5000/api/centros/ y como metodo usamos POST, esto añadirá un nuevo centro a nuestra base de datos
Seleccionamos body y luego Raw y el tipo debe ser JSON, luego copiamos el codigo:

```bash
{
            "apertura": "09:00",
            "cierre": "20:00",
            "direccion": "Calle 24 y 12",
            "email": "pruebajson@gmail.com",
            "nombre": "Centro los alamos",
            "latitud": "1.4556",
            "longitud": "-12.567",
            "telefono": "112233123",
            "tipo_centro": "ropa",
            "web": "http://centrolosalamos.com",
            "id_municipio": 1
}

```

Al pulsar send deberiamos obtener la respuesta:

```bash
[
    {
        "centro": {
            "nombre": "Centro los alamos",
            "tipo_centro": "ROPA",
            "cierre": "20:00",
            "direccion": "Calle 24 y 12",
            "apertura": "09:00",
            "web": "http://centrolosalamos.com",
            "email": "pruebajson@gmail.com",
            "latitud": 1.4556,
            "longitud": -12.567,
            "telefono": "112233123"
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

Si queremos ver los centros, habría que cambiar el metodo a GET con el endpoint: http://127.0.0.1:5000/api/centros/ que devuelve la primera pagina con las paginas totales y el numero de elementos por página.
En caso de querer una página en particular le pasamos el parametro page en la url: http://127.0.0.1:5000/api/centros/?page=1

```bash

{
            "id": 1,
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

```bash

  {
    "centros": [
      [
        {
          "id": 1, 
          "direccion": "Calle 24 y 12", 
          "apertura": "12:00", 
          "telefono": "112233123", 
          "email": "pruebajson@gmail.com", 
          "latitud": 1.4556, 
          "longitud": -12.567, 
          "nombre": "Centro los alamos", 
          "tipo_centro": "ROPA", 
          "web": null, 
          "cierre": "20:00"
        }
      ]
    ], 
    "pages": 1, 
    "per_page": 4
  }
```

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

**Turnos**  
En Postman usamos el endpoint http://127.0.0.1:5000/api/centros/<int:centro_id>/turnos_disponibles/?fecha=<fecha>
La Api nos devolvera el listado de turnos disponibles para una fecha dada y en caso de no existir la fecha, nos dará los turnos disponibles en la fecha de hoy, para ese centro.
El formato de la fecha debe ser el siguiente: dd-mm-AAAAA
http://127.0.0.1:5000/api/centros/1/turnos_disponibles/?fecha=22-11-2020

```bash
[
    {
        "centro_id": 1,
        "fecha": "22-11-2020",
        "turno": [
            {
                "hora_inicio": "09:00",
                "hora_fin": "09:30"
            },
            {
                "hora_inicio": "09:30",
                "hora_fin": "10:00"
            },
            {
                "hora_inicio": "10:00",
                "hora_fin": "10:30"
            },
            {
                "hora_inicio": "10:30",
                "hora_fin": "11:00"
            },
            {
                "hora_inicio": "11:00",
                "hora_fin": "11:30"
            },
            {
                "hora_inicio": "11:30",
                "hora_fin": "12:00"
            },
            {
                "hora_inicio": "12:00",
                "hora_fin": "12:30"
            },
            {
                "hora_inicio": "12:30",
                "hora_fin": "13:00"
            },
            {
                "hora_inicio": "13:00",
                "hora_fin": "13:30"
            },
            {
                "hora_inicio": "13:30",
                "hora_fin": "14:00"
            },
            {
                "hora_inicio": "14:00",
                "hora_fin": "14:30"
            },
            {
                "hora_inicio": "14:30",
                "hora_fin": "15:00"
            },
            {
                "hora_inicio": "15:00",
                "hora_fin": "15:30"
            },
            {
                "hora_inicio": "15:30",
                "hora_fin": "16:00"
            }
        ]
    },
    200
]


```

Utilizamos el endpoint http://127.0.0.1:5000/api/centros/:id/reserva/ con el metodo POST. Esto dará de alta un turno en caso de que esté disponible para el centro, el día y la hora indicada.
La entrada debería ser de la siguiente forma:

```bash
    {
        "email" : "juan.perez@gmail.com" ,
        "nombre" : "Juan",
        "apellido" : "Perez",
        "telefono" : "221-5930941" ,
        "hora_inicio" : "15:00" ,
        "hora_fin" : "15:30" ,
        "fecha" : "29-11-2020" ,
    }

```

Al precionar SEND, en caso de que el turno haya sido creado exitosamente se producirá la siguiente salida:

```bash
[[
    {
        "turno": {
            "centro_id": "1",
            "email": "juan.perez@gmail.com"
        },
        "telefono": "112233123",
        "hora_inicio": "15:00",
        "hora_fin": "15:30"
    },
    201
]
```

En caso de que para los datos seleccionados ya exista un turno ocupado se mostrará lo siguiente:

```bash
[
    {
        "message": "El turno ya existe",
    }
]
```

Si intentamos reservar un turno en una fecha anterior a la actual o a más de 3 días se mostrará lo siguiente:

```bash
[
    {
        "message": "La fecha no esta en el rango de los 3 proximos días"
    }
]
```
