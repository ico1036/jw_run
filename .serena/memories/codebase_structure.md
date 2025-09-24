# Codebase Structure

## Root Directory Layout
```
jw_run/
├── src/                           # Core Python modules
│   └── superclaude_helper.py     # Main SuperClaude helper class
├── config/                        # Configuration files
│   └── superclaude_config.json   # SuperClaude settings and workflows
├── examples/                      # Usage examples
│   └── workflow_examples.py      # Demo workflows
├── tests/                         # Testing infrastructure
│   ├── run_tests.py              # Main test runner
│   ├── playwright/               # Playwright E2E tests
│   ├── debug_screenshots/        # Test evidence/debugging
│   └── reports/                  # Generated test reports
├── saturday-run-coffee-club/     # Web application
│   ├── index.html               # Main web page
│   ├── css/, js/, images/       # Frontend assets
│   └── server.js                # Node.js server
├── main.py                       # Project entry point
├── pyproject.toml               # Python project configuration
└── README.md                    # Project documentation
```

## Key Components

### SuperClaude Helper Module (`src/superclaude_helper.py`)
- **SuperClaudeHelper class** - Main utility for framework integration
- **Workflow management** - Command sequence generation
- **Persona recommendation** - Task-based persona selection
- **Configuration management** - JSON config loading

### Testing Infrastructure (`tests/`)
- **Comprehensive E2E testing** with Playwright
- **Cross-browser compatibility** testing
- **Mobile responsive** testing
- **Admin functionality** testing
- **Performance monitoring** and reporting

### Saturday Run Club (`saturday-run-coffee-club/`)
- **Static web application** for event management
- **Responsive design** with Aman Hotels inspiration
- **GitHub API integration** for participant management
- **Multiple deployment targets** (GitHub Pages, Vercel, Render)

## Entry Points
- `main.py` - SuperClaude framework demonstration
- `tests/run_tests.py` - Comprehensive test suite execution
- `saturday-run-coffee-club/index.html` - Web application
- `src/superclaude_helper.py` - Direct module testing