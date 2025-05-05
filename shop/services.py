# shop/services.py

import requests
from django.conf import settings

def obtener_juegos_externos(limit=9):
    """
    Consume la API de IGDB y devuelve una lista de juegos.
    De momento devuelve una lista vacía si falta configurar credenciales.
    """
    client_id     = settings.IGDB_CLIENT_ID
    client_secret = settings.IGDB_CLIENT_SECRET

    if not client_id or not client_secret:
        # Si no están en el .env, devolvemos lista vacía para seguir probando el front
        return []

    # 1) Obtener token OAuth de Twitch (IGDB usa Twitch auth)
    auth = requests.post(
        'https://id.twitch.tv/oauth2/token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
    ).json()

    token = auth.get('access_token')
    if not token:
        return []

    # 2) Petición a IGDB para obtener datos
    headers = {
        'Client-ID':     client_id,
        'Authorization': f'Bearer {token}'
    }
    # Ejemplo de body: campos name, cover.url, summary
    body = 'fields name,cover.url,summary; limit %d;' % limit

    resp = requests.post('https://api.igdb.com/v4/games', headers=headers, data=body)
    if resp.status_code != 200:
        return []

    return resp.json()
