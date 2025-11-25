# ENVIRONMENT CONFIGURATION

## System Information

### **Shell Environment**
- **Primary Shell**: PowerShell (Windows)
- **Operating System**: Windows
- **Platform**: win32

### **Command Syntax Requirements**

#### **PowerShell-Specific Commands**
When providing shell commands, use PowerShell syntax:

```powershell
# List files
Get-ChildItem

# Remove file
Remove-Item file.txt

# Remove directory
Remove-Item -Recurse -Force dir

# Copy file
Copy-Item source.txt destination.txt

# Copy directory
Copy-Item -Recurse source destination

# Create directory
New-Item -ItemType Directory -Path dir

# View file content
Get-Content file.txt

# Find in files
Select-String -Path *.txt -Pattern "search"

# Command separator
; (Always use ; not &&)
```

#### **DO NOT Use Unix/Bash Commands**
- ❌ `ls` → Use `Get-ChildItem` or `dir`
- ❌ `rm` → Use `Remove-Item` or `del`
- ❌ `cp` → Use `Copy-Item` or `copy`
- ❌ `cat` → Use `Get-Content` or `type`
- ❌ `&&` → Use `;` for command chaining

### **Character Encoding & Display Issues**

#### **CRITICAL: Emoji Restrictions**
- **CONSTRAINT**: DO NOT use emojis in any code, scripts, or output that will be executed in PowerShell
- **REASON**: PowerShell has encoding issues with Unicode emojis that cause display and execution problems
- **APPLIES TO**: 
  - Python scripts
  - Shell commands
  - File content that will be displayed in terminal
  - Error messages in code
  - Comments in code files

#### **Safe for Documentation Only**
Emojis are acceptable ONLY in:
- Markdown documentation files (like this one)
- README files
- Planning documents
- Any file that won't be executed or displayed in PowerShell

#### **Examples of Violations**

❌ **WRONG** (Python script with emoji):
```python
print("✅ Test passed!")
print("❌ Test failed!")
```

✅ **CORRECT** (Python script without emoji):
```python
print("[PASS] Test passed!")
print("[FAIL] Test failed!")
```

❌ **WRONG** (PowerShell command with emoji):
```powershell
Write-Host "🚀 Starting application..."
```

✅ **CORRECT** (PowerShell command without emoji):
```powershell
Write-Host "[START] Starting application..."
```

### **Text Alternatives for Common Emojis**

Use these text alternatives in code and scripts:

| Emoji | Text Alternative |
|-------|-----------------|
| ✅ | [PASS], [OK], [SUCCESS] |
| ❌ | [FAIL], [ERROR], [FAILED] |
| ⚠️ | [WARN], [WARNING] |
| 🚀 | [START], [LAUNCH] |
| 🔧 | [FIX], [REPAIR] |
| 📊 | [DATA], [STATS] |
| 🎯 | [TARGET], [GOAL] |
| 💡 | [INFO], [TIP] |
| 🔍 | [SEARCH], [FIND] |
| 📝 | [NOTE], [DOC] |

### **Python Environment**

#### **Package Manager**
- **Primary**: `uv` (modern Python package manager)
- **Fallback**: `pip`

#### **Virtual Environment Activation**
```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# If execution policy blocks it:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **Common Python Commands**
```powershell
# Install dependencies
pip install -r requirements.txt

# Using uv
uv sync

# Run application
python streamlit_app.py

# Run tests
python test_dashboard.py
pytest tests/
```

### **File Path Conventions**

#### **Path Separators**
- Use backslash `\` for Windows paths in documentation
- Python code should use forward slash `/` or `os.path.join()` for cross-platform compatibility
- PowerShell accepts both `\` and `/` but `\` is preferred

#### **Examples**
```powershell
# PowerShell paths
.\src\calculations\performance.py
.venv\Scripts\Activate.ps1

# Python code (cross-platform)
"src/calculations/performance.py"
os.path.join("src", "calculations", "performance.py")
```

### **Execution Constraints**

#### **What AI Can Execute**
- PowerShell commands via `executePwsh` tool
- File operations (read, write, edit)
- Git commands

#### **What AI Cannot Execute**
- Python code directly (must ask user to run)
- Interactive applications (Streamlit, Jupyter)
- Long-running processes (development servers)

#### **When Providing Code to Execute**
- Always specify it's for user to run: "Please run this in your PowerShell terminal:"
- Provide complete, copy-paste ready commands
- Include any necessary setup steps
- Warn about long-running processes

### **Common Pitfalls to Avoid**

1. **Using Unix commands** - Always use PowerShell equivalents
2. **Emojis in code** - Use text alternatives like [PASS], [FAIL]
3. **Assuming bash syntax** - PowerShell has different operators and syntax
4. **Wrong path separators** - Use `\` for Windows paths in PowerShell
5. **Trying to execute Python directly** - Always ask user to run Python code

### **Environment Verification**

Before starting work, AI should verify:
- [ ] Using PowerShell command syntax
- [ ] No emojis in any code or scripts
- [ ] Correct path separators for Windows
- [ ] Clear about what user needs to execute vs. what AI can execute
- [ ] Text alternatives used instead of emojis in output

---

## Quick Reference

**Shell**: PowerShell (Windows)  
**Python Package Manager**: uv / pip  
**Path Separator**: `\` (backslash)  
**Emoji Policy**: ❌ Never in code/scripts, ✅ OK in documentation  
**Command Chaining**: `;` (semicolon, not `&&`)
