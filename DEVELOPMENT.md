# Development Documentation

## Current Project Status

### What Works
- Application running on port 3022
- Question loading and categorization
- Session management
- Basic quiz functionality
- Mobile-responsive UI

### Known Issues
- Port 5000 blocked by Windows Defender (resolved by using 3022)
- Session cleanup needs monitoring
- Need to verify all questions are properly categorized

## Development Environment

### Required Setup
1. Windows PowerShell (Admin privileges)
2. Python 3.8+
3. Git
4. Web browser (Chrome/Firefox recommended)

### First-Time Setup
```powershell
# Run as Administrator
.\dev_setup.ps1
```

### Daily Development
1. Start PowerShell in project directory
2. Activate virtual environment:
```powershell
.\venv\Scripts\Activate
```
3. Run application:
```powershell
python app.py
```
4. Access: http://127.0.0.1:3022

## Project Structure

### Active Files
- `app.py` - Main application
- `new_questions.json` - Question database
- `templates/test.html` - Quiz interface
- `templates/results.html` - Results page
- `static/styles.css` - Styling
- `requirements.txt` - Dependencies
- `dev_setup.ps1` - Setup script

### Archived Files (in archive/)
- `VA_DMV_100_Unique_Questions_Quiz.py` - Old CLI version
- `quiz_data.py` - Deprecated data handler
- `test.html.bak` - Backup template

## Session Notes for Next Time

### Completed
- Fixed port issues (now using 3022)
- Archived old files
- Created setup documentation
- Added PowerShell setup script
- Updated project structure

### Next Steps
1. **High Priority**
   - Add user authentication
   - Implement progress saving
   - Add practice mode
   - Enhance statistical tracking

2. **Testing Needed**
   - Session persistence
   - Question distribution
   - Mobile responsiveness
   - Windows Defender interaction

3. **Documentation Needed**
   - API documentation
   - Database schema
   - Test procedures
   - Deployment guide

### Useful Prompts for Next Session

1. For debugging:
```
I'm seeing [specific error] when [action]. Can you help diagnose the issue?
```

2. For new features:
```
I want to add [feature] to the application. What's the best way to implement this?
```

3. For testing:
```
Can you help create test cases for [component/feature]?
```

4. For documentation:
```
Please document how [feature/component] works and how to use it.
```

## Common Commands

### PowerShell
```powershell
# Setup
.\dev_setup.ps1

# Run application
python app.py

# Install new dependency
pip install [package]
pip freeze > requirements.txt

# Git commands
git status
git add .
git commit -m "descriptive message"
git push
```

### Flask Routes
- `/` - Main quiz interface
- `/test` - Test page
- `/test2` - Template test
- `/results` - Quiz results

## Troubleshooting Guide

### Port Issues
1. Check Windows Defender
2. Verify port 3022 is free
3. Run PowerShell as admin
4. Use `dev_setup.ps1`

### Session Issues
1. Clear browser cache
2. Check `flask_session` directory
3. Restart application
4. Verify Flask-Session config

### Python Issues
1. Verify virtual environment
2. Check Python version
3. Reinstall dependencies
4. Check log files

## Security Notes

### Windows Defender
- Port range 3000-4000 recommended
- Use `dev_setup.ps1` for firewall rules
- Run PowerShell as administrator

### Session Security
- 30-minute timeout
- Filesystem storage
- No sensitive data in session
- Clear sessions regularly

## Coding Standards

### Python
- PEP 8 compliant
- Type hints where possible
- Comprehensive error handling
- Detailed logging

### HTML/CSS
- Mobile-first approach
- Semantic HTML5
- BEM naming convention
- Cross-browser compatible

### JavaScript
- ES6+ standards
- Event delegation
- Error handling
- Console logging for debug

## Testing Procedures

### Manual Testing
1. Quiz flow
2. Session handling
3. Mobile responsiveness
4. Cross-browser compatibility

### Automated Testing (Future)
- Unit tests
- Integration tests
- E2E tests
- Performance tests
