# Virginia DMV Practice Test 🚗

A modern, interactive web application built with Flask that helps users prepare for the Virginia DMV permit exam. Features an engaging user interface, detailed feedback system, and comprehensive test coverage of all DMV manual topics.

## ✨ Features

- **Interactive Test Interface**: Dynamic question-by-question progression
- **Comprehensive Coverage**: Questions from all major DMV manual sections
- **Smart Question Selection**: Balanced distribution across categories
- **Visual Learning**: Integrated road sign and scenario images
- **Detailed Feedback**: Explanations for both correct and incorrect answers
- **Progress Tracking**: Section-by-section progress monitoring
- **Mobile Responsive**: Optimized for both desktop and mobile devices
- **Score Analysis**: Detailed breakdown of performance by category

## 🛠️ Tech Stack

- **Backend**: Python 3.x with Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Storage**: JSON-based question bank
- **Image Processing**: Python Pillow for image optimization
- **Testing**: Python unittest framework

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/spotcircuit/dmv_test.git
   cd dmv_test
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access at http://localhost:3022

## 📚 Project Structure

```
dmv_test/
├── app.py                 # Main Flask application
├── static/               # Static assets
│   ├── dmv_images/      # Test images
│   └── styles.css       # CSS styling
├── templates/           # HTML templates
├── quiz_data/          # Question data and configurations
└── utils/              # Utility scripts and helpers
```

## 🎯 Test Content

### Categories
- **Road Signs** (25%): Traffic signs, signals, and markings
- **Rules of the Road** (25%): Traffic laws and regulations
- **Safe Driving** (20%): Defensive driving techniques
- **Penalties and Insurance** (15%): Legal requirements
- **Alcohol and Drugs** (15%): Safety and legal implications

### Question Format
```json
{
    "category": "Road Signs",
    "question": "What does this sign mean?",
    "options": ["A. Stop", "B. Yield", "C. Merge", "D. Speed Limit"],
    "image": "stop_sign.jpg",
    "answer": "A",
    "explanation": "The red octagonal sign always means STOP..."
}
```

## 🔧 Development Tools

The repository includes several utility scripts:
- `auto_quiz_scraper.py`: Automated question collection
- `image_verification.py`: Image validation tools
- `clean_questions.py`: Data cleaning utilities
- `test_dmv_questions.py`: Test suite

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🔄 Version History

### Current Version (2.0)
- Enhanced mobile responsiveness
- Improved feedback system
- Optimized image loading
- Updated question bank
- Added comprehensive test coverage

## 📞 Support

For issues and feature requests, please use the GitHub issues tracker.

---

Made with ❤️ by SpotCircuit
