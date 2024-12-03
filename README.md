# Virginia DMV Practice Test

A Flask-based web application that provides an interactive practice test for the Virginia DMV permit exam, featuring engaging feedback and a modern user interface.

## Project Structure
```
virginia_permit_test/
├── static/
│   ├── dmv_images/      # Test question images
│   └── styles.css       # Application styling
├── templates/
│   ├── test.html        # Main test interface
│   ├── results.html     # Test results page
│   └── image_test.html  # Image loading test page
├── app.py              # Flask application
├── new_questions.json  # Test questions database
└── requirements.txt    # Project dependencies
```

## Current Features
- Interactive question-by-question test interface
- Dynamic feedback system with humorous responses
- Progress tracking through test sections
- Image-based questions for road signs and scenarios
- Results page with score breakdown

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python app.py
```
4. Access the application at http://localhost:3022

## Current Challenges
- Image loading issues in the main test interface
- Need to implement proper error handling for missing images
- Further testing needed for question progression and scoring
- Session management issues causing "Session expired" errors
- Image path not being correctly set in the HTML template

## Next Steps
1. Debug and fix image loading in the main test interface
2. Implement error handling for missing or corrupted images
3. Add comprehensive test coverage
4. Enhance mobile responsiveness
5. Add user session management
6. Implement question randomization within sections
7. Verify Flask session settings and ensure proper session management
8. Ensure image keys in question data match those in the `IMAGES` dictionary

## Dependencies
- Flask
- Python 3.x
- Additional requirements listed in requirements.txt

## Testing
- Test route available at /image_test for verifying image loading
- Main test interface at /
- Results page accessible after test completion

## Data Structure

### Test Sections Distribution
The test is divided into specific categories with question allocations:
- Road Signs: 9 questions (25%)
- Rules of the Road: 9 questions (25%)
- Safe Driving: 7 questions (20%)
- Penalties and Insurance: 5 questions (15%)
- Alcohol and Drugs: 5 questions (15%)

### Question Format
Questions are stored in `new_questions.json` with the following structure:
```json
{
    "category": "Road Signs",
    "question": "What does a red octagonal sign indicate?",
    "options": [
        "A. Yield",
        "B. Stop",
        "C. Do not enter",
        "D. No parking"
    ],
    "image": "stop.jpg",
    "answer": "B",
    "explanation": "Engaging feedback message..."
}
```

### Session Management
- Questions are randomly selected within their categories
- Progress is tracked per section
- Scores are maintained throughout the session
- Feedback is provided after each answer

## Application Flow
1. User starts test at root URL (/)
2. Questions are presented one at a time
3. User selects answer and receives immediate feedback
4. "Next Question" button appears after answering
5. Results page shows after completing all sections

## 🚀 Quick Start

### Prerequisites
- Windows OS
- Python 3.8+
- PowerShell (Administrator access)
- Web browser (Chrome/Firefox recommended)

### Setup (First Time)
1. Clone and navigate:
```powershell
git clone [repository-url]
cd virginia_permit_test
```

2. Run setup script (as Administrator):
```powershell
.\dev_setup.ps1
```

3. Access application:
```
http://127.0.0.1:3022
```

### Daily Development
```powershell
.\venv\Scripts\Activate
python app.py
```

## 📁 Project Structure

### Active Components
```
virginia_permit_test/
├── app.py                # Core application logic
├── new_questions.json    # Question database
├── requirements.txt      # Python dependencies
├── dev_setup.ps1        # Setup automation
├── static/
│   └── styles.css       # Application styling
├── templates/
│   ├── test.html        # Quiz interface
│   └── results.html     # Results page
└── archive/             # Archived files (deprecated)
```

### Key Files
- `app.py`: Flask application with quiz logic and routing
- `new_questions.json`: Structured question data following VA DMV format
- `dev_setup.ps1`: Automated environment setup and configuration

## 🛠 Technical Stack

### Backend
- **Framework**: Flask 3.0.0+
- **Session Management**: Flask-Session
- **Port**: 3022 (Windows Defender compatible)
- **Python Version**: 3.8+

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Mobile-first responsive design
- **JavaScript**: ES6+ standards
- **Dependencies**: Listed in requirements.txt

## 🔧 Configuration

### Port Settings
- Using port 3022 (3000-4000 range)
- Windows Defender configured via dev_setup.ps1
- Avoid common ports (80, 8080, 5000)

### Session Configuration
- Type: Filesystem
- Lifetime: 30 minutes
- Storage: Local filesystem
- Cleanup: Automatic between tests

## 📊 Data Structure

### Question Format
```json
{
    "category": "Road Signs",
    "question": "What does this sign mean?",
    "options": ["A", "B", "C", "D"],
    "answer": "A",
    "explanation": "Detailed explanation",
    "image": "optional_image.jpg"
}
```

### Categories (VA DMV Requirements)
- Road Signs (25%): 9 questions
- Rules of the Road (25%): 9 questions
- Safe Driving (20%): 7 questions
- Penalties/Insurance (15%): 5 questions
- Alcohol/Drugs (15%): 5 questions

## 🐛 Known Issues & Roadmap

### Current Issues
- [ ] Navigation between questions needs repair
- [ ] Question count verification needed
- [ ] Session cleanup monitoring required

### Planned Features
- [ ] User authentication
- [ ] Progress saving
- [ ] Practice mode
- [ ] Statistical tracking
- [ ] Additional questions

## 🔍 Troubleshooting

### Common Issues
1. **Port Access**
   - Run PowerShell as Administrator
   - Use dev_setup.ps1
   - Check Windows Defender

2. **Python Environment**
   - Verify virtual environment
   - Check requirements.txt
   - Confirm Python version

3. **Session Issues**
   - Clear browser cache
   - Check flask_session directory
   - Restart application

## 📝 Development Protocols

### Code Standards
- **Python**: PEP 8 compliance
- **HTML/CSS**: BEM methodology
- **JavaScript**: ES6+ standards
- **Git**: Meaningful commit messages

### File Management
- Keep active files in main directory
- Archive deprecated files
- Document major changes
- Maintain version control

### Testing Requirements
- Manual testing of quiz flow
- Session persistence verification
- Mobile responsiveness checks
- Cross-browser compatibility

## 🔒 Security Considerations

### Windows Environment
- Run PowerShell as Administrator
- Configure Windows Defender
- Use recommended port range
- Follow security protocols

### Data Protection
- No sensitive data in sessions
- Regular session cleanup
- Secure question storage
- Protected admin functions

## 📚 Documentation Standards

### Code Comments
- Function purpose and parameters
- Complex logic explanation
- TODO markers for improvements
- Version update notes

### Git Commits
- Descriptive messages
- Reference issue numbers
- Document breaking changes
- Tag version releases

## 🤝 Contributing

### Process
1. Fork repository
2. Create feature branch
3. Follow code standards
4. Submit pull request

### Guidelines
- Test thoroughly
- Update documentation
- Follow security protocols
- Maintain compatibility

## 📋 Maintenance

### Regular Tasks
- Update dependencies
- Clean session data
- Monitor logs
- Backup question database

### Version Control
- Semantic versioning
- Release notes
- Change documentation
- Backup procedures

## 🆘 Support

### Resources
- Official VA DMV materials
- Flask documentation
- Python best practices
- Web security guidelines

### Contact
[Project maintainer contact information]

## Version History

### Version 1.15 (Current)
- Fixed modal popup functionality in both practice and test modes
- Improved button text to correctly reflect current mode ("Try Again" in practice, "Next Question" in test)
- Enhanced modal animations and transitions
- Fixed score tracking and display
- Improved error handling in answer submission

### Version 1.14
- Initial mode selection implementation
- Added Gen Z themed feedback
- Implemented streak tracking
- Basic question loading

### Version 1.13
#### Route Structure Changes
- Separated routes for better flow:
  - `/` → Mode selection splash screen
  - `/test` → Question display
  - `/static/images/<filename>` → Image serving

#### Session Management
- Modified session handling:
  - Clear session only when entering mode selection
  - Maintain session data while switching modes
  - Added fallback for sections: `sections = load_questions() or []`

#### Mode Behavior
- Practice Mode:
  - Stay on question until correct answer
  - Track wrong attempts
  - Show explanations
- Test Mode:
  - Move to next question regardless of answer
  - Track score and streak
  - One attempt per question

### Current Issues (1.13)
1. **Modal Popups**: Not displaying after answer submission
   - Attempted fixes:
     - Simplified modal CSS
     - Added debug logging
     - Modified modal display logic
     - Changed JavaScript event handling

2. **Image Loading**: Intermittent issues with first image
   - Added error handling for image serving
   - Logging for failed image loads

### Next Steps
1. Investigate modal popup issues:
   - Check JavaScript console for errors
   - Verify event handling
   - Consider alternative popup implementation

2. Monitor and improve:
   - Image loading reliability
   - Session state management
   - Mode switching behavior

### Technical Notes
- Flask backend with session management
- JavaScript frontend for interactivity
- Static file serving for images
- JSON-based question storage

This documentation tracks the evolution of the application and current focus areas for improvement.
