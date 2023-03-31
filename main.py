import subprocess
import random, string
import qrcode
from PIL import Image
from azure.storage.blob import ContainerClient, ContentSettings
from twilio.rest import Client
from config import directorio_origen_video, cuentaSID, cadenaConexionBlob, tokenAutorizacion

#poner aquí la ruta donde se graba el vídeo
ruta_origen = directorio_origen_video 

def getRandomName():
    name = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
    name += "".join(str(random.randrange(0, 9)) for _ in range(5))
    return name

def codigoQR(link): 
    img = qrcode.make(link)
    f = open("output.png", "wb")
    img.save(f)
    f.close()
    im = Image.open("output.png")
    im.show()

def subirABlob(nombreFoto):
    CONNECT_STR = cadenaConexionBlob
    CONTAINER_NAME = "videos"
    input_file_path = f"{ruta_origen}\\videosTransformados\\{nombreFoto}.mp4"
    output_blob_name = f"{nombreFoto}.mp4"
    container_client = ContainerClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME)
    my_content_settings = ContentSettings(content_type="video/mp4")

    with open(input_file_path, "rb") as data:
        container_client.upload_blob(name=output_blob_name, data=data, overwrite=True, content_settings=my_content_settings)
    enviarWhatsapp(nombreFoto)


def enviarWhatsapp(nombre):
    account_sid = cuentaSID
    auth_token = tokenAutorizacion
    client = Client(account_sid, auth_token)
    
    url = f"https://videomatontest.blob.core.windows.net/videos/{nombre}.mp4"
    texto = f"Codigo del video: *{nombre}*"

    message = client.messages \
        .create(body=f'Gracias por participar en uno de nuestros fotomatones La Cabina Gris. \nEsta es el video que te has hecho. \n{texto}',
            media_url=[url],
            from_='whatsapp:+19282784108',
            to='whatsapp:+34690849490'
        )
    
def grabarVideo(nombre):
    nombreSalida = getRandomName()
    dondeEstaHandbrake = "HandBrakeCLI.exe"
    dondeGraboVideo = f"{ruta_origen}\\videosTransformados\\{nombreSalida}.mp4"
    videoAtransformar = f"{ruta_origen}\\{nombre}.mp4"

    handbrake_command = [dondeEstaHandbrake, "-i", videoAtransformar, "-o", dondeGraboVideo,"-e", "x264", "-q", "20", "-B", "160"]
    
    #mas comandos handbrake: https://handbrake.fr/docs/en/latest/cli/cli-options.html

    subprocess.run(handbrake_command, shell=False)
    
    subirABlob(nombreSalida)
    codigoQR(f"https://videomatontest.blob.core.windows.net/videos/{nombreSalida}.mp4")
    
    
if __name__ == "__main__":
    grabarVideo("test")
    