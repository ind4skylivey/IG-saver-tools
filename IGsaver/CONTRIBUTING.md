# 🤝 Contributing to IGsaver

First off, thank you for considering contributing to IGsaver! It's people like you that make IGsaver such a great tool.

## 🌟 Ways to Contribute

### 1. 🐛 Report Bugs

Found a bug? Please [open an issue](https://github.com/ind4skylivey/IG-saver-tools/issues/new) with:

- **Clear title** describing the issue
- **Steps to reproduce** the bug
- **Expected vs actual behavior**
- **Environment details** (OS, Python version)
- **Logs** if applicable (from `logs/` directory)

### 2. 💡 Suggest Features

Have an idea? We'd love to hear it!

- [Open a feature request](https://github.com/ind4skylivey/IG-saver-tools/issues/new)
- Describe the feature and why it would be useful
- Feel free to propose implementation ideas

### 3. 📖 Improve Documentation

Documentation can always be better:

- Fix typos or unclear explanations
- Add examples or use cases
- Translate documentation
- Create video tutorials

### 4. 🔧 Submit Code

#### Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone git@github.com:YOUR_USERNAME/IG-saver-tools.git
   cd IG-saver-tools
   ```

3. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or venv/bin/activate.fish
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

#### Code Guidelines

**We follow clean code principles:**

- ✅ Use type hints for all function parameters and returns
- ✅ Write docstrings for all functions and classes
- ✅ Keep functions focused on a single responsibility
- ✅ Use descriptive variable and function names
- ✅ Add comments only when necessary to explain "why", not "what"
- ✅ Follow existing code style and structure

**Example:**

```python
def download_highlight(self, username: str, highlight_id: str) -> bool:
    """
    Download a single Instagram highlight
    
    Args:
        username: Instagram username
        highlight_id: ID of the highlight to download
        
    Returns:
        True if download successful, False otherwise
    """
    # Implementation here
    pass
```

#### Testing Your Changes

Before submitting:

```bash
# Test the basic functionality
./run.sh --help

# Test imports
python -c "from src.main import main; print('✓ Imports OK')"

# Run the tool (if you have Instagram access)
./run.sh --verbose
```

#### Commit Messages

We use conventional commits:

```
feat: Add support for downloading reels
fix: Handle expired session tokens correctly
docs: Update installation instructions
refactor: Simplify download logic
test: Add unit tests for auth module
```

**Format:**
```
<type>: <short description>

<optional longer description>

<optional footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

#### Submit Pull Request

1. **Push your changes:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub:**
   - Clear title and description
   - Link related issues
   - Describe what changed and why

3. **Wait for review:**
   - Address feedback if requested
   - Be patient and respectful

## 🎨 Design Contributions (Desktop App)

We're planning a desktop application! If you're a designer:

- Create mockups for the GUI
- Suggest UX improvements
- Design icons and branding
- Create demo videos

Share your work in [Discussions](https://github.com/ind4skylivey/IG-saver-tools/discussions)!

## 📋 Project Structure

```
IGsaver/
├── src/
│   ├── main.py              # Entry point
│   ├── app.py               # Main application logic
│   ├── cli.py               # CLI interface
│   ├── auth.py              # Authentication
│   ├── downloader.py        # Highlights downloader
│   ├── stories_downloader.py # Stories downloader
│   └── ...                  # Other modules
├── tests/                   # Tests (coming soon)
├── docs/                    # Additional documentation
└── ...
```

## 🔍 Areas Looking for Help

### High Priority
- [ ] **Testing on Windows** - Most development is on Linux
- [ ] **Testing on macOS** - Need Mac testers
- [ ] **2FA flow improvements** - Make it smoother
- [ ] **Error handling** - Better error messages
- [ ] **Desktop app design** - UI/UX mockups

### Medium Priority
- [ ] Unit tests
- [ ] Integration tests
- [ ] Documentation improvements
- [ ] Example configurations
- [ ] Video tutorials

### Future
- [ ] Desktop app development (Electron/Tauri)
- [ ] Cloud sync features
- [ ] Analytics dashboard
- [ ] Translations

## 💬 Communication

- **Questions?** Open a [Discussion](https://github.com/ind4skylivey/IG-saver-tools/discussions)
- **Bug or feature?** Open an [Issue](https://github.com/ind4skylivey/IG-saver-tools/issues)
- **Want to chat?** Use GitHub Discussions

## 🏆 Recognition

Contributors will be:
- Added to README.md acknowledgments
- Mentioned in release notes
- Forever grateful to! ❤️

## 📜 Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior:**
- Being respectful and inclusive
- Welcoming newcomers
- Accepting constructive criticism
- Focusing on what's best for the community

**Unacceptable behavior:**
- Harassment or discriminatory comments
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

### Enforcement

Instances of unacceptable behavior may be reported by opening an issue or contacting the maintainers. All complaints will be reviewed and investigated.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution, no matter how small, is valued and appreciated. Thank you for helping make IGsaver better for everyone!

**Happy coding! 🚀**
