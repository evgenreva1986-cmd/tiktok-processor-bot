![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-blue?logo=telegram)
# TikTok Media Processor & Recognition Bot

A high-performance media processing tool that bridges asynchronous audio recognition with automated filesystem management for Telegram.

![Bot Interface Preview](demo.png)

## Technical Highlights

* **Asynchronous Integration:** Leveraging `asyncio` for the Shazam recognition engine allows the bot to handle high-latency API requests efficiently.
* **Advanced Media Processing:** Utilizing a hybrid approach with `yt-dlp` for stream capturing and `FFmpeg` for extracting audio layers and re-encoding them into high-quality MP3 (192kbps).
* **Resilient Error Handling:** Implemented a robust multi-layered exception handling system to manage network timeouts, conversion failures, and unsupported media types.
* **Security-First Design:** Sensitive credentials are encapsulated using environment variables via `python-dotenv`.
* **Automated Lifecycle Management:** Built-in resource cleanup routines ensure the server's filesystem remains pristine by purging temporary media artifacts immediately after delivery.

## Tech Stack

* **Language:** Python 3.10+
* **Bot Framework:** pyTelegramBotAPI (Telebot)
* **Media Core:** yt-dlp, FFmpeg
* **Recognition:** Shazamio (Asynchronous Shazam API)
* **Environment:** python-dotenv

## Project Structure

```text
├── main.py            # Main script with bot logic and handlers
├── ffmpeg             # Linux binary for multimedia processing
├── ffprobe            # Linux binary for media stream analysis
├── requirements.txt   # Python dependencies and libraries
├── Aptfile            # System packages configuration for hosting
├── buildpacks         # Custom build configurations for deployment
├── .python-version    # Specifies the Python version for the environment
├── .gitignore         # Git rules to exclude sensitive or temporary files
├── LICENSE            # MIT License agreement
├── README.md          # Project documentation and setup guide
└── demo.png           # Visual preview or screenshot of the bot
```
## Installation & Setup
### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
## 2. FFmpeg Configuration
The project uses custom Linux binaries included in the repository. Ensure that the ffmpeg and ffprobe files in the root directory have executable permissions:
```Bash
chmod +x ffmpeg ffprobe
```
Note: If you are developing on Windows, you will need the Windows versions (.exe) of these binaries.
## 3. Environment Variables
Create a `.env` file in the root directory and add your bot token:
```Bash
API_TOKEN=your_telegram_bot_token_here
```
## 4. Run the Application
```Bash

python main.py
```
## 🚀 Try it out
Click the button below to start the bot:

[![Start Bot](https://img.shields.io/badge/Start_on_Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/link_to_vid_tt_bot)

## Future Improvements
* Asynchronous Migration: Transitioning to aiogram for superior concurrency and production-grade stability.

* Database Integration: Adding PostgreSQL or Redis for user analytics and intelligent result caching.

* Dockerization: Containerizing the application for seamless, one-click multi-platform deployment.

* Queue Management: Implementing task queues (e.g., Celery) to handle heavy media processing workloads in the background.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
