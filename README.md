
# Flask Ecosmart Backend

backend para la aplicación movil Ecosmart, una plataforma para gestionar materiales reciclables,localizar puntos de reciclajes y promover la practica del reciclaje mediante recompensas. 

## Características

*   **Autenticación de usuarios:** Los usuarios pueden registrarse e iniciar sesión en la aplicación.
*   **Gestión de productos:** Los usuarios pueden crear, ver y eliminar sus productos reciclables.
*   **Gestión de pedidos:** Los usuarios pueden crear, ver y eliminar sus ordenes de reciclaje.
*   **Sistema de recompensas:** Los usuarios pueden ganar puntos por reciclar y ver sus recompensas.
*   **Centros de reciclaje:** Los usuarios pueden ver una lista de centros de reciclaje.
*   **Categorías:** Los productos se organizan por categorías.

## Tecnologías

*   **Flask:** Un micro framework web para Python.
*   **MySQL:** Un sistema de gestión de bases de datos relacionales.
*   **Cloudinary:** Un servicio de gestión de imágenes y vídeos basado en la nube.
*   **JWT:** Un estándar para crear tokens de acceso.
*   **Bcrypt:** Una función de hash de contraseñas.

## Instalación

1.  Clona el repositorio:
    ```
    git clone https://github.com/tu-usuario/flask-ecosmart-backend.git
    ```
2.  Crea un entorno virtual:
    ```
    python -m venv Ecosmart_venv
    ```
3.  Activa el entorno virtual:
    ```
    Ecosmart_venv\Scripts\activate
    ```
4.  Instala las dependencias:
    ```
    pip install -r requirements.txt
    ```
5.  Crea un archivo `.env` y añade las siguientes variables de entorno:
    ```
    MYSQL_HOST=
    MYSQL_USER=
    MYSQL_PASSWORD=
    MYSQL_DB=
    MYSQL_PORT=
    JWT_SECRET_KEY=
    CLOUDINARY_CLOUD_NAME=
    CLOUDINARY_API_KEY=
    CLOUDINARY_API_SECRET=
    ```
6.  Ejecuta la aplicación:
    ```
    flask --app index.py run 
    ```

## Endpoints de la API

| Método | Endpoint | Descripción |
| --- | --- | --- |
| POST | /auth/login | Inicia sesión de un usuario. |
| POST | /auth/register | Registra un nuevo usuario. |
| GET | /auth/profile | Obtiene el perfil del usuario autenticado. |
| POST | /api/product | Crea un nuevo producto. |
| GET | /api/product | Obtiene todos los productos del usuario autenticado. |
| DELETE | /api/product | Elimina un producto. |
| GET | /api/category | Obtiene todas las categorías. |
| GET | /api/centers | Obtiene todos los centros de reciclaje. |
| POST | /api/order | Crea un nuevo pedido. |
| GET | /api/order | Obtiene todos los pedidos del usuario autenticado. |
| DELETE | /api/order | Elimina un pedido. |
| DELETE | /api/complete-order | Elimina un pedido y los materiales asociados a él. |
| PUT | /api/rewards | Actualiza las recompensas del usuario autenticado. |
| GET | /api/rewards | Obtiene las recompensas del usuario autenticado. |

