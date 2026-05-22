# 生成后自检清单

生成动作后，**必须逐条检查**以下问题，确认无误后再输出给用户。

## C# 命名空间冲突（最高频错误）

Quicker 自动注入的 using 包含 `System.Windows`、`System.Windows.Forms`、`System.Drawing`、`System.IO`、`System.Windows.Shapes`，以下类型**必须写全限定名**：

| 简写 | 冲突 | 正确写法 |
|------|------|----------|
| `Rectangle` | `System.Drawing` vs `System.Windows.Shapes` | 按用途写全名 |
| `ListBox` | `System.Windows.Controls` vs `System.Windows.Forms` | 按用途写全名 |
| `Path` | `System.IO` vs `System.Windows.Shapes` | `System.IO.Path` |
| `Control` | `System.Windows.Controls` vs `System.Windows.Forms` | 按用途写全名 |
| `NotifyIcon` | `System.Windows.Forms` | `System.Windows.Forms.NotifyIcon` |
| `DialogResult` | `System.Windows.Forms` | `System.Windows.Forms.DialogResult` |
| `Bitmap` | `System.Drawing` | `System.Drawing.Bitmap` |
| `SolidBrush` | `System.Drawing` | `System.Drawing.SolidBrush` |
| `Pen` | `System.Drawing` | `System.Drawing.Pen` |
| `Font` | `System.Drawing` | `System.Drawing.Font` |
| `Form` | `System.Windows.Forms` | `System.Windows.Forms.Form` |
| `Point` | `System.Drawing` vs `System.Windows` | 按用途写全名 |

**规则：只要同时 using 了 `System.Windows` 和 `System.Windows.Forms`/`System.Drawing`，所有有歧义的类型一律写全名。**

## C# 变量与语法

- **`var` 不允许多声明**：`var a = 1, b = 2;` 是错的，必须拆成 `var a = 1; var b = 2;`
- **同一方法内变量名不能重复**：检查所有局部变量名在方法内是否唯一
- **类型别名不存在**：不要用 `F<Tb>` 这种自造别名，直接写 `F<TextBox>`
- **跨类访问**：方法必须是 `public static`
- **删除未使用的字段/变量**

## XAML

- **Style 必须用 StaticResource**：`Style="{StaticResource Key}"`，不能写 `Style="{Key}"`
- **同一控件不能有重复属性**：特别是 `Text=` 同时有默认值和 Binding 的情况，只能保留一个
- **文件图标绑定**：`qk:IconControl` 需要 `icon:.txt` 格式，不能绑定完整路径

## 性能

- **避免逐像素 GetPixel**：用 `BitBlt` + `GetBitmapBits` 批量读取
- **Timer 间隔**：不低于 30ms，30-50ms 为宜

## 验证流程

1. 生成 Python 脚本
2. 运行脚本生成 JSON
3. 从 JSON 中提取 cscode 和 XAML
4. 用正则扫描 cscode：检查未限定的冲突类型名、`var` 多声明、重复变量名
5. 用正则扫描 XAML：检查 `Style="{` 非 StaticResource、重复属性
6. 修复所有问题后重新生成，再次验证直到无问题
