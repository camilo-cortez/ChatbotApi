import random
import re

def get_faq_suggestions(input_string):
    # Lista de sugerencias relacionadas con la conexión a Internet
    internet_suggestions = [
        "Reinicia el router/modem: Apágalo, espera 10 segundos y enciéndelo nuevamente.",
        "Verifica el cableado: Asegúrate de que todos los cables estén bien conectados.",
        "Reinicia el PC: A veces un simple reinicio puede resolver problemas de conexión.",
        "Verifica el Wi-Fi: Asegúrate de estar conectado a la red correcta y con la contraseña adecuada.",
        "Comprueba si hay cortes de servicio: Contacta a tu proveedor de internet para verificar si hay interrupciones en tu área.",
        "Desactiva y activa el adaptador de red: Ve a 'Configuración de red' y reinicia el adaptador.",
        "Usa el solucionador de problemas de Windows: Entra a Configuración > Actualización y seguridad > Solucionar problemas.",
        "Desactiva el firewall temporalmente: Algunos firewalls pueden bloquear la conexión a Internet.",
        "Actualiza los controladores de la tarjeta de red: Ve al 'Administrador de dispositivos' y actualiza los controladores.",
        "Verifica la configuración de DNS: Configura los servidores DNS manualmente (por ejemplo, 8.8.8.8 y 8.8.4.4 de Google)."
    ]
    
    # Lista de sugerencias relacionadas con problemas de email
    email_suggestions = [
        "Verifica tu conexión a Internet: Asegúrate de estar conectado a la red antes de intentar enviar o recibir correos.",
        "Revisa la configuración del servidor de correo: Verifica que el servidor de salida (SMTP) y el de entrada (IMAP/POP3) estén configurados correctamente.",
        "Borra la caché de tu cliente de correo: En ocasiones, el caché puede causar problemas al enviar o recibir mensajes.",
        "Comprueba los filtros de correo: Revisa que no haya filtros o reglas que estén redirigiendo tus correos a carpetas incorrectas.",
        "Verifica el espacio de almacenamiento en tu cuenta de correo: Si tu buzón está lleno, podrías no poder recibir correos nuevos.",
        "Intenta utilizar otro cliente de correo: Si el problema persiste, prueba con otro software o aplicación de correo para descartar un problema con el cliente.",
        "Desactiva temporalmente el antivirus o firewall: A veces, los programas de seguridad pueden bloquear el acceso al servidor de correo.",
        "Comprueba la configuración de tu dirección de correo: Asegúrate de que la dirección de correo electrónico y la contraseña sean correctas.",
        "Revisa los correos bloqueados o en la carpeta de spam: Asegúrate de que no se haya filtrado algún correo importante.",
        "Actualiza tu cliente de correo: Mantén actualizado el software de correo para asegurarte de contar con las últimas mejoras y correcciones."
    ]
    
    # Lista de sugerencias relacionadas con problemas de teléfono/celular
    phone_suggestions = [
        "Reinicia tu teléfono: Apaga y enciende tu dispositivo para solucionar posibles fallos temporales.",
        "Verifica la cobertura de la red: Asegúrate de estar en un área con buena señal para realizar llamadas o usar datos móviles.",
        "Revisa la configuración de la red móvil: Asegúrate de que los datos móviles y la itinerancia estén habilitados en tu dispositivo.",
        "Borra el caché de las aplicaciones: Algunas aplicaciones pueden generar problemas si acumulan datos de forma incorrecta.",
        "Actualiza el sistema operativo: Asegúrate de que tu teléfono esté actualizado con las últimas correcciones de seguridad y mejoras de rendimiento.",
        "Verifica las actualizaciones de las aplicaciones: Mantén tus aplicaciones actualizadas para asegurarte de que no haya errores de funcionamiento.",
        "Desactiva el modo de ahorro de energía: Algunos teléfonos limitan la conectividad y el rendimiento cuando el modo de ahorro de energía está activado.",
        "Revisa si tienes bloqueada la señal: Asegúrate de que no haya opciones activadas que bloqueen las llamadas o la conexión de datos.",
        "Revisa el espacio de almacenamiento: Si tu dispositivo está lleno, podrías tener problemas para instalar nuevas actualizaciones o descargar archivos.",
        "Restablece la configuración de red: Si tienes problemas con Wi-Fi, Bluetooth o datos móviles, restablecer la configuración de red puede ayudar."
    ]

    # Convertimos el string de entrada a una lista de palabras
    words = input_string.split()

    # Limpiar las palabras de caracteres no alfabéticos usando expresiones regulares
    cleaned_words = [re.sub(r'\W+', '', word.lower()) for word in words]  # Eliminar caracteres no alfabéticos

    # Variable para almacenar las sugerencias seleccionadas
    selected_suggestions = []

    # Buscamos si alguna palabra clave está presente
    for word in cleaned_words:
        if word == "internet" or word == "red":
            selected_suggestions = random.sample(internet_suggestions, 5)
            break
        
        if word == "email":
            selected_suggestions = random.sample(email_suggestions, 5)
            break
        
        if word == "telefono" or word == "celular":
            selected_suggestions = random.sample(phone_suggestions, 5)
            break

    # Si no se encuentran palabras clave, retornamos un mensaje indicando que no hay sugerencias
    if not selected_suggestions:
        return "No se encontraron sugerencias relacionadas con 'internet', 'red', 'email', 'telefono' o 'celular'."
    
    # Formateamos las sugerencias seleccionadas con numeración
    return "\n".join(f"{i+1}. {suggestion}" for i, suggestion in enumerate(selected_suggestions))
