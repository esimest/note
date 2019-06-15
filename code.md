# VS Code 使用技巧 与设置

- [Keyboard reference sheet](https://go.microsoft.com/fwlink/?linkid=832145)
  > Ctrl + Shift + P  --> >Help: Keyboard Shortcuts Preferences

- 按键优先级 Ctrl > Shift > Alt > Enter

- 块注释快捷键改为：Ctrl + Shift + /

- 代码片段 (code snippet)

## User Settings

```json
{
    "editor.minimap.enabled": false,
    "workbench.colorTheme": "Atom One Light",   // 需要下载 atom one light 插件
    "terminal.integrated.shell.windows": "bash.exe",
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
    "workbench.iconTheme": "vscode-icons",   // 需要下载 vscode-icons 插件
}
```

## Python Settings

```json
"[python]": {
    "python.pythonPath": "ipython",              // python 路径
    "python.dataScience.enabled": false,         // 关闭 dataScience(jupyter) 功能
    "python.linting.pylintEnabled": false,       // 打开格式检测功能
    "python.testing.debugPort": 30000,           // 设置 python 代码调试端口 30000
    "python.autoComplete.addBrackets": true,     // 函数自动添加括号
    "python.autoComplete.extraPaths": true,      // 对目录中 python 包添加自动补全功能
    "python.linting.pep8Enabled": true,          // 使用 pep8 检测代码格式
    "python.terminal.executeInFileDir": true,    // 打开终端的路径设置为文件的绝对路径
    "python.testing.pyTestEnabled": true,        // 开启 pytest 测试框架
    "python.testing.unittestEnabled": true,      // 开启 unittest 测试框架
    "python.venvPath": "${workspaceFolder}/.venv",                  // 虚拟环境路径
}
```

```shell
pip install ipython, autopep8, pep8, pytest, rope
```
