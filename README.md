Caracteristicas
=============

- Calcula la Máscara de Subred de Longitud Variable (VLSM) para una dirección de red y un conjunto de hosts por red.
- Utiliza la fórmula logarítmica para determinar el número de bits necesarios para los hosts.
- Muestra la máscara de subred VLSM calculada.

**Ten en cuenta que este script está diseñado para funcionar con direcciones IPv4 estándar y no es compatible con direcciones IPv6.**


Documentación 
=============

Este script está diseñado para calcular la subnetización utilizando VLSM (Variable Length Subnet Masking). Se considera útil en casos donde se necesita un número específico de hosts para diferentes subredes dentro de la misma red. A continuación, se proporciona una descripción detallada de las funciones y cómo utilizar este script.

Descripción general
-------------
Este script de Python permite a los usuarios introducir una dirección de red y un conjunto de números que representan la cantidad de hosts requeridos en cada subred. Con esta información, el script calcula las máscaras de subred necesarias para cada subred y proporciona información adicional, como la dirección de red, el rango de direcciones IP utilizables, la dirección de difusión, la máscara de subred y el número de hosts direccionables.

Requisitos
-------------
Este script requiere Python 3 y la biblioteca 'colored' para colorear el texto en la terminal. Para instalar 'colored', puede utilizar pip:

`pip install colored`


Funciones en el script
-------------
El script contiene varias funciones que realizan una variedad de tareas:

| Funciones | Descripción                    |
| ------------- | ------------------------------ |
| `is_empty(text)`      | Comprueba si el texto dado está vacío..       |
| `is_correct_network_address(address)`   | Comprueba si la dirección de red introducida es válida.     |
| `is_correct_endpoint_numbers_per_network(numbers)`      | Comprueba si el número de endpoints por red introducido es válido.
| `is_correct_prefix(prefix)`      | Comprueba si el prefijo de subred introducido es válido.       |
| `power_bit_length(x)`      | Devuelve el número de bits necesarios para representar un número dado.      |
| `get_mask_from_prefix(prefix)`      | Comprueba si el texto dado está vacío..      |
| `get_32bit_format(ip_address)`      | Convierte una dirección IP en su representación binaria de 32 bits. |
| `get_ip_from_32bit_format(format_32bit)`      | Convierte una representación binaria de 32 bits en una dirección IP.      |
| `get_first_addressable_ip(network_ip)`      |  Obtiene la primera dirección IP direccionable de la subred.     |
| `get_last_addressable_ip(network_ip, mask)`      |  Obtiene la última dirección IP direccionable de la subred.       |
| `get_broadcast_ip(network_ip, mask)`      | Calcula la dirección IP de difusión de la subred.    |
| `get_next_network_ip(network_ip, mask)`      |Obtiene la dirección de la próxima red.       |
| `calculate_vlsm(network_ip, endpoint_numbers_per_network, prefix)`      | Realiza los cálculos VLSM y devuelve las subredes.      |
| `inject_data_to_dict(network_ip, length_of_subnets, subnets)`      | Inyecta los datos calculados en un diccionario.      |
| `main()`      |La función principal que toma las entradas del usuario y llama a las otras funciones.  |

¿Cómo usar?
-------------
1. Ejecute el script de Python en su terminal.
`py vlsm.py`
2. Cuando se le solicite, introduzca la dirección de red inicial.
3. A continuación, introduzca el número de hosts que se requieren en cada subred, separados por comas.
4. Finalmente, puede introducir un prefijo de máscara de subred opcional.
5. El script devolverá la información de la subred para cada número de hosts que haya proporcionado.

![Como usar el script](howtouse.gif)
