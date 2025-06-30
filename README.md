# Multi-Platform Media Downloader 🎬

A clean, modern web application for downloading videos, music, and images from social media platforms. Built as a learning project to explore FastAPI, modern web development, and media processing.

![Demo](https://i.pinimg.com/originals/97/df/4a/97df4acbb437547ca7f7db9ace467050.gif)

## 🌟 Features

### Core Functionality
- **Multi-Platform Support**: Download from YouTube, Instagram, Twitter, Pinterest, TikTok, and 100+ other platforms
- **Multiple Formats**: Support for MP4 (video), MP3 (audio), and IMAGE downloads
- **Quality Selection**: Choose from various quality options (720p, 480p, 360p for videos; 320k, 256k, 192k for audio)
- **Fast Downloads**: Optimized download process with progress tracking
- **No API Keys Required**: Uses yt-dlp library for direct platform access

### User Experience
- **Clean Modern Interface**: Dark theme with soft gradients and glow effects
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Intuitive Workflow**: Simply paste URL, select format, and download
- **Progress Tracking**: Real-time download progress with status updates
- **Error Handling**: Clear error messages and retry options

### Technical Features
- **FastAPI Backend**: High-performance Python backend with async support
- **Vanilla JavaScript Frontend**: Clean, dependency-free frontend code
- **TailwindCSS Styling**: Modern utility-first CSS framework
- **Educational Code**: Extensively commented code perfect for learning
- **Production Ready**: Robust error handling and security considerations

## 🎯 Why I Built This

This project was created as a personal learning exercise to:
- Master modern web development with FastAPI and Python
- Understand async programming and background task processing
- Practice clean, maintainable code architecture
- Learn about media processing and file handling
- Explore responsive web design with TailwindCSS
- Build something actually useful for everyday media downloading needs

## 🛠️ How It Works

### Backend Architecture
- **FastAPI Server**: Handles API endpoints and serves static files
- **yt-dlp Integration**: Powerful media extraction library supporting 100+ platforms
- **Async Processing**: Non-blocking downloads with progress tracking
- **File Management**: Secure file handling and cleanup

### Frontend Design
- **Vanilla JavaScript**: No frameworks, pure ES6+ code
- **Progressive Enhancement**: Works without JavaScript for basic functionality
- **Responsive Layout**: Mobile-first design with TailwindCSS
- **Real-time Updates**: Dynamic progress tracking and error handling

### Technologies Used
- **Backend**: Python 3.11, FastAPI, uvicorn, yt-dlp, pydantic
- **Frontend**: HTML5, CSS3, JavaScript ES6+, TailwindCSS
- **Icons**: Font Awesome
- **Development**: Live reload, comprehensive logging

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/bentex2006/media-downloader.git
cd media-downloader
```

2. **Install dependencies**
```bash
pip install fastapi uvicorn yt-dlp pydantic
```

3. **Run the application**
```bash
python main.py
```

4. **Open your browser**
```
http://localhost:5000
```

That's it! The application will be running with live reload enabled for development.

## 🚀 Deployment

### Local Development
```bash
# Clone and install
git clone https://github.com/bentex2006/media-downloader.git
cd media-downloader
pip install -r requirements.txt

# Run with hot reload
python main.py
```

### Production Deployment

#### Using Docker (Recommended)
```bash
# Build the image
docker build -t media-downloader .

# Run the container
docker run -p 5000:5000 media-downloader
```

#### Using Replit
1. Fork this repository on Replit
2. Dependencies will install automatically
3. Click "Run" to start the server
4. Your app will be available at your Replit URL

#### Using Railway/Heroku
1. Connect your GitHub repository
2. Set the start command to: `python main.py`
3. Deploy with one click

#### Manual Server Deployment
```bash
# Install dependencies
pip install fastapi uvicorn yt-dlp pydantic

# Run with production server
uvicorn main:app --host 0.0.0.0 --port 5000
```

## 📱 Usage

1. **Paste any media URL** from supported platforms (YouTube, Instagram, Twitter, etc.)
2. **Select your preferred format**: MP4 (video), MP3 (audio), or IMAGE
3. **Choose quality settings**: From best quality to smallest file size
4. **Click Download** and wait for processing
5. **Download your file** when ready

### Supported Platforms
- YouTube (videos, playlists, channels)
- Instagram (posts, stories, reels)
- Twitter/X (videos, images)
- Pinterest (images, videos)
- TikTok (videos)
- Facebook (public videos)
- Vimeo, Dailymotion, Reddit
- And 100+ more via yt-dlp

## ⚠️ Disclaimer

**Important Legal Notice:**

This tool is designed for educational purposes and personal use only. Users are responsible for:

- **Respecting Copyright**: Only download content you own or have permission to download
- **Following Platform Terms**: Comply with the terms of service of each platform
- **Legal Compliance**: Ensure your usage complies with local laws and regulations
- **Personal Use Only**: Do not redistribute or use downloaded content commercially

The developer is not responsible for any misuse of this tool. Please respect content creators' rights and platform policies.

## 🧑‍💻 Development & Learning

### Code Philosophy
This project emphasizes **human-written, educational code** with the following principles:

- **Extensive Comments**: Every function, import, and logic block is explained
- **Clean Architecture**: Clear separation of concerns and modular design
- **Learning-Focused**: Code written to teach concepts, not just work
- **Best Practices**: Following Python and web development standards

### AI Assistance Disclosure
While this codebase is **primarily human-written** as a learning exercise, I utilized AI assistance for:
- Code review and optimization suggestions
- Documentation improvements
- Bug fixing guidance
- Best practice recommendations

The core logic, architecture decisions, and implementation approach are original human work designed for educational value.

## 👨‍💻 Author & Credits

**Created by:** [b3nt3x](https://linktr.ee/mrbentex)

- **GitHub**: [@bentex2006](https://github.com/bentex2006)
- **Links**: [linktr.ee/mrbentex](https://linktr.ee/mrbentex)

### Acknowledgments
- **yt-dlp** team for the incredible media extraction library
- **FastAPI** team for the modern Python web framework
- **TailwindCSS** for the utility-first CSS framework
- The open-source community for inspiration and resources

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Educational Use Encouraged**: Feel free to use this code for learning, modify it, and build upon it for your own projects.

## 🤝 Contributing

While this is primarily a personal learning project, contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear comments
4. Test thoroughly
5. Submit a pull request with detailed description

### Development Guidelines
- Follow the existing commenting style
- Maintain educational value of code
- Test all changes thoroughly
- Update documentation as needed

## 🐛 Issues & Support

If you encounter any issues:
1. Check the [Issues](https://github.com/bentex2006/media-downloader/issues) page
2. Create a new issue with detailed description
3. Include error logs and steps to reproduce

## ⭐ Show Your Support

If this project helped you learn or was useful, please consider:
- Starring the repository
- Sharing it with others learning web development
- Contributing improvements or suggestions

---

**Happy Learning! 🚀**
