# VSCode 编辑器相关概念

![VSCode 基本布局](./hero.png)

## Editor(编辑器)

这里的编辑器指的不是 VSCode 这个软件，而是指一块可以用于编辑文本的区域。

## Group(编辑器组)

如布局图所示，Group 是 Editor 的集合，一个 Group 中可以打开一个或多个 Editor。默认布局只有一个 Group，可以通过命令或鼠标拖拽等方式创建多个 Group。

## Panel(面板)

面板包含几个子模版

- Problem(问题面板)
- OUTPT(输出面板)
- Debug Console(调试面板)
- Terminal(终端面板)

## Side Bar(侧边栏)

侧边栏属于视图栏的展开形式

### 内置视图

- Explore(资源管理器视图)
- Search(搜索视图)
- SCM(Git 视图)
- Debug(调试视图)
- Extensions(扩展视图)

### 插件视图

- Remote Explore(远程资源管理器)
- GitLens(Git 视图)
- Docker(容器管理视图)
- Kuberntes(应用编排视图)

## Vertical/Horizontal

Vertical(水平的)，指多个 Group 的排列方式为水平排列(横向扩展)
Horizontal(垂直的)，指多个 Group 的排列方式为垂直的(纵向扩展)