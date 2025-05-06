#shop/management/commands/seed_from_external.py
import os
import requests
from django.core.management.base import BaseCommand
from shop.models import Juego, Categoria

RAWG_API_KEY      = os.getenv('RAWG_API_KEY')
IGDB_CLIENT_ID    = os.getenv('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET= os.getenv('IGDB_CLIENT_SECRET')

CATEGORIAS = ["Aventuras", "Carreras", "Estrategia", "Terror", "Acción"]

class Command(BaseCommand):
    help = 'Carga 25 juegos desde IGDB, repartidos en 5 categorías'

    def handle(self, *args, **kwargs):
        categorias = []
        for nombre in CATEGORIAS:
            cat, _ = Categoria.objects.get_or_create(nombre=nombre)
            categorias.append(cat)

        token_resp = requests.post(
            'https://id.twitch.tv/oauth2/token',
            params={
                'client_id':     IGDB_CLIENT_ID,
                'client_secret': IGDB_CLIENT_SECRET,
                'grant_type':    'client_credentials'
            }
        )
        if token_resp.status_code != 200:
            self.stderr.write('❌ Error al obtener token IGDB')
            return

        token = token_resp.json()['access_token']

        headers = {
            'Client-ID':     IGDB_CLIENT_ID,
            'Authorization': f'Bearer {token}'
        }

        igdb_query = 'fields id,name,summary,cover.url; limit 50;'
        r = requests.post('https://api.igdb.com/v4/games', headers=headers, data=igdb_query)

        if r.status_code != 200:
            self.stderr.write(f'❌ Error al consumir IGDB: {r.status_code}')
            return

        juegos_igdb = r.json()

        if len(juegos_igdb) < 25:
            self.stderr.write('❌ No se recibieron suficientes juegos')
            return

        for i in range(5):
            for j, categoria in enumerate(categorias):
                index = i + j * 5
                juego_igdb = juegos_igdb[index]
                titulo     = juego_igdb.get('name', f'Juego {index+1}')
                resumen    = juego_igdb.get('summary', '')[:200]
                cover_url  = ''
                if juego_igdb.get('cover'):
                    cover_url = juego_igdb['cover']['url'].replace('t_thumb', 't_cover_big')
                    cover_url = f'https:{cover_url}' if not cover_url.startswith('http') else cover_url

                Juego.objects.update_or_create(
                    titulo=titulo,
                    defaults={
                        'resumen': resumen,
                        'cover': cover_url,
                        'categoria': categoria
                    }
                )

        self.stdout.write(self.style.SUCCESS('✅ 25 juegos importados desde IGDB y asignados a categorías'))