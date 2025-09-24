# Design Patterns & Guidelines

## SuperClaude Framework Patterns

### Command Pattern
- **Workflow Commands**: Structured as command sequences (e.g., `["/sc:design", "/sc:implement", "/sc:test"]`)
- **Persona Commands**: Task-driven persona selection based on keywords
- **Configuration Commands**: JSON-driven workflow configuration

### Strategy Pattern
- **Multiple deployment strategies**: GitHub Pages, Vercel, Render
- **Testing strategies**: Local, browser compatibility, mobile responsive
- **Persona selection strategies**: Keyword-based, task-type based

### Observer Pattern
- **Test result monitoring**: SuperClaudeTestAnalyzer observes test execution
- **Performance tracking**: Built-in performance monitoring during tests
- **Error reporting**: Automatic issue generation for high-severity problems

## Development Guidelines

### Single Responsibility
- Each module has clear, focused purpose
- SuperClaudeHelper - Framework utility only  
- TestRunner - Testing orchestration only
- Individual test files - Specific testing concerns

### Configuration Over Code
- Workflows defined in JSON, not hardcoded
- Persona preferences configurable
- MCP server selection configurable
- Quality checklists configurable

### Graceful Degradation
- **Fallback configurations** when JSON missing
- **Local storage fallback** when GitHub API unavailable
- **Error handling** with user-friendly Korean messages
- **Default values** for all configuration options

## Testing Design Patterns

### Page Object Pattern (Implicit)
- Test methods interact with specific page elements
- Reusable selectors and interactions
- Separation of test logic from page structure

### Test Data Builder Pattern
- Configuration-driven test scenarios
- Reusable test setup and teardown
- Consistent test environment preparation

### Reporter Pattern
- SuperClaudeTestAnalyzer generates structured reports
- Multiple output formats (Markdown, GitHub issues)
- Evidence collection through screenshots

## Korean UX Patterns
- **User-facing messages in Korean** for better accessibility
- **Technical terms in English** for developer clarity
- **Respectful language patterns** ("주인님", "🙇‍♂️")
- **Emoji-enhanced communication** for visual clarity