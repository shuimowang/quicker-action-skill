# Quicker 动作编写规范

## 设计原则

### 1. 能在 cscode 里做的就不要拆步骤

CustomWindow 的 cscode 可以在回调中做任何事（读剪贴板、操作图片、弹对话框、写文件等），不需要额外的 csscript 步骤。

**反面教材：**
- Step 0: csscript 获取剪贴板 → 变量 A
- Step 1: CustomWindow 显示变量 A → 输出变量 B/C/D/E
- Step 2: csscript 读变量 A/B/C/D/E → 裁剪保存

**正确做法：**
- Step 0: 多实例检测
- Step 1: CustomWindow（cscode 内部完成获取、显示、裁剪、保存）

步骤间变量传递有成本（类型转换、对齐），能避免就避免。

### 2. 只有多实例检测必须是独立步骤

GetWindows + simpleIf 必须在窗口创建前执行，无法放进 cscode。

### 3. 不要滥用 C# 脚本

能用内置步骤 + 表达式 `$=` 解决的，不写 C#。C# 只用于：
- 剪贴板、图片像素操作
- Win32 API / 外部 DLL
- 复杂对象构建
- 内置步骤无法覆盖的场景

### 4. 变量最小化

- 不需要在步骤间传递的数据，用 cscode 局部变量（`static` 字段）
- 需要跨步骤传递的才定义为动作变量
- `SaveState: true` 仅用于需要持久化的配置

---

## CustomWindow 规范

### 多实例处理（必须）

每个使用 CustomWindow 的动作都必须处理多实例。标准模式：

```
Step 0: sys:customwindow (GetWindows) → windowList
Step 1: sys:simpleIf {windowList}.Any()
  IfSteps:
    - sys:customwindow (Close) 关闭旧窗口
    - sys:stop 退出
Step 2: sys:customwindow (ShowAndWaitClose) 主窗口
```

### windowId

统一用 `$=_context.ActionId`，确保同一动作的窗口共享 ID。

### XAML 规范

- `xmlns:qk="https://getquicker.net"` 仅在使用 qk: 前缀控件（如 `qk:IconControl`）时才需要声明
- 不写 `x:Class`
- 不写 `WindowStartupLocation`（由 `winLocation` 参数控制）
- 事件绑定在 cscode 中用 `+=`，不写 XAML 字符串绑定
- 按钮操作优先用 `Tag` 属性 + `OnButtonClicked` 分发
- `Style` 必须用 `StaticResource`

### cscode 规范

- 必须有 `OnWindowCreated`
- C# 5.0 语法：无 `$""`、无 `?.`、无 `=>` 表达式体
- 命名空间冲突必须全限定：`System.Windows.Controls.Image`、`System.Windows.Shapes.Rectangle`、`System.Drawing.Bitmap`
- 不要同时 import `System.Drawing` 和 `System.Windows.Controls`/`System.Windows.Shapes` 而不加限定

### 通知方式

cscode 中推荐用 `AppHelper`（`using Quicker.Utilities`）做 Toast 通知，不阻塞：

```csharp
using Quicker.Utilities;
AppHelper.ShowError("错误消息", false);   // 第二个参数 false 避免阻塞
AppHelper.ShowSuccess("成功消息");
AppHelper.ShowWarning("警告消息");
AppHelper.ShowInformation("提示消息");
```

`MessageBox.Show` 用于需要用户做选择（Yes/No）或其他需要阻塞等确认的场景。

### dataMapping

- 窗口需要读动作变量时才用 dataMapping
- 窗口内部产生的数据不需要通过 dataMapping 传出（cscode 直接处理）

---

## 变量类型对照

C# 脚本中读写变量必须用正确的 .NET 类型：

| VarType | .NET 类型 |
|---------|-----------|
| 3 | `System.Drawing.Bitmap` |
| 10 | `System.Collections.Generic.Dictionary<string, object>` |
| 13 | `System.Data.DataTable` |

**Bitmap 变量注意事项：**
- 剪贴板 `Clipboard.GetImage()` 返回 WPF `BitmapSource`，存入变量前需用 `CopyPixels` + `LockBits` 转为 `System.Drawing.Bitmap`
- cscode 中需要在 WPF Image 控件显示 Bitmap 变量时，用 `ToBitmapSource()` 转换（Bitmap → MemoryStream → BitmapImage）
- cscode 内部用 `static Bitmap` 字段持有数据，不要通过动作变量传递

---

## 步骤结构规范

### InputParams / OutputParams

必须是**对象（字典）**，不是数组：
```json
"InputParams": {"参数名": {"VarKey": null, "Value": "值"}}
"OutputParams": {"输出名": "变量名"}
```

### 每个 Step 必须有 `Id`（GUID 字符串）

### 顶层字段必须完整

ActionType=24，包含全部字段：Row, Col, ActionType, Title, Description, Icon, Path, DelayMs, Data, Data2, Data3, Children, Id, TemplateId, TemplateRevision, UseTemplate, LastEditTimeUtc, SharedActionId, ShareTimeUtc, CreateTimeUtc, AsSubProgram, SkipWhenStopRunningActions, SkipCheckUpdate, AutoUpdate, KeepInfoWhenUpdate, MinQuickerVersion, ContextMenuData, AllowScrollTrigger, EnableEvaluateVariable, IsTextProcessor, IsImageProcessor, Association, DoNotClosePanel, UserLimitation

### Variable 字段必须完整

Key, IsLocked, Type, Desc, DefaultValue, SaveState, IsInput, IsOutput, ParamName, InputParamInfo, OutputParamInfo, TableDef, CustomType, Group

---

## 复查清单

生成动作后，逐条检查：

### 结构
- [ ] ActionType = 24
- [ ] 顶层字段完整（34 个）
- [ ] Data 是合法的 JSON 字符串
- [ ] 每个 Step 有 Id
- [ ] 每个 Variable 字段完整
- [ ] InputParams / OutputParams 是字典，不是数组

### CustomWindow
- [ ] 有多实例检测（GetWindows + simpleIf + Close + stop）
- [ ] windowId 用 `$=_context.ActionId`
- [ ] 使用 qk: 控件时声明了 `xmlns:qk`，未使用时不强制
- [ ] XAML 无 `x:Class`、无 `WindowStartupLocation`
- [ ] 事件在 cscode 中绑定，不写 XAML 字符串绑定

### C# 代码
- [ ] 无 C# 5.0 禁止语法（`$""`、`?.`、`=>` 表达式体、`nameof()`）
- [ ] 命名空间冲突已全限定（Image、Rectangle、Bitmap、Point、Path）
- [ ] 无重复 `using` 声明
- [ ] Image 变量用 `System.Drawing.Bitmap`，不用 `BitmapSource`
- [ ] Clipboard.GetImage() 返回的 BitmapSource 存入变量前已转换

### 设计
- [ ] 能在 cscode 做的事没有拆成额外步骤
- [ ] 变量数量最小化（只定义需要跨步骤传递的）
- [ ] 没有多余的 csscript 步骤
