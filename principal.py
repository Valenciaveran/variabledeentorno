import requests
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional


class EnvironmentLoader:
    """Carga las variables de entorno necesarias."""
    @staticmethod
    def load() -> None:
        load_dotenv()

    @staticmethod
    def get_env_variable(key: str) -> Optional[str]:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"La variable de entorno '{key}' no está definida.")
        return value


class GoogleSearchClient:
    """Cliente para interactuar con la API de Google Custom Search."""
    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, api_key: str, search_engine_id: str):
        self.api_key = api_key
        self.search_engine_id = search_engine_id

    def search(self, query: str, start: int = 1, language: str = "lang_es") -> List[Dict]:
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start,
            "lr": language
        }
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la solicitud: {e}")
            return []


class SearchPresenter:
    """Presenta los resultados de la búsqueda al usuario."""
    @staticmethod
    def show_results(results: List[Dict]) -> None:
        if not results:
            print("⚠️  No se encontraron resultados.")
            return

        print("\n🔍 Resultados encontrados:\n")
        for idx, item in enumerate(results, start=1):
            title = item.get('title', 'Sin título')
            link = item.get('link', 'Sin enlace')
            snippet = item.get('snippet', 'Sin descripción')

            print(f"{idx}. 📌 {title}")
            print(f"   🔗 {link}")
            print(f"   📝 {snippet}")
            print("-" * 80)


def main():
    try:
        # Cargar variables de entorno
        EnvironmentLoader.load()
        api_key = EnvironmentLoader.get_env_variable("API_KEY_SEARCH_GOOGLE")
        search_engine_id = EnvironmentLoader.get_env_variable("SEARCH_ENGINE_ID")

        # Configurar búsqueda
        query = 'filetype:sql "MySQL dump" (pass|password|passwd|pwd)'
        start_page = 1
        language = "lang_es"

        # Ejecutar búsqueda
        client = GoogleSearchClient(api_key, search_engine_id)
        results = client.search(query=query, start=start_page, language=language)

        # Mostrar resultados
        SearchPresenter.show_results(results)

    except ValueError as ve:
        print(f"❗ Error de configuración: {ve}")
    except Exception as e:
        print(f"🔥 Error inesperado: {e}")


if __name__ == "__main__":
    main()
