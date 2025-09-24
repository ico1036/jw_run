# Task Completion Workflow

## When Task is Completed

### 1. Testing Requirements
- **Always run tests** before considering task complete
- Primary test command: `uv run python tests/run_tests.py`
- Verify specific functionality with targeted tests if needed

### 2. Code Quality Checks
- **No formal linting configured yet** - follow Python style conventions manually
- **No automatic formatting** - maintain consistent style as per existing code
- **Type checking** - Ensure type hints are consistent and accurate

### 3. Verification Steps
```bash
# 1. Run comprehensive test suite
uv run python tests/run_tests.py

# 2. Verify main functionality still works
uv run python main.py

# 3. Check helper module functionality  
uv run python src/superclaude_helper.py

# 4. If web components changed, test locally
cd saturday-run-coffee-club && python3 -m http.server 8000
```

### 4. Documentation Updates
- Update relevant docstrings for any modified functions
- Update README.md if significant functionality added
- Update config files if new workflow patterns added

### 5. Git Operations
```bash
# Standard git workflow
git add .
git status  # Review changes
git commit -m "Descriptive commit message"
# Push only when explicitly requested
```

### 6. Special Considerations
- **Saturday Run Club**: Test both local server and GitHub Pages if frontend changed
- **SuperClaude Helper**: Verify config loading and workflow generation
- **Cross-browser compatibility**: Run browser tests if UI changes made

### 7. Failure Handling
- If tests fail, **do not proceed** with task completion
- Investigate root cause using debug tests
- Fix issues before marking task complete
- Generate test reports for complex failures