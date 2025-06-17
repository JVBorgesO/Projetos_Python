import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

def get_coordinates(address, geolocator, retries=3):
    for _ in range(retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return pd.Series([location.latitude, location.longitude])
            else:
                return pd.Series([None, None])
        except (GeocoderTimedOut, GeocoderServiceError):
            time.sleep(1)
    return pd.Series([None, None])


arquivo_excel = 'enderecos_totais.xlsx'

coluna_endereco = 'endereco'

df = pd.read_excel(arquivo_excel)

# Inicializa o geolocalizador
geolocator = Nominatim(user_agent="geoapi_enderecos")

df[['Latitude', 'Longitude']] = df[coluna_endereco].apply(lambda x: get_coordinates(x, geolocator))

arquivo_saida = 'enderecos_com_coordenadas_totais.xlsx'
df.to_excel(arquivo_saida, index=False)

print(f'Arquivo gerado com sucesso: {arquivo_saida}')
