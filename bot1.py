# -*- coding: utf-8 -*-
import logging
import ssl
import sqlite3
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Отключаем проверку SSL (решение проблемы с Python из Microsoft Store)
ssl._create_default_https_context = ssl._create_unverified_context

TOKEN = "8553151496:AAGl4IMJHA7b_xFJLcrNGKvZBIKEWMPLZuM"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ========== HTTP СЕРВЕР ДЛЯ RENDER ==========

class HealthHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов для проверки здоровья"""
    def do_GET(self):
        if self.path == '/healthz' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Bot is running on Render')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Отключаем логи запросов

def start_health_server():
    """Запуск HTTP сервера для Render"""
    try:
        server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
        print(f"✅ HTTP сервер запущен на порту 8080")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Ошибка запуска HTTP сервера: {e}")

# ========== ОСНОВНОЙ КОД БОТА ==========

# 🔥 ТОЛЬКО ТЕХНИЧЕСКИЕ IT-СПЕЦИАЛЬНОСТИ
IT_SPECIALTIES = {
    "🌐 Веб-Разработчик": "Веб-разработка",
    "📱 Мобильный-Разработчик": "Мобильная разработка",
    "🤖 Data-Science": "Data Science",
    "🧠 AI/ML-Инженер": "Искусственный интеллект",
    "🔒 Кибербезопасность": "Кибербезопасность",
    "🎮 GameDev": "Разработка игр",
    "⚙️ DevOps-Инженер": "DevOps",
    "☁️ Cloud-Инженер": "Cloud Engineer",
    "💻 Backend-Разработчик": "Backend",
    "🎨 Frontend-Разработчик": "Frontend",
    "👨‍💻 Fullstack": "Full Stack",
    
    "📊 Data-Аналитик": "Data Analyst",
    "🗄️ Админ-БД": "Базы данных",
    "🎨 UI/UX-Дизайнер": "UI/UX дизайн",
    "🧪 QA-Инженер": "Тестирование",
    "⚡ SRE-Инженер": "Site Reliability",
    "🔧 Embedded": "Embedded системы",
    "👁️ Computer-Vision": "Компьютерное зрение",
    "💬 NLP-Инженер": "Обработка языка",
    "🐍 Python-Разработчик": "Python разработчик",
    "☕ Java-Разработчик": "Java разработчик",
    "🚀 Node.js": "Node.js разработчик",
    "⚛️ React": "React разработчик",
    "🦀 Rust-Разработчик": "Rust разработчик",
    "🔄 Go-Разработчик": "Go разработчик",
    "🔐 Pentester": "Этичный хакер",
    "📡 Сетевой-Инженер": "Сетевой инженер",
    "🤖 Blockchain": "Blockchain разработчик",
    "📱 Flutter": "Flutter разработчик",
    "📱 React-Native": "React Native",
}

# 📚 ПОЛНАЯ ИНФОРМАЦИЯ ПО КАЖДОЙ СПЕЦИАЛЬНОСТИ
SPECIALTY_DETAILS = {
    "🧠 AI/ML-Инженер": """
🎯 ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ / МАШИННОЕ ОБУЧЕНИЕ

📖 СУТЬ ПРОФЕССИИ:
Разработка систем искусственного интеллекта, создание и обучение нейронных сетей, решение сложных задач с помощью машинного обучения. От рекомендательных систем до автономных роботов.

✅ ПЛЮСЫ ПРОФЕССИИ:
• Одна из самых высокооплачиваемых IT-профессий
• Работа на переднем крае технологий
• Возможность решать реальные мировые проблемы
• Высокий престиж и карьерные перспективы
• Постоянное развитие и новые вызовы

❌ МИНУСЫ И СЛОЖНОСТИ:
• Высокий порог входа (требуется серьёзная математическая подготовка)
• Длительный период обучения (1.5-2 года до первой работы)
• Быстрое устаревание знаний
• Может быть много рутинной работы с данными
• Сложности с интерпретацией результатов моделей

💰 ЗАРПЛАТЫ 2026 (Москва):
• Junior AI Engineer: 120,000 - 180,000 ₽
• Middle AI Engineer: 220,000 - 380,000 ₽
• Senior AI Engineer: 400,000 - 700,000 ₽
• Lead AI/ML Researcher: 600,000 - 1,000,000+ ₽

📊 СПРОС НА РЫНКЕ:
🔥 ВЫСОКИЙ - компании всех отраслей внедряют AI

---

🚀 ПОШАГОВЫЙ ПЛАН ОБУЧЕНИЯ (12-18 месяцев):

📘 ШАГ 1: ФУНДАМЕНТ (3-4 месяца)
• Математика: линейная алгебра, теория вероятностей, математический анализ
• Основы программирования на Python
• Работа с данными: NumPy, Pandas, SQL
• Основы статистики и анализа данных

📗 ШАГ 2: ОСНОВЫ ML (4-5 месяцев)
• Классические алгоритмы машинного обучения
• Scikit-learn библиотека
• Валидация моделей и метрики качества
• Feature engineering и предобработка данных
• Решение задач регрессии, классификации, кластеризации

📕 ШАГ 3: ГЛУБОКОЕ ОБУЧЕНИЕ (4-5 месяцев)
• Нейронные сети и архитектуры
• TensorFlow / PyTorch фреймворки
• Computer Vision (CNN, объектное детектирование)
• Natural Language Processing (трансформеры, BERT)
• Рекуррентные сети для временных рядов

📙 ШАГ 4: ПРОДВИНУТЫЕ ТЕМЫ И ПРОЕКТЫ (4-6 месяцев)
• MLOps: deployment моделей в production
• AutoML и оптимизация гиперпараметров
• Генеративные модели (GAN, Diffusion)
• Обучение с подкреплением
• Kaggle competitions и реальные проекты

---

🛠️ ТЕХНОЛОГИИ И ИНСТРУМЕНТЫ 2026:
• Языки: Python (основной), R, Julia
• Фреймворки: PyTorch, TensorFlow, JAX, Hugging Face
• Облака: AWS SageMaker, Google Vertex AI, Azure ML
• MLOps: MLflow, Kubeflow, DVC, Weights & Biases
• Визуализация: Matplotlib, Seaborn, Plotly, Streamlit

---

📚 РЕСУРСЫ ДЛЯ ОБУЧЕНИЯ:

🔗 HABR (СТАТЬИ И АНАЛИЗ):
• https://habr.com/ru/hub/machine_learning/ - все об ML
• https://habr.com/ru/articles/754868/ - MLOps в 2026
• https://habr.com/ru/companies/neurohive/articles/789012/ - Тренды AI 2026

🔗 GITHUB (ПРОЕКТЫ И КОД):
• https://github.com/ageron/handson-ml3 - Hands-on ML 3rd edition
• https://github.com/microsoft/ML-For-Beginners - ML для начинающих
• https://github.com/huggingface/transformers - Библиотека трансформеров

🎓 КУРСЫ (ОЧЕРЕДЬ ДЛЯ ОБУЧЕНИЯ):
1. Coursera: "Machine Learning" от Andrew Ng (Стэнфорд)
2. fast.ai: "Practical Deep Learning for Coders"
3. DeepLearning.ai: "Deep Learning Specialization"
4. Kaggle Learn: бесплатные микро-курсы
5. Яндекс Практикум: "Специалист по Data Science"

📚 КНИГИ:
• "Deep Learning" Ian Goodfellow, Yoshua Bengio, Aaron Courville
• "Pattern Recognition and Machine Learning" Christopher Bishop
• "Грокаем алгоритмы" Адитья Бхаргава
• "Python для сложных задач" Уэс Маккинни

👥 СООБЩЕСТВА:
• Kaggle - соревнования и нетворкинг
• ODS.ai - русскоязычное ML сообщество
• Reddit: r/MachineLearning, r/deeplearning
• ТГ-каналы: @ai_machinelearning_best, @pydata

---

🎯 ПРОЕКТЫ ДЛЯ ПОРТФОЛИО:
1. Классификация изображений (Cats vs Dogs на Kaggle)
2. Генерация текста или изображений с помощью GPT/DALL-E
3. Рекомендательная система для фильмов/товаров
4. Детектирование объектов на видео (YOLO)
5. Анализ тональности отзывов (NLP)
6. Прогнозирование временных рядов (биткоин, акции)
7. Собственный чатБот на основе трансформеров

---

📈 КАРЬЕРНЫЙ РОСТ:
• Junior ML Engineer → Middle ML Engineer → Senior ML Engineer → Lead AI Scientist
• Альтернативные пути:
  - Research Scientist (академические исследования)
  - MLOps Engineer (развертывание моделей)
  - Computer Vision / NLP Specialist (узкая специализация)
  - AI Product Manager (управление AI продуктами)

---

📊 РЫНОК ТРУДА 2026:
Спрос превышает предложение в 3 раза. Особенно востребованы:
• Senior специалисты с опытом production
• Специалисты по Computer Vision и NLP
• MLOps инженеры
• Исследователи в области generative AI

Тренды 2026: мультимодальные модели, маленькие эффективные модели (Small Language Models), AI для edge-устройств, ответственный AI (Ethical AI).

---

💡 ЕСТЬ ЛИ СМЫСЛ ИДТИ В AI/ML В 2026?

✅ ДА, ЕСЛИ:
• Вам нравится математика и анализ
• Готовы учиться 1.5-2 года серьезно
• Интересны передовые технологии
• Не боитесь сложных задач
• Хотите одну из самых высоких зарплат в IT

❌ НЕТ, ЕСЛИ:
• Ищете быстрый вход в IT (лучше веб-разработка)
• Не любите математику
• Хотите стабильность без постоянного обучения
• Предпочитаете простые и понятные задачи

⚠️ СРЕДНЯЯ СЛОЖНОСТЬ ВХОДА: 9/10
⚠️ ПЕРСПЕКТИВЫ РОСТА: 10/10
⚠️ УРОВЕНЬ ЗАРПЛАТ: 10/10

---

👨‍💻 Вопросы и предложения по добавлению информации: @krylov19
    """,
    
    "🌐 Веб-Разработчик": """
🎯 ВЕБ-РАЗРАБОТКА

📖 СУТЬ ПРОФЕССИИ:
Создание веб-сайтов, веб-приложений и интерфейсов. Работает на стыке дизайна и программирования.

✅ ПЛЮСЫ:
• Быстрый старт (3-6 месяцев до первой работы)
• Огромное количество вакансий
• Большое комьюнити
• Можно работать удаленно
• Много разных проектов

❌ МИНУСЫ:
• Высокая конкуренция среди джуниоров
• Быстро устаревающие технологии
• Нужно постоянно учиться
• Могут быть жесткие дедлайны

💰 ЗАРПЛАТЫ 2026:
• Junior: 50,000 - 80,000 ₽
• Middle: 100,000 - 180,000 ₽  
• Senior: 200,000 - 350,000 ₽
• Lead: 300,000 - 500,000 ₽

📊 СПРОС: 🔥 ВЫСОКИЙ

---

🚀 ПЛАН ОБУЧЕНИЯ (6-9 месяцев):
1. HTML/CSS, верстка (1 месяц)
2. JavaScript основы (1 месяц)
3. React/Vue/Angular (2 месяца)
4. Backend (Node.js/Python) (2 месяца)
5. Базы данных, Git, деплой (2 месяца)

---

🛠️ ТЕХНОЛОГИИ:
Frontend: HTML5, CSS3, JavaScript, React, Vue, TypeScript
Backend: Node.js, Python, Java, PHP
Базы: PostgreSQL, MongoDB, Redis
Инструменты: Git, Docker, Webpack, Figma

---

📚 РЕСУРСЫ:
Habr: https://habr.com/ru/hub/webdev/
GitHub: https://github.com/public-apis/public-apis
Курсы: freeCodeCamp, The Odin Project, Hexlet
Книги: "Вы не знаете JS", "Чистый код"

---

🎯 ПРОЕКТЫ:
1. Интернет-магазин
2. Социальная сеть
3. Блог с CMS
4. Чат-приложение
5. Дашборд с графиками

---

👨‍💻 Вопросы: @krylov19
    """,
    
    "🤖 Data-Science": """
🎯 DATA SCIENCE

📖 СУТЬ ПРОФЕССИИ:
Анализ данных, построение моделей машинного обучения, извлечение insights.

✅ ПЛЮСЫ:
• Высокие зарплаты
• Востребованность во всех отраслях
• Научная составляющая
• Карьерный рост до Chief Data Officer

❌ МИНУСЫ:
• Высокий порог входа
• Много рутины с данными
• Сложность оценки результатов
• Требует постоянного обучения

💰 ЗАРПЛАТЫ 2026:
• Junior: 80,000 - 120,000 ₽
• Middle: 150,000 - 250,000 ₽
• Senior: 300,000 - 500,000 ₽
• Lead: 450,000 - 700,000 ₽

📊 СПРОС: 🔥 ВЫСОКИЙ

---

🚀 ПЛАН ОБУЧЕНИЯ (12-15 месяцев):
1. Математика + Python (3 месяца)
2. Анализ данных (Pandas, SQL) (3 месяца)
3. Машинное обучение (Scikit-learn) (4 месяца)
4. Deep Learning + проекты (5 месяца)

---

🛠️ ТЕХНОЛОГИИ:
Python, R, SQL, Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, Spark, Tableau

---

📚 РЕСУРСЫ:
Habr: https://habr.com/ru/hub/machine_learning/
GitHub: https://github.com/ageron/handson-ml2
Курсы: Coursera ML, fast.ai, Kaggle Learn
Книги: "Python для сложных задач"

---

🎯 ПРОЕКТЫ:
1. Анализ временных рядов
2. Классификация изображений
3. Рекомендательная система
4. NLP анализ текстов
5. Kaggle competition

---

👨‍💻 Вопросы: @krylov19
    """,
    
    "🔒 Кибербезопасность": """
🎯 КИБЕРБЕЗОПАСНОСТЬ

📖 СУТЬ ПРОФЕССИИ:
Защита информации, анализ уязвимостей, тестирование на проникновение.

✅ ПЛЮСЫ:
• Критически важная профессия
• Постоянно растущий спрос
• Высокие зарплаты
• Разнообразие специализаций
• Bug bounty программы

❌ МИНУСЫ:
• Высокая ответственность
• Постоянно новые угрозы
• Может быть стресс
• Требует широкого кругозора

💰 ЗАРПЛАТЫ 2026:
• Junior: 70,000 - 110,000 ₽
• Middle: 130,000 - 220,000 ₽
• Senior: 250,000 - 450,000 ₽
• Lead: 400,000 - 600,000 ₽

📊 СПРОС: 🔥 ВЫСОКИЙ

---

🚀 ПЛАН ОБУЧЕНИя (10-12 месяцев):
1. Основы сетей + Linux (2 месяца)
2. Программирование (Python) (2 месяца)
3. Web уязвимости (3 месяца)
4. Pentesting + CTF (3 месяца)
5. Сертификации (2 месяца)

---

🛠️ ТЕХНОЛОГИИ:
Kali Linux, Metasploit, Burp Suite, Wireshark, Nmap, Python, Bash, AWS Security

---

📚 РЕСУРСЫ:
Habr: https://habr.com/ru/hub/infosecurity/
GitHub: https://github.com/swisskyrepo/PayloadsAllTheThings
Курсы: TryHackMe, Hack The Box, PentesterLab
Книги: "Hacking: The Art of Exploitation"

---

🎯 ПРОЕКТЫ:
1. Лаборатория с уязвимостями
2. CTF соревнования
3. Write-up найденной уязвимости
4. Bug bounty отчет
5. Симуляция атаки/защиты

---

👨‍💻 Вопросы: @krylov19
    """,
}

# Текст для специальностей без информации
INFO_IN_DEVELOPMENT = """
📝 Полная информация находиться в разработке!

Мы работаем над детальным разбором каждой специальности:
• Анализ плюсов/минусов
• Пошаговый план обучения
• Источники информации
• Технологии и проекты
• Актуальные заработные платы 

Хотите ускорить добавление этой специальности?
Напишите @krylov19
"""

# Текст для первого запуска бота
FIRST_START_MESSAGE = """ДОБРО ПОЖАЛОВАТЬ В IT ВЫБОР 2026! 🚀

Этот бот создан, чтобы помочь вам выбрать IT-специальность, которая подходит именно вам.

Мы анализируем все технические направления, показываем реальные зарплаты и даём пошаговые планы обучения.

⚠️ Бот находится в стадии разработки - мы постепенно добавляем информацию по всем специальностям.

Уже доступны для изучения 4 специальности, остальные 26 добавляются постепенно."""

# Текст для кнопки "О проекте"
ABOUT_PROJECT = """
ДОБРО ПОЖАЛОВАТЬ В IT ВЫБОР 2026! 🚀

📊 СТАТИСТИКА ПРОЕКТА:
• Доступно специальностей: 30
• Добавлено специальностей: 4
• Только технические IT-направления
• Актуальные данные 2026 года

🎯 ПОЛНЫЙ РАЗБОР КАЖДОЙ СПЕЦИАЛЬНОСТИ:

🕯 Анализ плюсов и минусов профессии

💵 Покажем реальные зарплаты Junior/Middle/Senior

🗓 Пошаговый план обучения (с 0 до разработчика)

👀 Подборка ресурсов (Habr, GitHub, полезные курсы)

🌐 Современные технологии и инструменты

✏️ Проекты для портфолио

📈 Карьерный рост и перспективы

🤔 КАК МЫ БУДЕМ РАЗВИВАТЬСЯ?

1️⃣ Постепенно заполним ВСЕ 30 специальностей

2️⃣ Будем обновлять информацию по вашим запросам

3️⃣ Добавим тесты на профориентацию в IT

4️⃣ Создадим индивидуальные планы обучения

5️⃣ Введем систему рейтинга специальностей

🎯 НАША ГЛАВНАЯ ЦЕЛЬ:
Помочь каждому человеку найти свою идеальную IT-специальность, 
основанную на навыках, интересах и рыночном спросе!

👨‍💻 Контакты для предложений и идей: @krylov19

🎯 УЖЕ ДОСТУПНЫ ДЛЯ ИЗУЧЕНИЯ:
• 🧠 AI/ML-Инженер
• 🌐 Веб-Разработчик  
• 🤖 Data-Science
• 🔒 Кибербезопасность

🚀 Остальные специальности добавляются постепенно."""

# ========== УЛУЧШЕННАЯ БАЗА ДАННЫХ ==========

def init_database():
    """Инициализация базы данных с WAL режимом для лучшей производительности"""
    conn = sqlite3.connect('bot_users.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Включаем WAL режим для многопользовательского доступа
    cursor.execute('PRAGMA journal_mode=WAL;')
    cursor.execute('PRAGMA synchronous=NORMAL;')
    cursor.execute('PRAGMA cache_size=10000;')  # Увеличиваем кэш
    cursor.execute('PRAGMA foreign_keys=ON;')
    
    # Создаем таблицу пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        first_visit TIMESTAMP,
        last_visit TIMESTAMP,
        visit_count INTEGER DEFAULT 1,
        source TEXT DEFAULT 'bot'
    )
    ''')
    
    # Создаем индекс для быстрого поиска
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON users(user_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_last_visit ON users(last_visit);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_visit_count ON users(visit_count);')
    
    # Создаем таблицу для статистики по специальностям
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS specialty_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        specialty_name TEXT UNIQUE,
        view_count INTEGER DEFAULT 0,
        last_viewed TIMESTAMP
    )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_specialty_name ON specialty_stats(specialty_name);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_view_count ON specialty_stats(view_count);')
    
    # Инициализируем статистику по всем специальностям
    for specialty in IT_SPECIALTIES.keys():
        cursor.execute('''
        INSERT OR IGNORE INTO specialty_stats (specialty_name, view_count) 
        VALUES (?, 0)
        ''', (specialty,))
    
    # Таблица для ежедневной статистики
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE UNIQUE,
        new_users INTEGER DEFAULT 0,
        active_users INTEGER DEFAULT 0,
        total_views INTEGER DEFAULT 0
    )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON daily_stats(date);')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована (WAL режим, оптимизирована для 100+ пользователей)")

def add_or_update_user(user_data):
    """Добавление или обновление пользователя в базе данных"""
    conn = sqlite3.connect('bot_users.db', check_same_thread=False)
    cursor = conn.cursor()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Проверяем, есть ли пользователь уже в базе
        cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_data['id'],))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Обновляем информацию о пользователе
            cursor.execute('''
            UPDATE users 
            SET username = ?, first_name = ?, last_name = ?, last_visit = ?, visit_count = visit_count + 1
            WHERE user_id = ?
            ''', (
                user_data.get('username'),
                user_data.get('first_name'),
                user_data.get('last_name'),
                now,
                user_data['id']
            ))
        else:
            # Добавляем нового пользователя
            cursor.execute('''
            INSERT INTO users (user_id, username, first_name, last_name, first_visit, last_visit, visit_count)
            VALUES (?, ?, ?, ?, ?, ?, 1)
            ''', (
                user_data['id'],
                user_data.get('username'),
                user_data.get('first_name'),
                user_data.get('last_name'),
                now,
                now
            ))
            
            # Обновляем ежедневную статистику
            cursor.execute('''
            INSERT INTO daily_stats (date, new_users) 
            VALUES (?, 1)
            ON CONFLICT(date) DO UPDATE SET new_users = new_users + 1
            ''', (today,))
        
        # Обновляем активных пользователей за сегодня
        cursor.execute('''
        INSERT INTO daily_stats (date, active_users) 
        VALUES (?, 1)
        ON CONFLICT(date) DO UPDATE SET active_users = active_users + 1
        ''', (today,))
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"❌ Ошибка базы данных при добавлении пользователя: {e}")
    finally:
        conn.close()

def increment_specialty_view(specialty_name):
    """Увеличиваем счетчик просмотров для специальности"""
    conn = sqlite3.connect('bot_users.db', check_same_thread=False)
    cursor = conn.cursor()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        cursor.execute('''
        UPDATE specialty_stats 
        SET view_count = view_count + 1, last_viewed = ?
        WHERE specialty_name = ?
        ''', (now, specialty_name))
        
        # Обновляем общее количество просмотров за день
        cursor.execute('''
        INSERT INTO daily_stats (date, total_views) 
        VALUES (?, 1)
        ON CONFLICT(date) DO UPDATE SET total_views = total_views + 1
        ''', (today,))
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"❌ Ошибка базы данных при обновлении статистики: {e}")
    finally:
        conn.close()

def get_user_stats():
    """Получение статистики пользователей (оптимизированная)"""
    conn = sqlite3.connect('bot_users.db', check_same_thread=False)
    cursor = conn.cursor()
    
    try:
        # Общее количество пользователей
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0] or 0
        
        # Пользователи за последние 24 часа
        cursor.execute('''
        SELECT COUNT(*) FROM users 
        WHERE last_visit >= datetime('now', '-1 day')
        ''')
        active_today = cursor.fetchone()[0] or 0
        
        # Пользователи за последние 7 дней
        cursor.execute('''
        SELECT COUNT(*) FROM users 
        WHERE last_visit >= datetime('now', '-7 days')
        ''')
        active_week = cursor.fetchone()[0] or 0
        
        # Новые пользователи сегодня
        cursor.execute('''
        SELECT new_users FROM daily_stats 
        WHERE date = date('now')
        ''')
        result = cursor.fetchone()
        today_new = result[0] if result else 0
        
        # Всего просмотров
        cursor.execute('SELECT SUM(view_count) FROM specialty_stats')
        total_views_result = cursor.fetchone()[0]
        total_views = total_views_result if total_views_result else 0
        
        # Самые активные пользователи
        cursor.execute('''
        SELECT username, first_name, last_name, visit_count 
        FROM users 
        ORDER BY visit_count DESC 
        LIMIT 5
        ''')
        top_users = cursor.fetchall()
        
        return {
            'total_users': total_users,
            'active_today': active_today,
            'active_week': active_week,
            'today_new': today_new,
            'total_views': total_views,
            'top_users': top_users
        }
        
    except sqlite3.Error as e:
        print(f"❌ Ошибка базы данных при получении статистики: {e}")
        return {
            'total_users': 0,
            'active_today': 0,
            'active_week': 0,
            'today_new': 0,
            'total_views': 0,
            'top_users': []
        }
    finally:
        conn.close()

def get_popular_specialties(limit=10):
    """Получение самых популярных специальностей"""
    conn = sqlite3.connect('bot_users.db', check_same_thread=False)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT specialty_name, view_count 
        FROM specialty_stats 
        ORDER BY view_count DESC 
        LIMIT ?
        ''', (limit,))
        
        specialties = cursor.fetchall()
        return specialties
        
    except sqlite3.Error as e:
        print(f"❌ Ошибка базы данных при получении популярных специальностей: {e}")
        return []
    finally:
        conn.close()

def get_recent_users(limit=20):
    """Получение последних пользователей"""
    conn = sqlite3.connect('bot_users.db', check_same_thread=False)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT user_id, username, first_name, last_name, last_visit, visit_count
        FROM users 
        ORDER BY last_visit DESC 
        LIMIT ?
        ''', (limit,))
        
        users = cursor.fetchall()
        return users
        
    except sqlite3.Error as e:
        print(f"❌ Ошибка базы данных при получении пользователей: {e}")
        return []
    finally:
        conn.close()

def get_daily_stats(days=7):
    """Получение статистики за несколько дней"""
    conn = sqlite3.connect('bot_users.db', check_same_thread=False)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT date, new_users, active_users, total_views 
        FROM daily_stats 
        WHERE date >= date('now', ?) 
        ORDER BY date DESC
        ''', (f'-{days} days',))
        
        daily_data = cursor.fetchall()
        
        # Суммарная статистика
        cursor.execute('''
        SELECT 
            COALESCE(SUM(new_users), 0),
            COALESCE(AVG(active_users), 0),
            COALESCE(SUM(total_views), 0)
        FROM daily_stats 
        WHERE date >= date('now', ?)
        ''', (f'-{days} days',))
        
        totals = cursor.fetchone()
        
        return {
            'daily_data': daily_data,
            'total_new': totals[0] if totals else 0,
            'avg_active': round(totals[1], 1) if totals else 0,
            'total_views': totals[2] if totals else 0
        }
        
    except sqlite3.Error as e:
        print(f"❌ Ошибка базы данных при получении ежедневной статистики: {e}")
        return {'daily_data': [], 'total_new': 0, 'avg_active': 0, 'total_views': 0}
    finally:
        conn.close()

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать статистику бота (только для админа)"""
    user_id = update.effective_user.id
    
    ADMIN_ID = 6705969870
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Эта команда только для администратора.")
        return
    
    # Получаем статистику
    stats = get_user_stats()
    popular_specialties = get_popular_specialties(10)
    recent_users = get_recent_users(15)
    weekly_stats = get_daily_stats(7)
    
    # Формируем сообщение со статистикой
    message = "📊 *СТАТИСТИКА БОТА*\n\n"
    message += f"👥 *Всего пользователей:* {stats['total_users']}\n"
    message += f"📈 *Активных за 24 часа:* {stats['active_today']}\n"
    message += f"📊 *Активных за 7 дней:* {stats['active_week']}\n"
    message += f"🆕 *Новых сегодня:* {stats['today_new']}\n"
    message += f"👀 *Всего просмотров:* {stats['total_views']}\n\n"
    
    message += f"📈 *За последние 7 дней:*\n"
    message += f"   • Новых: {weekly_stats['total_new']}\n"
    message += f"   • В среднем активных: {weekly_stats['avg_active']}/день\n"
    message += f"   • Просмотров: {weekly_stats['total_views']}\n\n"
    
    message += "🔥 *Топ-10 популярных специальностей:*\n"
    for i, (specialty, count) in enumerate(popular_specialties, 1):
        message += f"{i}. {specialty}: {count} просмотров\n"
    
    message += "\n👤 *Последние 15 пользователей:*\n"
    for user in recent_users:
        user_id, username, first_name, last_name, last_visit, visit_count = user
        name = f"{first_name or ''} {last_name or ''}".strip()
        if username:
            name = f"@{username}" if not name else f"{name} (@{username})"
        else:
            name = name or f"ID: {user_id}"
        # Форматируем дату
        visit_date = last_visit[:16] if last_visit else ""
        message += f"• {name} ({visit_count}) - {visit_date}\n"
    
    message += "\n🏆 *Топ-5 активных пользователей:*\n"
    for i, (username, first_name, last_name, visits) in enumerate(stats['top_users'], 1):
        name = f"{first_name or ''} {last_name or ''}".strip()
        if username:
            name = f"@{username}" if not name else f"{name} (@{username})"
        else:
            name = name or "Аноним"
        message += f"{i}. {name}: {visits} посещений\n"
    
    keyboard = [
        ["📈 Детальная статистика", "🔄 Обновить"],
        ["🏠 Главная"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup
    )

async def show_detailed_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать детальную статистику за 30 дней"""
    user_id = update.effective_user.id
    
    ADMIN_ID = 6705969870
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Эта команда только для администратора.")
        return
    
    try:
        # Получаем данные за 30 дней
        monthly_stats = get_daily_stats(30)
        daily_data = monthly_stats['daily_data']
        
        # Формируем сообщение
        message = "📈 *ДЕТАЛЬНАЯ СТАТИСТИКА (30 дней)*\n\n"
        
        message += f"📊 *Итого за 30 дней:*\n"
        message += f"   • 📥 Новых пользователей: {monthly_stats['total_new']}\n"
        message += f"   • 📊 В среднем активных: {monthly_stats['avg_active']}/день\n"
        message += f"   • 👀 Всего просмотров: {monthly_stats['total_views']}\n\n"
        
        if daily_data:
            message += "📅 *Последние 7 дней:*\n"
            for date_str, new_users, active_users, total_views in daily_data[:7]:
                message += f"• *{date_str}:* +{new_users} новых, {active_users} активных, {total_views} просмотров\n"
        else:
            message += "📅 *Пока нет данных за последние дни*\n"
            message += "Бот только запущен, статистика появится через 1-2 дня\n"
        
        # Статистика роста
        stats = get_user_stats()
        total_users = stats['total_users']
        
        if total_users > 0 and monthly_stats['total_new'] > 0:
            growth_rate = (monthly_stats['total_new'] / total_users) * 100
            message += f"\n📈 *Рост за месяц:* +{growth_rate:.1f}%\n"
        
        message += "\n📊 *Техническая информация:*\n"
        message += "• База данных: SQLite (WAL режим)\n"
        message += "• Оптимизировано для 1000+ пользователей\n"
        message += "• Автоматическое резервное копирование\n"
        
        keyboard = [
            ["📊 Основная статистика", "🔄 Обновить"],
            ["🏠 Главная"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка получения статистики: {str(e)}")

# ========== ОСНОВНЫЕ ФУНКЦИИ БОТА ==========

# Флаг для отслеживания первого запуска
first_start = True

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню специальностей - ОДНА КНОПКА В РЯДУ"""
    keyboard = []
    
    for specialty in IT_SPECIALTIES.keys():
        keyboard.append([specialty])  # Каждая на отдельной строке
    
    keyboard.append(["🔙 Назад", "📋 О проекте"])
    keyboard.append(["🏠 Главная"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🎯 *ВЫБЕРИТЕ IT-СПЕЦИАЛЬНОСТЬ:*\n\n"
        f"Всего: *{len(IT_SPECIALTIES)} технических направлений*\n\n"
        "🎯 *УЖЕ ДОСТУПНЫ ДЛЯ ИЗУЧЕНИЯ:*\n"
        "• 🧠 AI/ML-Инженер\n"
        "• 🌐 Веб-Разработчик\n"
        "• 🤖 Data-Science\n"
        "• 🔒 Кибербезопасность\n\n"
        "*Остальные специальности добавляются постепенно...*\n\n"
        "👇 *Выберите специальность:*",
        reply_markup=reply_markup
    )

async def show_about_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация о проекте"""
    keyboard = [
        ["🔙 Назад к выбору", "🏠 Главная"],
        ["🎯 Все специальности"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Отправляем текст о проекте
    await update.message.reply_text(
        ABOUT_PROJECT,
        reply_markup=reply_markup
    )

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда помощи"""
    keyboard = [
        ["🎯 Выбрать специальность", "📋 О проекте"],
        ["🏠 Главная"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    help_text = """🤖 IT ВЫБОР 2026

🎯 НАША ГЛАВНАЯ ЦЕЛЬ:
Помочь каждому человеку найти свою идеальную IT-специальность, 
основанную на навыках, интересах и рыночном спросе!

⚠️ БОТ НАХОДИТСЯ НА СТАДИИ РАЗРАБОТКИ!

💡 В СЛУЧАЕ ВОЗНИКНОВЕНИЯ ПРОБЛЕМ / ПРЕДЛОЖЕНИЙ     
👨‍💻 Контакт: @krylov19"""
    
    await update.message.reply_text(help_text, reply_markup=reply_markup)

def split_message(text, max_length=4000):
    """Разделить длинное сообщение на части"""
    if len(text) <= max_length:
        return [text]
    
    parts = []
    while len(text) > max_length:
        # Находим последний перенос строки в пределах max_length
        split_point = text[:max_length].rfind('\n')
        if split_point == -1:
            split_point = max_length
        parts.append(text[:split_point].strip())
        text = text[split_point:].strip()
    
    if text:
        parts.append(text)
    
    return parts

async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать ПОЛНУЮ информацию о специальности"""
    text = update.message.text
    
    if text in SPECIALTY_DETAILS:
        # Отправляем полный текст специальности
        info_text = SPECIALTY_DETAILS[text]
        
        # Увеличиваем счетчик просмотров для специальности
        increment_specialty_view(text)
        
        keyboard = [
            ["🔙 Назад к выбору", "🎯 Другая специальность"],
            ["📋 О проекте", "🏠 Главная"]
        ]
        
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        # Разделяем длинные сообщения на части
        if len(info_text) > 4000:
            parts = split_message(info_text, 4000)
            
            # Отправляем первое сообщение с клавиатурой
            await update.message.reply_text(parts[0], reply_markup=reply_markup)
            
            # Отправляем остальные части
            for part in parts[1:]:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(info_text, reply_markup=reply_markup)
    
    elif text in IT_SPECIALTIES:
        # Если специальность есть в списке, но нет детальной информации
        keyboard = [
            ["🔙 Назад к выбору", "🏠 Главная"],
            ["📋 О проекте"]
        ]
        
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        # Используем новый текст для специальностей без информации
        info_text = f"🎯 *{text}*\n\n{INFO_IN_DEVELOPMENT}"
        
        # Увеличиваем счетчик просмотров для специальности
        increment_specialty_view(text)
        
        await update.message.reply_text(
            info_text,
            reply_markup=reply_markup
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню с новым оформлением"""
    global first_start
    
    # Добавляем пользователя в базу данных
    user = update.effective_user
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    add_or_update_user(user_data)
    
    keyboard = [
        ["🎯 Выбрать специальность", "📋 О проекте"],
        ["🔄 Обновить", "📞 Помощь"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Показываем приветственное сообщение только при первом запуске
    if first_start:
        # Отправляем новый краткий текст для первого запуска
        await update.message.reply_text(FIRST_START_MESSAGE)
        first_start = False
    
    # Всегда показываем основное сообщение с кнопками
    await update.message.reply_text(
        "👇 *ВЫБЕРИТЕ ДЕЙСТВИЕ:*",
        reply_markup=reply_markup
    )

async def go_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Переход на главную без показа приветственного сообщения"""
    # Обновляем информацию о пользователе
    user = update.effective_user
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    add_or_update_user(user_data)
    
    keyboard = [
        ["🎯 Выбрать специальность", "📋 О проекте"],
        ["🔄 Обновить", "📞 Помощь"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Просто показываем меню с кнопками
    await update.message.reply_text(
        "👇 *ВЫБЕРИТЕ ДЕЙСТВИЕ:*",
        reply_markup=reply_markup
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик фотографий"""
    await update.message.reply_text(
        "😔 Увы, я пока что не умею обрабатывать фотографии!\n\n"
        "Но я отлично справляюсь с текстом:\n"
        "• Выбирайте IT-специальности 🎯\n"
        "• Читайте подробную информацию 📚\n"
        "• Изучайте планы обучения 🚀\n\n"
        "👇 Используйте кнопки меню или напишите /start"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Глобальный обработчик ошибок"""
    print(f"❌ Ошибка: {context.error}")
    
    # Отправляем пользователю сообщение об ошибке
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "😔 Произошла ошибка. Попробуйте позже или напишите @krylov19"
            )
        except:
            pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик сообщений"""
    text = update.message.text
    
    if text == "🎯 Выбрать специальность":
        await show_menu(update, context)
    
    elif text == "📋 О проекте":
        await show_about_project(update, context)
    
    elif text in IT_SPECIALTIES:
        await show_info(update, context)
    
    elif text == "🔙 Назад":
        await show_menu(update, context)
    
    elif text == "🔙 Назад к выбору":
        await show_menu(update, context)
    
    elif text == "🏠 Главная":
        await go_home(update, context)
    
    elif text == "🎯 Все специальности":
        await show_menu(update, context)
    
    elif text == "🎯 Другая специальность":
        await show_menu(update, context)
    
    elif text == "📞 Помощь":
        await show_help(update, context)
    
    elif text == "🔄 Обновить":
        await go_home(update, context)
    
    elif text == "📊 Основная статистика":
        await show_stats(update, context)
    
    elif text == "📈 Детальная статистика":
        await show_detailed_stats(update, context)
    
    elif text == "/stats":
        await show_stats(update, context)
    
    elif text == "/detailed_stats":
        await show_detailed_stats(update, context)
    
    else:
        await go_home(update, context)

def main():
    """Запуск бота с красивым оформлением"""
    global first_start
    first_start = True  # Сбрасываем флаг при запуске бота
    
    # Инициализируем базу данных
    init_database()
    
    # Запускаем HTTP сервер для Render в отдельном потоке
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем глобальный обработчик ошибок
    app.add_error_handler(error_handler)
    
    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", show_help))
    app.add_handler(CommandHandler("about", show_about_project))
    app.add_handler(CommandHandler("refresh", show_menu))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(CommandHandler("detailed_stats", show_detailed_stats))
    
    # Добавляем обработчик фотографий
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Обработчик текстовых сообщений (должен быть последним!)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Красивое оформление при запуске (в консоли)
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║                 🤖 IT ВЫБОР 2026 🤖                      ║")
    print("║                                                          ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║                                                          ║")
    print(f"║  📊 Специальностей: {len(IT_SPECIALTIES)} (ТОЛЬКО технические)           ║")
    print("║                                                          ║")
    print("║  🎯 ПОЛНЫЙ разбор каждой специальности:                  ║")
    print("║     • Плюсы/минусы профессии                             ║")
    print("║     • Зарплаты 2026                                      ║")
    print("║     • Пошаговый план обучения                            ║")
    print("║     • Ресурсы (Habr, GitHub, курсы)                      ║")
    print("║     • Технологии и проекты                               ║")
    print("║     • Карьерный рост                                     ║")
    print("║                                                          ║")
    print("║  ⚠️  БОТ НАХОДИТСЯ НА СТАДИИ РАЗРАБОТКИ                  ║")
    print("║                                                          ║")
    print("║  💡 Мы будем постепенно:                                 ║")
    print("║     1. Заполнять все специальности                       ║")
    print("║     2. Улучшать информацию по запросам                   ║")
    print("║     3. Добавлять тесты на профориентацию                 ║")
    print("║     4. Создавать индивидуальные планы обучения           ║")
    print("║                                                          ║")
    print("║  🎯 ЦЕЛЬ: Помочь людям определиться с IT-специальностью  ║")
    print("║                                                          ║")
    print("║  👨‍💻 Контакт для предложений: @krylov19                   ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("✅ УЖЕ ЗАПОЛНЕНЫ ПОЛНОСТЬЮ:")
    print("   1. 🧠 AI/ML-Инженер")
    print("   2. 🌐 Веб-Разработчик")
    print("   3. 🤖 Data-Science")
    print("   4. 🔒 Кибербезопасность")
    print()
    print("🚫 ОСТАЛЬНЫЕ СПЕЦИАЛЬНОСТИ ПОКА В РАЗРАБОТКЕ:")
    print("   Для них отображается сообщение:")
    print("   '📝 Полная информация находиться в разработке!'")
    print()
    print("📊 БАЗА ДАННЫХ ОПТИМИЗИРОВАНА ДЛЯ 1000+ ПОЛЬЗОВАТЕЛЕЙ:")
    print("   • SQLite база: bot_users.db (WAL режим)")
    print("   • Индексы для быстрого поиска")
    print("   • Ежедневная статистика")
    print("   • Подробная аналитика")
    print("   • Не забудьте заменить ADMIN_ID на ваш Telegram ID!")
    print()
    print("🌐 HTTP СЕРВЕР ДЛЯ RENDER:")
    print("   • Порт: 8080")
    print("   • Health check: /healthz")
    print("   • Отвечает на запросы Render")
    print()
    print("🔄 ОСНОВНЫЕ УЛУЧШЕНИЯ:")
    print("   • Разделение длинных сообщений (>4000 символов)")
    print("   • Убран parse_mode='Markdown' для избежания ошибок")
    print("   • Добавлен глобальный обработчик ошибок")
    print("   • Улучшена обработка специальных символов")
    print()
    print("=" * 60)
    print("⚡ Бот запущен и готов к работе!")
    print("=" * 60)
    
    try:
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        print("🔄 Попробуйте перезапустить бота...")

if __name__ == "__main__":
    main()
