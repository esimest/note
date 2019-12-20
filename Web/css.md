# CSS 层叠样式

## 分类

- 内联(行内): style 属性

- 内部(文件内): style 标签

- 外部样式: link 标签引入

## 结构

```css
// 内敛样式声明
style="style1:value1;style2:value2"
// 内部样式声明
selector {attr1: style1; attr2: style2...}
```


## 选择器(selector)

### 标签选择器

### id 选择器

### 类选择器

## 样式(style)

- width: 元素的宽度

- height: 元素的高度

- background-color: 元素的背景颜色

## 长度单位

- px(像素)

- %(父元素的百分比)

- em

- ex

## 颜色表示法

- 单词表示法

- 十六进制表示法

- RGB 表示法

## 伪类选择器

> 顺序: L -> V -> H -> A

- :link
   > 访问前样式 (只能添加给 a 标签)

- :visited
   > 访问后的样式 (只能添加给 a 标签)

- :hover
   > 鼠标移入后的样式

- :active
   > 鼠标按下后的样式

- :after : before
   > 在元素的最前/后面添加样式和文本

- :checked :disabled :focus
   > (针对表单元素)

## 结构性伪类选择器

- nth-of-type()
- first-of-type()
- last-of-type()
- only-of-type()
- nth-of-child()
- first-of-child()
- last-of-child()
- only-of-child()

## 样式继承

- 子元素可以继承父元素的样式
- 文字相关的样式默认是可以继承的
- 布局相关的样式默认是无法继承的，但是可以通过 `${style}: inherit` 实现布局样式的继承.

## 选择器优先级

> 当具备相同优先级时, 后设置的样式优先级高(覆盖)
> 内部样式和外部样式的优先级一样高
> 内联样式的优先级最高

- 优先级
   > `内联 > id > class > tag > *(通配) > 继承`

## CSS 盒子模型

> 所有的 HTML 元素可以当作盒子看待

组成(由内向外):

`content(内容) -> padding(内边距) -> border(边框) -> margin(外边距)`

- content: width * height

- padding: content 到 border 的距离
  > padding-left padding-right padding-top padding-bottom

- border: 边框

- margin: 盒子之间的距离.(可以为负数)