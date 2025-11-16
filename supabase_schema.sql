-- SQL скрипт для создания таблиц в Supabase
-- Выполните этот скрипт в SQL Editor в Supabase Dashboard

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица жанров
CREATE TABLE IF NOT EXISTS genres (
    id BIGSERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Таблица игр (справочник) - БЕЗ genre_id
CREATE TABLE IF NOT EXISTS games (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    developer TEXT,
    publisher TEXT,
    release_year INTEGER,
    description TEXT
);

-- Таблица связи игр и жанров (many-to-many)
CREATE TABLE IF NOT EXISTS game_genres (
    id BIGSERIAL PRIMARY KEY,
    game_id BIGINT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    genre_id BIGINT NOT NULL REFERENCES genres(id) ON DELETE CASCADE,
    UNIQUE(game_id, genre_id)
);

-- Таблица коллекции пользователя (связь пользователь-игра)
CREATE TABLE IF NOT EXISTS user_games (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    game_id BIGINT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    hours_played REAL DEFAULT 0,
    status TEXT DEFAULT 'owned',
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, game_id)
);

-- Создание индексов для улучшения производительности
CREATE INDEX IF NOT EXISTS idx_user_games_user_id ON user_games(user_id);
CREATE INDEX IF NOT EXISTS idx_user_games_game_id ON user_games(game_id);
CREATE INDEX IF NOT EXISTS idx_game_genres_game_id ON game_genres(game_id);
CREATE INDEX IF NOT EXISTS idx_game_genres_genre_id ON game_genres(genre_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Включение Row Level Security (опционально, для безопасности)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE genres ENABLE ROW LEVEL SECURITY;
ALTER TABLE games ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_genres ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_games ENABLE ROW LEVEL SECURITY;

-- Политики безопасности (разрешаем все операции через API ключ)
-- Для production рекомендуется настроить более строгие политики
CREATE POLICY "Enable all operations for authenticated users" ON users
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Enable all operations for genres" ON genres
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Enable all operations for games" ON games
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Enable all operations for game_genres" ON game_genres
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Enable all operations for user_games" ON user_games
    FOR ALL USING (true) WITH CHECK (true);

-- Заполнение жанров
INSERT INTO genres (name) VALUES 
    ('Action'),
    ('Adventure'),
    ('RPG'),
    ('Strategy'),
    ('Simulation'),
    ('Sports'),
    ('Racing'),
    ('Puzzle'),
    ('Horror'),
    ('Fighting'),
    ('Shooter'),
    ('Platformer'),
    ('Stealth'),
    ('Survival'),
    ('MMO'),
    ('MOBA'),
    ('Indie'),
    ('Casual'),
    ('Educational')
ON CONFLICT (name) DO NOTHING;
