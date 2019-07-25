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
    "editor.wordWrap": "on", // 切换自动换行 Alt + Z
    "workbench.statusBar.visible": true,
    "C_Cpp.updateChannel": "Insiders",
    "editor.fontSize": 16,
    "zenMode.hideLineNumbers": false,
    "zenMode.hideTabs": false,
    "python.linting.enabled": false,
    "diffEditor.ignoreTrimWhitespace": false,
}

```

## Code User Settings

```json
{
    "workbench.colorTheme": "Solarized Dark",
    "terminal.integrated.shell.windows": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
    "explorer.confirmDragAndDrop": false,
    "explorer.confirmDelete": false,
    "git.autofetch": true,
    "window.zoomLevel": 2,
    "git.enableSmartCommit": true,
    "editor.cursorStyle": "block-outline",
    "editor.cursorSmoothCaretAnimation": true,
    "editor.cursorBlinking": "smooth",
    "editor.find.addExtraSpaceOnTop": true,
    "editor.find.autoFindInSelection": true,
    "workbench.iconTheme": "vscode-icons",
    "python.pythonPath": "ipython",
    "python.dataScience.enabled": false,
    "python.terminal.executeInFileDir": true,
    "python.globalModuleInstallation": true,
    "zenMode.centerLayout": false,
    "files.exclude": {
        "**/*.docx": true,
        "**/*.exe": true,
        "**/*.tar.gz": true,
        "**/*.zip": true,
        "**/*.rar": true,
        "**/*.xlsx": true,
        "**/*.xlsm": true,
        "**/*.in": true,
        "**/*.ac": true,
        "**/*.pyc": true,
    },
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "workbench.activityBar.visible": false,
    "editor.wordWrap": "on",
    "workbench.statusBar.visible": true,
    "C_Cpp.updateChannel": "Insiders",
    "editor.fontSize": 16,
    "zenMode.hideLineNumbers": false,
    "zenMode.hideTabs": false,
    "diffEditor.ignoreTrimWhitespace": false,
    "maven.terminal.useJavaHome": true,
    "editor.suggestSelection": "first",
    "vsintellicode.modify.editor.suggestSelection": "automaticallyOverrodeDefaultValue",
    "git.confirmSync": false,
    // 默认：`~!@#$%^&*()-=+[{]}\|;:'",.<>/?
    // "editor.wordSeparators": " ",
    "search.usePCRE2": true,
    "editor.minimap.enabled": false,
    "editor.largeFileOptimizations": false,
    "python.analysis.memory.keepLibraryAst": true,
    "python.analysis.memory.keepLibraryLocalVariables": true,
    "python.diagnostics.sourceMapsEnabled": false,
    "python.disableInstallationCheck": true,
    "python.linting.pep8Enabled": true,
    "python.linting.pylintEnabled": false,
    "python.jediEnabled": false,
}

```

## Code Short User ShortCut Settings

```json
// Place your key bindings in this file to override the defaults
[
    {
        "key": "ctrl+shift+oem_2",
        "command": "editor.action.blockComment",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+a",
        "command": "-editor.action.blockComment",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+shift+l",
        "command": "workbench.action.terminal.clear",
        "when": "terminalFocus && !terminalFindWidgetVisible"
    },
    {
        "key": "ctrl+r",
        "command": "workbench.action.reloadWindow",
        "when": ""
    },
    {
        "key": "ctrl+f12",
        "command": "editor.action.revealDefinitionAside",
        "when": "editorHasDefinitionProvider && editorTextFocus && !isInEmbeddedEditor"
    },
    {
        "key": "f12",
        "command": "editor.action.peekDefinition",
        "when": "editorHasDefinitionProvider && editorTextFocus && !inReferenceSearchEditor && !isInEmbeddedEditor"
    },
    {
        "key": "alt+f12",
        "command": "editor.action.goToImplementation",
        "when": "editorHasImplementationProvider && editorTextFocus && !isInEmbeddedEditor"
    },
    {
        "key": "f12",
        "command": "-editor.action.revealDefinition",
        "when": "editorHasDefinitionProvider && editorTextFocus && !isInEmbeddedEditor"
    },
]
```
## Code Extensions

```python
[
    "bracket pair colorizer2",
    "C/C++",
    "C++ Intellisense",
    "DotENV",
    "Git History",
    "indent-rainbow",
    "JSON-Template",
    "markdown-formatter",
    "markdownlint",
    "Python",
    "Rainbow CSV",
    "shell-format",
    "Simple icons",
    "SynthWave'84",
    "vscode-fileheader",
    "vscode-icons",
    "vscode-mindmap",
    "vscode-pdf",
    "YAML",
    "python snippets"
]
```

## Python Settings

```shell
pip install ipython, autopep8, pep8, pytest, rope
```
