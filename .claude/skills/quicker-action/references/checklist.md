# C# 语法自检

结构和设计层面的检查见 [动作编写规范 - 复查清单](action-spec.md#复查清单)。本文档聚焦 C# 语法细节。

## 命名空间冲突（最高频错误）

Quicker 自动注入的 using 包含 `System.Windows`、`System.Windows.Forms`、`System.Drawing`、`System.IO`、`System.Windows.Shapes`，以下类型**必须写全限定名**：

| 简写 | 冲突 | 正确写法 |
|------|------|----------|
| `Rectangle` | `System.Drawing` vs `System.Windows.Shapes` | 按用途写全名 |
| `ListBox` | `System.Windows.Controls` vs `System.Windows.Forms` | 按用途写全名 |
| `Path` | `System.IO` vs `System.Windows.Shapes` | `System.IO.Path` |
| `Control` | `System.Windows.Controls` vs `System.Windows.Forms` | 按用途写全名 |
| `Image` | `System.Drawing` vs `System.Windows.Controls` | 按用途写全名 |
| `Bitmap` | `System.Drawing` | `System.Drawing.Bitmap` |
| `Point` | `System.Drawing` vs `System.Windows` | 按用途写全名 |
| `SolidBrush` | `System.Drawing` | `System.Drawing.SolidBrush` |
| `Pen` | `System.Drawing` | `System.Drawing.Pen` |
| `Font` | `System.Drawing` | `System.Drawing.Font` |
| `Form` | `System.Windows.Forms` | `System.Windows.Forms.Form` |
| `DialogResult` | `System.Windows.Forms` | `System.Windows.Forms.DialogResult` |

**规则：只要同时 using 了 `System.Windows` 和 `System.Windows.Forms`/`System.Drawing`，所有有歧义的类型一律写全名。**

## C# 5.0 禁止语法

- `$""` 字符串插值 → 用 `string.Format("{0}", arg)`
- `?.` null 条件运算符 → 用 `if (x != null) x.Method()`
- `=>` 表达式体成员 → 用完整 `{ get { return 1; } }`（lambda 允许）
- `nameof()` → 用字符串字面量
- `is Type var` 模式匹配 → 用 `as` + null 检查

## 变量与语法

- `var` 不允许多声明：`var a = 1, b = 2;` 必须拆成 `var a = 1; var b = 2;`
- 同一方法内变量名不能重复
- 跨类方法必须 `public static`
- 删除未使用的字段/变量

## XAML

- Style 必须用 `StaticResource`
- 同一控件不能有重复属性
- 文件图标绑定用 `icon:.txt` 格式
