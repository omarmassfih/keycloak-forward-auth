# Contributing to Keycloak Forward Auth

Contributions are welcome. Follow this guide to ensure consistency and quality.

---

## How to Contribute
### 1. Fork and Clone
```bash
git clone https://github.com/yourusername/keycloak-forward-auth.git
cd keycloak-forward-auth
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Make Changes and Test
- Follow code style guidelines (`black`, `isort`).
- Run the application:
  ```bash
  uvicorn app:app --reload
  ```
- Run tests:
  ```bash
  pytest
  ```

### 5. Commit and Push
```bash
git add .
git commit -m "Add feature XYZ"
git push origin feature/your-feature-name
```

### 6. Submit a Pull Request
- Open a pull request on GitHub.
- Follow the pull request template.
- Ensure CI checks pass.

---

## Code Guidelines
- Follow PEP8 and Black formatting.
- Use meaningful commit messages.
- Write docstrings and type hints.
- Keep changes small and focused.

---

## Issues and Discussions
- Check existing issues before creating a new one.
- Use discussions for feature ideas.
- Provide clear steps to reproduce bugs.

---

## License
By contributing, you agree that your code will be under the MIT License.