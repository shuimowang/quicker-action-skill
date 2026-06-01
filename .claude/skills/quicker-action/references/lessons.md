# Quicker 动作开发关键经验

## 表达式前缀

| 前缀 | 类型 | 用途 |
|------|------|------|
| `$$` | 插值 | 字符串拼接，变量被替换为值 |
| `$=` | 表达式 | C# 代码，可计算和逻辑判断 |

## 词典访问语法

- **插值中**：`$${config.key}`
- **表达式中**：`$={config}["key"]`

## InputParams 变量使用

不能直接用 `{varName}`，必须：
- `$={varName}` 或
- `VarKey: "varName"`

## C# 5.0 限制

Quicker 只支持 C# 5.0，不能使用：
- 模式匹配：`if (child is Button btn)` ❌
- 字符串插值：`$"..."` ❌
- 空条件运算符：`?.` ❌

正确写法：
```csharp
if (child is Button) {
    var btn = (Button)child;
    // ...
}
```

## XAML 资源规范

1. `Window.Resources` 必须在使用前定义
2. 不能重复定义 `Window.Resources`
3. 使用 `StaticResource` 必须在资源定义之后

## 必要的 using 指令

```csharp
using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;  // UniformGrid
using Quicker.Utilities;                    // AppHelper
using Quicker.Public;                       // ICustomWindowContext
using System.Collections.Generic;           // IDictionary
```
