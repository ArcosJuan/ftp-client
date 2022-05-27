# FTP - File Transfer Protocol / Protocolo de transferencia de archivos

##  Que es un protocolo y de donde sale.
Un protocolo es un conjunto de reglas y procedimientos que permiten el exitoso envío y recibimiento de mensajes entre distintos dispositivos. Estas reglas y procedimientos pueden ser, por ejemplo, que puertos participan en la conexión, como debe establecerse la conexión, que tipo de datos se pueden enviar a través de ella, como deben estructurarse esos datos para que sean interpretados correctamente o que respuestas se esperan recibir. Estas reglas y procedimientos son descritas en ciertos documentos por organizaciones de normalización.
En cuanto al protocolo FTP, este se encuentra descrito en uno de los documentos [RFC](https://www.rfc-editor.org) (Request For Comments) creado por la organización de normalización [IETF](https://www.ietf.org) (Internet Engineering Task Force), que además de describir el protocolo FTP también describe muchos otros protocolos estandarizados.

## El protocolo FTP
### Historia y objetivos
El protocolo FTP fue descrito por primera vez en 1971, en el [RFC 114](https://datatracker.ietf.org/doc/html/rfc114), y desde ese entonces ha recibido varias actualizaciones, pasando de 17 a 69 páginas. En su primera versión definía como objetivo principal promover el uso indirecto de computadoras en la red, osea, el poder intercambiar información entre computadoras sin la necesidad de entender como entrar, o utilizar, un sistema remoto. El documento más actual en describir la funcionalidad del FTP ([RFC 959](https://datatracker.ietf.org/doc/html/rfc959)) añade otros 3 objetivos:
- Promover el intercambio de archivos.
- Proteger al usuario de variaciones en los sistemas de almacenamiento de archivos entre hosts.
- Transferir información de manera confiable y segura.

Aun asi FTP no es el unico protocolo de transferencia de archivos, tambien existen otros similares como HTTP. Pero estos no pueden transferir archivos de gran tamaño con la eficacia de FTP.

### Cómo funciona la comunicación utilizando FTP
FTP funciona encima de TCP y sigue el modelo Cliente-Servidor. Para transferir archivos requiere de dos conexiones TCP. Primero el cliente debe establecer una "conexión de control" entre uno de sus puertos y el puerto **21 (estándar)** del servidor, a través de esta conexión el cliente envia, en formato ASCII, comandos al servidor y en este mismo formato recibe respuestas del servidor. Luego, al solicitar se una transferencia de archivos se abrirá "conexión de datos" a través de la cual se enviarán o recibirán, en formato binario, los archivos que decidan transferirse. Existen dos formas de establecer la conexión de datos:
- **Activa**: El cliente envía al servidor una solicitud de transferencia de datos junto con uno de sus puertos. El servidor, al recibir esta solicitud, abre una conexión de datos entre su puerto **20 (estándar)** y el puerto que recibe del cliente.
- **Pasiva**: El cliente solicita al servidor uno de sus puertos disponibles. Al recibir el puerto del servidor, el cliente establece la conexión de datos entre uno de sus puertos y el enviado por el servidor.
(Es más común que se utilice una conexión pasiva ya que las conexiones activas pueden dar problemas con el firewall del cliente)

Una vez establecida la conexión el cliente poseerá permisos según sus credenciales (nombre y contraseña). Es posible, igualmente, establecer conexiones anónimas, osea, que no requieren de ninguna credencial.

### Control de errores
FTP no tiene detección de pérdida de datos durante la transmisión, este nivel de errores son manejados por el protocolo TCP encima del cual está construido. Por este mismo motivo la conexión no brinda ningún tipo de seguridad. Para una conexión segura existe el protocolo SFTP, que se aprovecha del protocolo SSH.

##  Implementacion
Implementamos el protocolo FTP para la creación de [ftp-client](https://github.com/ArcosJuan/ftp-client), una interfaz de cliente por terminal que simplifica el envío de comandos al servidor. Las herramientas que se usaron para esta implementación fueron python y su librería ftplib.

Se puede observar en el código fuente, que utilizamos las funciones built-in de python para la ejecución de comandos en vez métodos como [ftp.voidcmd()](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L283) que son más generalizables. Esto se debe a que los métodos built-in de python contienen comprobaciones específicas de cada comando que mejoran la interpretación de la entrada y el formato de la salida.

### Trabajo interno de las funciones
A continuación se muestran dos diagramas que presentan una visión general de lo que sucede internamente en el código de las funciones que utiliza ftp-client.

Estos dos ejemplos presentan como funciona la comunicación a través de la conexión de control (en [Change directory](https://github.com/ArcosJuan/ftp-client/blob/main/ftp_client.py#L92)), y la conexión de datos (en [Download](https://github.com/ArcosJuan/ftp-client/blob/main/ftp_client.py#L127))

#### Change directory (ftp.cwd)
![change_dir_diagram](https://user-images.githubusercontent.com/87381835/170430048-26eb1ac8-8795-4126-8aef-7f82f12c1fdd.png)


**Funciones de ftplib:**

1º [cwd](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L614)

2º [voidcmd](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L283)

3º [putcmd](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L205)

4º [putline](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L195)
#### Download (ftp.retrbinary)
![download_diagram](https://user-images.githubusercontent.com/87381835/170430106-8359ca96-cfe7-43f7-8108-2570dfe87d5a.png)

**Funciones de ftplib:**

1º [retrbinary](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L421)

2º [transfercmd](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L391)

3º [ntransfercmd](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L336)

4º [makeport](https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L311)

### Tutorial
Al iniciar la aplicación se le solicitará ingresar:
- El host del servidor al que se desea conectar.
- El puerto específico del servidor con el que quiere establecer la conexión de control (Si no ingresa nada, por defecto se establece en 21).
- El nombre de usuario con el que ingresar al servidor (opcional).
- La contraseña con la que desea ingresar al servidor (opcional).
( Si el nombre y la contraseña no son establecidos se estará estableciendo una conexión anónima)

Una vez establecida la conexión, se le presentan en pantalla todos los comandos disponibles. Al ingresar el número de la opción que corresponda al comando que desee ejecutar, el mismo, se ejecutará. En caso de necesitar parámetros se le solicitarán en pantalla.

A tener en cuenta: Si se cierra la conexión de manera inadecuada, cabe la posibilidad de que no se pueda volver a ejecutar el programa inmediatamente debido a que al estar FTP construido por encima de TCP, las conexiones TCP, por protocolo, permanecen abiertas un tiempo para garantizar la confiabilidad de la conexión.

### Referencias
RFCs:
- https://datatracker.ietf.org/doc/html/rfc959
- https://datatracker.ietf.org/doc/html/rfc114

Codigo:
- https://github.com/E-Renshaw/ftp-socket-server-python/blob/master/Client/client.py
- https://github.com/python/cpython/blob/9b027d4cea57e98c76f5176cc3188dc81603356c/Lib/ftplib.py#L1

+Info:
- https://www.geeksforgeeks.org/file-transfer-protocol-ftp/
- https://es.wikipedia.org/wiki/UTF-8
- https://www.youtube.com/watch?v=P2p7KAkJCMk
- https://es.wikipedia.org/wiki/Grupo_de_Trabajo_de_Ingeniería_de_Internet

