
# Manual de instalación de Allure TestOps para Ubuntu 20.04.4

_Este proyecto tiene el objetivo de lograr una correcta instalación de todas las 
dependencias necesarias para Selenium-Python, Allure Test Ops, y Jenkins._

## Características del servidor Ubuntu  📋

* **RAM:** 6 GB de RAM 
* **CPU:** 4vCPU
* **Tamaño de almacenamiento:** 20 GB 

## Instalación de dependencias para Selenium 🛠

* _Instalación de python_

```bash
  apt install python3-pip
```
* _Instalación de selenium_
```bash
  pip install selenium
```
* _Instalación de webdriver manager_
```bash
  pip install webdriver-manager
```
* _Instalación de pytest y el plugin del allure_
```bash
  apt install python-pytest
  pip install allure-pytest
```

## Instalación de navegadores para Ubuntu 🌐

* _Instalación de Google Chrome_

```bash
  sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
  sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
  sudo apt -y update 
  sudo apt -y install google-chrome-stable 
```

* _Instalación de Firefox_

```bash
  sudo apt-get update
  sudo apt install firefox
```

* _Instalación de Edge_

```bash
  curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
  sudo apt-get update
  sudo apt install microsoft-edge-stable
```

* _Instalación de Opera_

```bash
  wget -qO- https://deb.opera.com/archive.key | sudo apt-key add -
  sudo add-apt-repository "deb [arch=i386,amd64] https://deb.opera.com/opera-stable/ stable non-free" 
  sudo apt update
  sudo apt install opera-stable
```
##  Allure TestOps 📊

### Docker 🐳

* _Instalación de Docker_

```bash
  apt install docker.io
```

* _Instalación de Docker Compose_
```bash
  sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  docker-compose --version
```

* _Inicio de sesión en el registro de Docker: usando el nombre de usuario - qametaaccess 
  (Solicitará la contraseña, que se encuentra en el correo recibido)_

```bash
  docker login --username qametaaccess
```

* _Descarga de archivos por docker compose_ 

```bash
  wget https://docs.qameta.io/allure-testops/dist/allure-testops.zip
  unzip allure-testops.zip
  rm allure-testops.zip
  cd allure-testops
```

### Actualización de archivos de docker compose ✍
* _Actualizamos el archivo **.env** (Reemplazar con la [última versión]("https://docs.qameta.io/allure-testops/release-notes/"))_
```bash
  VERSION: 3.193.0
```
* _Adicionalmente Modificamos el puerto al 8081 para evitar problemas con Jenkins_

```bash
  ENDPOINT=http://localhost:8081 
  SERVER_PORT=8081
```

* _Y actualizamos `JWT_SECRET` con la salida del siguiente comando:_ `openssl rand -base64 16`
```bash
  JWT_SECRET: qOa07Nt6nvE/vrHoz+Ogvg==
```
### Iniciar Allure TestOps 🚀
Una vez que haya completado todas sus opciones de configuración, en la misma carpeta, 
puede obtener todas las dependencias y ejecutar la configuración con docker-compose: 
```bash
  docker-compose pull       # descargará las imagenes necesarias
  docker-compose up -d      # empezará la configuración
```
La inicialización suele tardar hasta 5 minutos. Puede verificar la preparación del sistema ejecutando el siguiente comando en la terminal
```bash
  docker-compose logs | grep "Application 'allure-ee-"
```
Si ve el siguiente resultado, es decir, las tres líneas, entonces la aplicación está lista
```bash
  report_1     |  Application 'allure-ee-report' is running! Access URLs:
  gateway_1    |  Application 'allure-ee-gateway' is running! Access URLs:
  uaa_1        |  Application 'allure-ee-uaa' is running! Access URLs:
```
## Jenkins 👨‍🦱
### Instalación 
Pasos para la instalación:
```bash
  sudo apt-get update
  sudo apt-get install openjdk-11-jdk
  wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
  sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
  sudo apt-get update
  sudo apt-get install jenkins
```
_Si tiene problemas con iniciarse use el comando:_
```bash
  sudo systemctl start jenkins #Iniciará el servicio de jenkins
  sudo systemctl status jenkins #Verificará el estado del servicio
```
### Configuración ⚙️
Para obtener la contraseña de desbloqueo necesitamos ejecutar este comando y usar la salida como contraseña
```bash
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
_Seguido a ello seleccionamos la opción de instalar plugins sugeridos_

![Personalizar Jenkins](https://imgur.com/dMV93S3.png)

_Luego podremos crear un usuario administrador_

![Crear usuario administrador](https://imgur.com/YreW22u.png)

## Integraciones con Jenkins CI 👨‍🦱📊
Este apartado nos ayudará a integrar Allure TestOps con el servidor Jenkins CI.

### 1. Instalar	plug-in	[en Jenkins](https://docs.qameta.io/allure-testops/integrations/jenkins/install-plugin/)
**1.1** Descargue el complemento [allure-jenkins](https://qameta.github.io/distributions/#allure-testops-jenkins) de github.io 

**1.2** En la página principal de Jenkins, vaya a Administrar Jenkins » Administrar complementos.
  ![Administrar plugins](https://imgur.com/gDfWYLN.png)

**1.3** Vaya a la pestaña Avanzado, haga clic en Elegir archivo y seleccione allure-jenkins.hpi que descargó en el paso n.º 1
  ![Administrar plugins](https://imgur.com/au7xeOl.png)

**1.4** Jenkins instalará el complemento y podrá continuar con los pasos posteriores del proceso de integración.

### 2. Configurar la autenticación en Allure TestOps y en Jenkins

* _Hay 2 autenticaciones que necesitamos configurar, en ambos casos necesitamos un token:_

  #### Autenticar Jenkins en Allure TestOps, generando un token secreto en el lado de Allure TestOps: 

  **2.1** Nos dirigimos al perfil y luego a la sección de Tokens de API, y creamos uno nuevo

  ![Perfil](https://imgur.com/lyD0fph.png) 
  
  **2.2** Asignamos un nombre y **copiamos el token**

  ![Token](https://imgur.com/l6kJaCH.png)

  **2.3** Agregue la información de su instancia de servidor Allure a la configuración de Jenkins.

  **2.4** Abrimos la página de configuración de Jenkins: Administrar Jenkins > Configurar sistema

  **2.5** Vamos a la sección Servidores Allure de la página de configuración y hacemos click en agregar

  ![Allure Servers](https://imgur.com/VqFhKWf.png)

  **2.6** Ingresamos el EndPoint del servidor de Allure y en la sección Credenciales, hacemos click en el botón Agregar y cree una credencial con el parámetro "Kind" = Secret Text y pegue el **token que generó en el paso anterior.**

  ![Credenciales](https://imgur.com/YCYWwGx.png)

  **2.7** Elejimos las credenciales creadas de la lista desplegable Credenciales y presione el botón Probar conexión

  ![Credenciales2](https://imgur.com/IL7Wwvj.png)

  #### Autenticar Allure TestOps en Jenkins, generando un token API para el usuario de Jenkins que se usará para Allure TestOps

  **2.8** Vamos a la configuración del usuario

  ![Configuración Jenkins](https://imgur.com/CQ64oot.png)
  
  **2.9** Agregamos un nuevo API-token para el usuario

  ![Nuevo API](https://imgur.com/gxH7GoV.png)
  
  **2.10** Guardamos el token nuevo en un lugar seguro ya que no puede recuperarlo de Jenkins

  ![Token](https://imgur.com/I6ebokx.png)

  **2.11** Creamos credenciales para Jenkins en la sección Administración en Allure TestOps
  
  **IMPORTANTE:** El username es el nombre de usuario que esté en Jenkins, y el password es el token generado

  ![Credenciales Allure](https://imgur.com/bDIr9GP.png)

  **2.12** Creamos el servidor de compilación para el sistema Jenkins
  * En el área de Administración de Allure TestOps, vaya a la sección Servidor de compilación y cree un nuevo servidor de compilación para su instancia de Jenkins.

  * Use el tipo de jenkins y las credenciales que creó en el paso anterior; seleccione de la lista desplegable.

  * Pruebe la conexión haciendo clic en el botón Probar conexión y envíe los datos.

  ![Servidor de Jenkins en Allure](https://imgur.com/7bIDYs8.png)

### 3. Configurar un trabajo de compilación [en Jenkins](https://docs.qameta.io/allure-testops/integrations/jenkins/cfg-job/)

  #### Configuración de trabajo de compilación de estilo libre único

  * Abrimos la página de configuración de trabajo (New Job), ingresamos un nombre para el Job y luego seleccione **"Crear un proyecto de estilo libre"**
  
  * Vamos a la sección de parametros y seleccionamos uno nuevo, de tipo Elección.

    ![Git](https://imgur.com/buJBs5I.png)
  
  * Ingresamos el parámetro para el Navegador con los siguientes datos: 

    ![Git](https://imgur.com/U1uNCas.png)

  * Agregamos un nuevo parámetro llamado Display que será el tamaño del navegador (este será de tipo cadena de texto):

    ![Git](https://imgur.com/8NxECSo.png)

  * Después agregamos un último parámetro, que es el Host

    ![Git](https://imgur.com/gYaJ30J.png)

  * Luego nos dirigimos a la sección de configurar el origen del código fuente, y luego ingresamoe el repositorio de las pruebas
  
    ![Git](https://imgur.com/5TM9aJ5.png)
  
  * Seguido a ello, tenemos que ingresar la [clave privada](https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/) dentro de las credenciales, con el usuario del servidor de Ubuntu, en mi caso fue root
  
    ![Credenciales ssh](https://imgur.com/JaVbEvH.png)
  
  * Luego de obtener acceso al repositorio, tenemos la posbilidad de **cambiar la rama**

    ![Git completo](https://imgur.com/2KYTFPW.png)

  * Ahora nos dirigimos a la sección Entorno de ejecución

  * Luego habilitamos la casilla de **Allure: upload results**, y agregamos los siguientes datos
  
  **IMPORTANTE:** la carpeta de results tiene que estar ubicada en el mismo lugar donde la creamos con el comando, en este caso será **"./allure-results"**

  ![Job Allure](https://imgur.com/eTWQ5gd.png)

  * **Servidor:** es el nombre del servidor Allure TestOps que asignó en Configurar sistema de Jenkins.
  * **Proyecto:** es una lista desplegable que tiene todo el proyecto del servidor Allure TestOps. Esto establecerá el proyecto de destino donde se almacenarán los resultados de su prueba.
  * **Nombre del lanzamiento:** aparecerá en el área de lanzamientos de Allure TestOps, donde se almacenan, analizan y procesan todos los resultados de las pruebas. Si usa las variables de Jenkins, el nombre de lanzamiento se cambiará dinámicamente de acuerdo con el número de compilación.
  * **Etiquetas de lanzamiento:** etiquetas para un trabajo en particular, en el lado de Allure TestOps, lo ayudará a filtrar las pruebas.
  * **Resultados:** ruta en el servidor de CI, donde almacena los resultados de la prueba de este mismo trabajo de compilación.

  * En la sección de **Ejecutar**, seleccionamos la opción de línea de comandos (shell), 
  
  ![Opciones ejecutar](https://imgur.com/qMCHNlO.png)

  * Allí ingresaremos las siguientes lineas

  ![Shell](https://imgur.com/ovUelwg.png)

  * Con esto concluimos la configuración del Job de Jenkins.

### 4. Configurar los entornos de pruebas en Jenkins y Allure TestOps

  * Luego de haber agregado los parámetros como Host, Browser y Display, tenemos que agregarlos a Allure Testops

  * Configuremos la configuración del proyecto Allure TestOps para el procesamiento de información de este entorno.

  ![Configuración Entorno Proyecto](https://imgur.com/kLrLAiT.png)

  * Si la variable no se encuentra en el entorno del proyecto, debemos agregarla desde la administración del servidor

  ![Entorno Allure](https://imgur.com/O8fAsjy.png)


## Documentación

* [Documentación de Allure TestOps](https://docs.qameta.io/allure-testops)
* [Documentación de Docker Compose](https://docs.docker.com/)

