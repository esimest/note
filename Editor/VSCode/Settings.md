# VS Code 使用技巧 与设置

- [Keyboard reference sheet](https://go.microsoft.com/fwlink/?linkid=832145)
  > Ctrl + Shift + P  --> >Help: Keyboard Shortcuts Preferences

- 按键优先级 Ctrl > Shift > Alt > Enter

- 块注释快捷键改为：Ctrl + Shift + /

- 代码片段 (code snippet)

## 迁移 VSCode

1. 下载最新版 VSCode 安装程序，按流程安装
2. 将源主机的 %APPDATA%/Code, %USERPROFILE%/.vscode/extensions
   拷贝至目标主机同名目录

## Code User Settings

```json
{
    "terminal.integrated.shell.windows": "bash.exe",
    "explorer.confirmDragAndDrop": false,
    "explorer.confirmDelete": false,
    "git.autofetch": true,
    "window.zoomLevel": 1,
    "git.enableSmartCommit": true,
    "editor.cursorStyle": "block-outline",
    "editor.cursorSmoothCaretAnimation": true,
    "editor.cursorBlinking": "smooth",
    "editor.find.addExtraSpaceOnTop": true,
    "editor.find.autoFindInSelection": true,
    "python.pythonPath": "ipython",
    "python.dataScience.enabled": false,
    "python.terminal.executeInFileDir": true,
    "python.globalModuleInstallation": true,
    "zenMode.centerLayout": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.DS_Store": false,
        "**/.pytest_cache": true,
        "**/*.doc*": true,
        "**/*.exe": true,
        "**/*.pyc": true,
        "**/*.rpm": true,
        "**/*.tar.*": true,
        "**/*.xls*": true,
        "**/*.zip": true,
        "**/*rar": true,
    },
    "files.trimTrailingWhitespace": true,
    "workbench.activityBar.visible": false,
    "editor.wordWrap": "on",
    "workbench.statusBar.visible": true,
    "C_Cpp.updateChannel": "Insiders",
    "editor.fontSize": 16,
    "zenMode.hideLineNumbers": false,
    "zenMode.hideTabs": false,
    "diffEditor.ignoreTrimWhitespace": false,
    "editor.suggestSelection": "first",
    "git.confirmSync": false,
    // 默认：`~!@#$%^&*()-=+[{]}\|;:'",.<>/?
    // "editor.wordSeparators": " ",
    "editor.minimap.enabled": false,
    "editor.largeFileOptimizations": false,
    "python.linting.pep8Enabled": true,
    "workbench.colorTheme": "Solarized Dark",
    "workbench.iconTheme": "vscode-icons",
    "terminal.integrated.rendererType": "dom",
    "python.jediPath": "jedi",
    "python.linting.pylintEnabled": false
}
```

## User ShortCut Settings

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
pip install ipython pep8 pytest rope jedi autopep8 pylint isort
```

## 配置 vscode 为 git 编辑器

`git config --global core.editor "code --wait"`

## Problems

```yaml
"Extension host terminated execptedly": "新装的插件不兼容，卸载掉即可"
```

## Go Settings

```shell
# 会影响到格式化工具对代码的自动补全(如 import/package)
go.useLanguageServer  # 甚用

# 不通的 go 设置会产生不同的 tools 列表
## 如 "go.formatTool": "goimports" 会使用 goimports 代替 goreturn

```

## JS Setting

```json
// Code 配置 jquery 语法支持
// 在项目根目录添加 jsconfig.json
{
  "exclude": ["node_modules"],
  "typeAcquisition": {
    "include": [
      "jquery"
    ]
  }
}
```

