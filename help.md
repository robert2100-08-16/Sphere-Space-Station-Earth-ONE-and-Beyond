# Git Issues

## Long Filename Error

If you encounter the error "filename too long" while pulling the repository, follow these steps:

1. Open a terminal/shell as administrator (Windows) or use sudo (Linux/Mac)
2. Run the following command:
   ```bash
   git config --system core.longpaths true
   ```
3. Try your git operation again

This setting enables support for long file paths in Git, which is especially important for Windows systems. 