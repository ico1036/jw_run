# Suggested Commands

## Development Commands
```bash
# Install and sync dependencies
uv sync

# Run main SuperClaude helper demo
uv run python main.py

# Run SuperClaude helper directly
uv run python src/superclaude_helper.py

# Run examples
uv run python examples/workflow_examples.py
```

## Testing Commands
```bash
# Run all Playwright tests
uv run python tests/run_tests.py

# Run specific test modules
uv run python tests/simple_verification.py
uv run python tests/final_verification.py
uv run python tests/emergency_debug.py

# Run pytest tests
uv run pytest tests/playwright/

# Debug specific issues
uv run python tests/debug_im_in_button.py
```

## Local Development (Saturday Run Club)
```bash
# Start local server for Saturday Run Club
cd saturday-run-coffee-club
python3 -m http.server 8000

# Alternative: Node.js server
cd saturday-run-coffee-club
node server.js
```

## Project Management
```bash
# Check project structure
tree -I '__pycache__|.git|.venv|node_modules'

# Git operations
git status
git add .
git commit -m "description"
git push origin main
```

## Darwin/macOS Specific Commands
```bash
# File operations
ls -la
find . -name "*.py" -type f
grep -r "pattern" .
cat filename.txt
open -a TextEdit filename.txt

# Process management  
ps aux | grep python
kill -9 <pid>
lsof -i :8000  # Check port usage
```