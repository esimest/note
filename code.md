# VS Code 使用技巧 与设置

- [Keyboard reference sheet](https://go.microsoft.com/fwlink/?linkid=832145)
  > Ctrl + Shift + P  --> >Help: Keyboard Shortcuts Preferences

- 按键优先级 Ctrl > Shift > Alt > Enter

- 块注释快捷键改为：Ctrl + Shift + /

- 代码片段 (code snippet)

## User Settings

```json
{
    "workbench.colorTheme": "Solarized Dark",
    "terminal.integrated.shell.windows": "C:\\Program Files\\Git\\bin\\bash.exe",
    "editor.minimap.enabled": false,
    "explorer.confirmDragAndDrop": false,
    "explorer.confirmDelete": false,
    "git.autofetch": true,
    "window.zoomLevel": 1,
    "git.enableSmartCommit": true,
    "editor.cursorStyle": "block-outline",
    "editor.cursorSmoothCaretAnimation": true,
    "editor.cursorBlinking": "smooth",
    "editor.find.addExtraSpaceOnTop": false,
    "editor.find.autoFindInSelection": true,
    "editor.formatOnPaste": true,
    "editor.formatOnSave": true,
    "workbench.iconTheme": "vscode-icons",
    "python.pythonPath": "ipython",
    "python.dataScience.enabled": false,
    "python.linting.pylintEnabled": false,
    "python.testing.debugPort": 30000,
    "python.testing.pyTestEnabled": true,
    "python.autoComplete.addBrackets": true,
    "python.linting.pep8Enabled": true,
    "python.terminal.executeInFileDir": true,
    "python.testing.unittestEnabled": true,
    "python.venvPath": "${workspaceFolder}/.venv",
    "python.globalModuleInstallation": true,
    "zenMode.centerLayout": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/*.docx": true,
        "**/*.exe": true,
        "**/*.tar.gz": true,
        "**/*.zip": true,
        "**/*rar": true
    },
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "workbench.activityBar.visible": false,
    "workbench.statusBar.feedback.visible": false,
    "editor.wordWrap": "on",
    "workbench.statusBar.visible": true,
    "C_Cpp.updateChannel": "Insiders",
    "editor.fontSize": 16,
    "zenMode.hideLineNumbers": false,
    "zenMode.hideTabs": false,
    "python.linting.enabled": false,
    "diffEditor.ignoreTrimWhitespace": false,
}

```

## Python Settings

```shell
pip install ipython, autopep8, pep8, pytest, rope
```
