# Code Style & Conventions

## Python Style
- **Type Hints**: Used throughout (e.g., `def suggest_persona(self, task_description: str) -> str:`)
- **Docstrings**: Google-style docstrings for all classes and methods
- **Naming**: snake_case for functions and variables, PascalCase for classes
- **Encoding**: UTF-8 explicitly specified in file operations
- **Path Handling**: Uses `pathlib.Path` for cross-platform compatibility

## Documentation Style
- **Korean Comments**: Project uses Korean for user-facing strings and comments
- **English Code**: Function/variable names in English
- **Docstring Format**: 
  ```python
  """
  Brief description
  
  Args:
      param_name: Parameter description
  
  Returns:
      Return description
  """
  ```

## Project Structure Conventions
- `src/` - Source code modules
- `config/` - Configuration files (JSON)
- `tests/` - All testing code
- `examples/` - Usage examples and demos
- `docs/` - Documentation files

## Error Handling
- Try-catch blocks with graceful fallbacks
- Default configurations when files missing
- Descriptive error messages in Korean

## Import Organization
- Standard library imports first
- Third-party imports second  
- Local imports last
- Absolute imports preferred over relative