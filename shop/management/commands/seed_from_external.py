#seed_from_external.py

import os
import requests
from django.core.management.base import BaseCommand
from shop.models import Juego, Categoria

RAWG_API_KEY      = os.getenv('RAWG_API_KEY')
IGDB_CLIENT_ID    = os.getenv('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET= os.getenv('IGDB_CLIENT_SECRET')

class Command(BaseCommand):
    help = 'Trae juegos de RAWG y de IGDB y los guarda en la tabla Juego'

    def handle(self, *args, **options):
        # RAWG
        rawg_url = f'https://api.rawg.io/api/games?key={RAWG_API_KEY}&page_size=6'
        r1 = requests.get(rawg_url)
        if r1.status_code == 200:
            # ← Aquí empieza el bucle de RAWG
            for item in r1.json().get('results', []):
                titulo = item['name']
                resumen = item.get('description_raw', '')[:200]
                cover   = item.get('background_image', '')
                # 1) Determinar nombre de categoría
                if item.get('genres'):
                    genre_name = item['genres'][0]['name']   # toma el primer género
                else:
                    genre_name = 'Sin categoría'
                # 2) Buscar o crear esa categoría
                cat_obj, created = Categoria.objects.get_or_create(nombre=genre_name)
                # 3) Crear o actualizar el Juego con la categoría
                Juego.objects.update_or_create(
                    titulo=titulo,
                    defaults={
                        'resumen': item.get('description_raw', '')[:200],
                        'cover':   item.get('background_image', ''),
                        'categoria': cat_obj,
                    }
                )
            self.stdout.write(self.style.SUCCESS('✅ Datos de RAWG importados'))
        else:
            self.stderr.write(f'Error RAWG: {r1.status_code}')

        # IGDB
        token_resp = requests.post(
            'https://id.twitch.tv/oauth2/token',
            params={
                'client_id':     IGDB_CLIENT_ID,
                'client_secret': IGDB_CLIENT_SECRET,
                'grant_type':    'client_credentials'
            }
        )
        if token_resp.status_code != 200:
            self.stderr.write('Error al obtener token IGDB')
            return
        token = token_resp.json()['access_token']

        headers = {
            'Client-ID':     IGDB_CLIENT_ID,
            'Authorization': f'Bearer {token}'
        }
        igdb_query = 'fields id,name,summary,cover.url; limit 6;'
        r2 = requests.post('https://api.igdb.com/v4/games', headers=headers, data=igdb_query)
        if r2.status_code == 200:
            for item in r2.json():
                titulo = item.get('name','Sin título')
                cover_url = ''
                if item.get('cover'):
                    cover_url = item['cover']['url'].replace('t_thumb','t_cover_big')
                Juego.objects.update_or_create(
                    titulo=titulo,
                    defaults={
                        'resumen': item.get('summary','')[:200],
                        'cover':   cover_url,
                    }
                )
            self.stdout.write(self.style.SUCCESS('✅ Datos de IGDB importados'))
        else:
            self.stderr.write(f'Error IGDB: {r2.status_code}')