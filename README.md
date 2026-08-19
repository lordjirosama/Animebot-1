🎌 Solurix Anime Info Bot

A powerful Telegram Anime Information Bot built with Python, Pyrogram, AniList GraphQL API, MongoDB, and Docker.

The bot is designed to provide anime information, posters, characters, ratings, genres, airing schedules, and more directly inside Telegram.

«🌐 Powered by Solurix Bots

📢 Channel: https://t.me/Solurix_bots»

---

✨ Features

🔎 Anime Search

Search for anime simply by sending the anime name.

Examples:

Naruto
One Piece
Solo Leveling
Attack on Titan
Demon Slayer

The bot searches AniList and returns matching anime.

🖼️ Anime Posters

The bot automatically fetches available anime cover images from AniList.

Poster information is used directly from the AniList media data, so no separate image API key is required.

📖 Complete Anime Information

Get useful information including:

- 🎌 Anime title
- 🇯🇵 Native title
- 🌐 English/Romaji title
- 📺 Format
- 📊 Status
- 🎬 Episodes
- ⏱️ Episode duration
- 📅 Season and year
- ⭐ Average score
- 🎭 Genres
- 📝 Synopsis
- 🔗 AniList page

👥 Character Information

The bot can retrieve character information for an anime.

It currently provides:

- Character name
- Character role
- Anime title
- Character information from AniList

🎭 Genre Search

Browse popular anime by genre.

Supported AniList genres can include:

- Action
- Adventure
- Comedy
- Drama
- Fantasy
- Horror
- Mystery
- Romance
- Sci-Fi
- Sports
- Supernatural
- Thriller
- and other AniList-supported genres

📅 Anime Schedule

Use:

/schedule

to view upcoming anime episodes available through AniList's airing schedule.

Information includes:

- 🎌 Anime title
- 🎬 Episode number
- 🕐 Airing time

⚡ Inline Search

The bot supports Telegram inline search.

After enabling inline mode through BotFather:

@YourBot Naruto

can be used directly from Telegram chats.

👤 User System

The bot can maintain basic user records in MongoDB.

Stored information includes:

- Telegram user ID
- First name
- Last name
- Username
- Active status
- Creation time
- Last update time

⚙️ User Settings

Users can check their current settings using:

/settings

Current settings include:

- 🌐 Language
- 🔔 Notifications

The settings system is designed to support additional options in future updates.

📊 Statistics

The owner can use:

/stats

to view basic bot statistics such as:

- Total registered users
- Active users

📢 Broadcast

The owner can use:

/broadcast Your message

to send an announcement to registered users.

The bot also reports:

- ✅ Successfully sent messages
- ❌ Failed messages

👑 Owner Panel

The owner can use:

/admin

to access the owner-only admin area.

Unauthorized users cannot use owner commands.

---

🤖 Bot Commands

👤 User Commands

Command| Description
"/start"| Start the bot
"/help"| Show available commands
"/schedule"| Show upcoming anime episodes
"/settings"| View user settings

🔎 Search

No command is required.

Simply send an anime name:

Naruto

One Piece

Solo Leveling

---

👑 Owner Commands

Command| Description
"/admin"| Open owner panel
"/stats"| Show bot statistics
"/broadcast <message>"| Broadcast a message

---

🧩 Inline Buttons

Anime search results provide interactive buttons such as:

📖 Full Info
👥 Characters
🔗 AniList

The full information page also provides:

👥 Characters
🔄 Refresh
🔗 Open AniList

---

🌐 AniList Integration

Anime information is retrieved using the public AniList GraphQL API.

AniList provides the anime metadata used by this bot, including titles, descriptions, scores, genres, episodes, characters, cover images, and airing information.

AniList:

https://anilist.co/

API:

https://graphql.anilist.co

No AniList API key is required for the public GraphQL requests used by this project.

---

🖼️ Image System

The bot obtains anime cover images from AniList.

The image flow is:

Anime Search
      ↓
AniList
      ↓
Anime Media Data
      ↓
Cover Image URL
      ↓
Telegram
      ↓
🖼️ Anime Poster

If an available poster cannot be sent, the bot falls back to a text result instead of failing the complete search.

---

💾 Database

MongoDB is used for persistent user-related information.

Collections

The project currently uses collections such as:

users
user_settings

Users

Stores basic Telegram user information.

User Settings

Stores user preferences such as:

language
notifications

MongoDB is optional for basic anime searching, but database-dependent features such as user statistics and broadcasting require MongoDB.

---

⚡ Cache System

The bot includes an in-memory cache to reduce unnecessary repeated AniList requests.

The cache can store:

- Anime searches
- Anime information
- Character information
- Genre results
- Airing schedules

Cached data automatically expires after its configured lifetime.

This helps reduce repeated API requests and improves response speed.

---

📁 Project Structure

Animebot-1/
│
├── bot.py
├── config.py
├── database.py
├── utils.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
│
└── plugins/
    ├── __init__.py
    ├── keyboards.py
    ├── anilist.py
    ├── anime_parser.py
    ├── cache.py
    ├── start.py
    ├── search.py
    ├── anime_info.py
    ├── characters.py
    ├── genres.py
    ├── schedule.py
    ├── callbacks.py
    ├── inline.py
    ├── commands.py
    ├── admin.py
    ├── broadcast.py
    ├── stats.py
    ├── users.py
    └── settings.py

---

⚙️ Configuration

Create your private ".env" file from ".env.example".

BOT_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash

MONGO_URI=your_mongodb_uri
DATABASE_NAME=anime_info_bot

OWNER_ID=your_telegram_user_id

Configuration Details

Variable| Purpose
"BOT_TOKEN"| Telegram bot token
"API_ID"| Telegram API ID
"API_HASH"| Telegram API hash
"MONGO_URI"| MongoDB connection URI
"DATABASE_NAME"| MongoDB database name
"OWNER_ID"| Telegram owner user ID

🔐 Security

Never publish:

.env
BOT_TOKEN
API_HASH
MONGO_URI

The ".gitignore" file already prevents ".env" from being committed.

---

🐳 Docker Deployment

Docker is the recommended deployment method.

Build and start

docker compose up -d --build

View logs

docker compose logs -f

Stop

docker compose down

Restart

docker compose restart

Check running containers

docker ps

---

🐍 Manual Installation

Install the required packages:

pip install -r requirements.txt

Create the environment file:

cp .env.example .env

Configure ".env", then start the bot:

python bot.py

---

🔄 Plugin System

The bot uses a modular plugin architecture.

Every Python file inside:

plugins/

is automatically discovered and loaded by "bot.py".

This makes it easy to:

- Add new features
- Remove individual features
- Maintain separate functionality
- Expand the bot without making "bot.py" unnecessarily large

---

🛡️ Error Handling

The project is designed to handle common failures gracefully.

Examples include:

- AniList unavailable
- Invalid search
- Missing anime information
- Missing poster
- MongoDB unavailable
- Invalid user input
- Unauthorized owner commands

Where possible, the bot returns a user-friendly message instead of crashing.

---

🚀 Planned Features

The project can be expanded with additional anime-related features.

Possible future additions:

- 🎬 Studio information
- 🏆 Detailed rankings
- 🔥 Trending anime
- 📈 Popular anime
- 🆕 Seasonal anime
- 📺 Better episode tracking
- 👤 Detailed character cards
- 🎨 Character images
- 🔔 Anime airing notifications
- ❤️ User favorites
- 📚 Watchlist
- 🔍 Advanced filters
- 🌐 Multiple language support
- 📊 Advanced statistics
- 🖼️ Custom branding images

These features are planned and should not be considered available until implemented in the code.

---

📢 Solurix Bots

This project is maintained under the Solurix Bots branding.

Official Channel

https://t.me/Solurix_bots

---

❤️ Credits

Anime Data

Anime information is provided through:

AniList

https://anilist.co/

Framework

Built with:

Pyrogram

https://github.com/pyrogram/pyrogram

Database

MongoDB

Containerization

Docker

---

⚠️ Disclaimer

This project is intended for educational and informational purposes.

Anime metadata and images are retrieved from third-party services. The bot does not claim ownership of third-party anime artwork, characters, titles, or metadata.

---

📜 License

This project can be distributed and modified according to the license included with the repository.

---

🌟 Solurix Bots

Anime information, directly in Telegram.

🌐 https://t.me/Solurix_bots# Animebot-1