from supabase import create_client, Client
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
SUPABASE_URL = "https://ufrdpcuxhxyneykzaczt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmcmRwY3V4aHh5bmV5a3phY3p0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMyODQ2OTcsImV4cCI6MjA3ODg2MDY5N30.ewVZUh_M6Tp7KarKX1DLFaX8X1IJoFIY7aKPiDV8uMw"

def get_supabase() -> Client:
    """Получение клиента Supabase"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    """Инициализация базы данных - создание таблиц и заполнение начальными данными"""
    supabase = get_supabase()
    
    # Проверяем и заполняем жанры (расширенный список)
    genres = [
        'Action', 'Adventure', 'RPG', 'Strategy', 'Simulation', 
        'Sports', 'Racing', 'Puzzle', 'Horror', 'Fighting', 
        'Shooter', 'Platformer', 'Stealth', 'Survival', 
        'MMO', 'MOBA', 'Indie', 'Casual', 'Educational'
    ]
    
    for genre_name in genres:
        # Проверяем, существует ли жанр
        existing = supabase.table('genres').select('id').eq('name', genre_name).execute()
        if not existing.data:
            supabase.table('genres').insert({'name': genre_name}).execute()
    
    # Получаем ID жанров для заполнения игр
    genres_data = supabase.table('genres').select('id, name').execute()
    genre_map = {g['name']: g['id'] for g in genres_data.data}
    
    # Заполнение начальными данными (игры с несколькими жанрами)
    # Формат: (title, developer, publisher, release_year, description, [список жанров])
    sample_games = [
        ('The Witcher 3: Wild Hunt', 'CD Projekt RED', 'CD Projekt', 2015, 'Epic fantasy RPG', ['RPG', 'Action', 'Adventure']),
        ('Grand Theft Auto V', 'Rockstar North', 'Rockstar Games', 2013, 'Open-world action', ['Action', 'Adventure']),
        ('Minecraft', 'Mojang Studios', 'Mojang Studios', 2011, 'Sandbox survival', ['Adventure', 'Survival', 'Indie']),
        ('Counter-Strike: Global Offensive', 'Valve', 'Valve', 2012, 'Tactical shooter', ['Shooter', 'Action']),
        ('The Elder Scrolls V: Skyrim', 'Bethesda Game Studios', 'Bethesda Softworks', 2011, 'Fantasy RPG', ['RPG', 'Action', 'Adventure']),
        ('FIFA 23', 'EA Sports', 'Electronic Arts', 2022, 'Football simulation', ['Sports', 'Simulation']),
        ('Civilization VI', 'Firaxis Games', '2K Games', 2016, 'Turn-based strategy', ['Strategy', 'Simulation']),
        ('Portal 2', 'Valve', 'Valve', 2011, 'Puzzle-platformer', ['Puzzle', 'Platformer', 'Indie']),
        ('Resident Evil 4', 'Capcom', 'Capcom', 2023, 'Survival horror', ['Horror', 'Action', 'Survival']),
        ('Street Fighter 6', 'Capcom', 'Capcom', 2023, 'Fighting game', ['Fighting', 'Action']),
        ('Red Dead Redemption 2', 'Rockstar Games', 'Rockstar Games', 2018, 'Western action-adventure', ['Action', 'Adventure', 'Simulation']),
        ('Baldur\'s Gate 3', 'Larian Studios', 'Larian Studios', 2023, 'Dungeons & Dragons RPG', ['RPG', 'Strategy', 'Adventure']),
        ('Cyberpunk 2077', 'CD Projekt RED', 'CD Projekt', 2020, 'Sci-fi action RPG', ['RPG', 'Action', 'Adventure']),
        ('The Last of Us Part I', 'Naughty Dog', 'Sony Interactive Entertainment', 2022, 'Post-apocalyptic action-adventure', ['Action', 'Adventure', 'Horror']),
        ('God of War', 'Santa Monica Studio', 'Sony Interactive Entertainment', 2018, 'Action-adventure', ['Action', 'Adventure', 'RPG']),
    ]
    
    for game in sample_games:
        title, developer, publisher, release_year, description, genre_names = game
        
        # Проверяем, существует ли игра
        existing = supabase.table('games').select('id').eq('title', title).execute()
        
        if not existing.data:
            # Создаем игру
            game_result = supabase.table('games').insert({
                'title': title,
                'developer': developer,
                'publisher': publisher,
                'release_year': release_year,
                'description': description
            }).execute()
            
            if game_result.data:
                game_id = game_result.data[0]['id']
                
                # Добавляем жанры для игры
                for genre_name in genre_names:
                    genre_id = genre_map.get(genre_name)
                    if genre_id:
                        # Проверяем, не добавлен ли уже этот жанр
                        existing_genre = supabase.table('game_genres').select('id').eq('game_id', game_id).eq('genre_id', genre_id).execute()
                        if not existing_genre.data:
                            supabase.table('game_genres').insert({
                                'game_id': game_id,
                                'genre_id': genre_id
                            }).execute()

def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Проверка пароля"""
    return hash_password(password) == password_hash
