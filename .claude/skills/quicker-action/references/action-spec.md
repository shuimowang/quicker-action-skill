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

### 2. 多实例检测放在窗口创建前

默认将 `LimitSingleInstance` 设为 `false`，不要依赖动作级单实例限制。需要限制 CustomWindow 数量时，`GetWindows + simpleIf` 必须在窗口创建前执行，无法放进 cscode。

### 3. 不要滥用 C# 脚本

能用内置步骤 + 表达式 `$=` 解决的，不写 C#。C# 只用于：
- 剪贴板、图片像素操作
- Win32 API / 外部 DLL
- 复杂对象构建
- 内置步骤无法覆盖的场景

### 4. 代码可读性

JSON 字符串中嵌入的 XAML、C# 代码必须用 `\n` 换行 + 缩进，不能挤成一行。

- **XAML**：每个属性独立一行或合理换行，子元素缩进 4 空格，添加注释分组（如 `<!-- 标题栏 -->`）
- **C# 代码**：保持正常代码格式，语句换行、花括号缩进
- **cscode** 已经用 `\n` 的保持不变；XAML 同样用 `\n` 而非拼成一行

**反面教材：**
```
"Value": "<Window xmlns=\"...\" Width=\"300\" Height=\"360\" WindowStyle=\"None\"><Grid><Grid.RowDefinitions><RowDefinition Height=\"28\"/><RowDefinition Height=\"*\"/></Grid.RowDefinitions>..."
```

**正确做法：**
```
"Value": "<Window xmlns=\"...\"\n        Width=\"300\" Height=\"360\"\n        WindowStyle=\"None\">\n    <Grid>\n        <Grid.RowDefinitions>\n            <RowDefinition Height=\"28\"/>\n            <RowDefinition Height=\"*\"/>\n        </Grid.RowDefinitions>\n..."
```

### 5. 变量最小化

- 不需要在步骤间传递的数据，用 cscode 局部变量（`static` 字段）
- 需要跨步骤传递的才定义为动作变量
- `SaveState: true` 仅用于需要持久化的配置

### 6. 所有步骤变量必须先在 Variables 中声明

除 Quicker 内置变量（如 `quicker_in_param`）外，步骤使用的每个动作变量都必须先在当前程序或子程序的 `Variables` 中声明。检查范围包括：

- `OutputParams` 中非 `null` 的目标变量
- `InputParams` 中非空的 `VarKey`
- `$={varName}` 表达式引用
- `$$...{varName}` 文本插值引用
- CustomWindow `dataMapping` 中引用的动作变量

`OutputParams` 是步骤的**输出变量词典**。key 是步骤模块定义的输出名，value 是你要存入的变量名。

```
"OutputParams": {
  "windowList": "windowList"
  ↑ 模块输出名     ↑ 存入哪个变量
}
```

这表示"把步骤的 `windowList` 输出存到名为 `windowList` 的变量中"。**这个变量必须在 `Variables` 数组中有定义，否则输出无处可存。**

**反面教材：**
```json
"Variables": [],   // ← 没有声明 windowList
"Steps": [{
  "StepRunnerKey": "sys:customwindow",
  "OutputParams": { "windowList": "windowList" }   // 输出到哪？变量不存在！
}, {
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": { "condition": "$={windowList}.Any()" }   // 读取为空！
}]
```

**正确做法：**
```json
"Variables": [
  { "Key": "windowList", "Type": 99, ... }   // 先声明变量
],
"Steps": [{
  "StepRunnerKey": "sys:customwindow",
  "OutputParams": { "windowList": "windowList" }   // 输出到已声明的变量
}, {
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": { "condition": "$={windowList}.Any()" }   // 正常读取
}]
```

**强制生成顺序：**

1. 先设计全部步骤。
2. 扫描上述五类变量使用位置，生成变量清单。
3. 先写完整的 `Variables` 数组。
4. 再写 `Steps`。
5. 最后反向扫描一次，确保不存在未声明引用。

不能先写步骤、最后凭记忆补变量。

### 7. 不要臆想不存在的步骤

`modules.md` 是常用模块速查，不是 Quicker 全部模块的白名单。不要凭记忆或想象编造模块名。

**常见臆想：**
- `sys:closeWindow` → 不存在，关闭窗口用 `sys:customwindow`（`type = "Close"`）
- `sys:messageBox` → 不存在，显示文本用 `sys:showText`
- `sys:inputBox` → 不存在，用户输入用 `sys:form`
- `sys:clipboard` → 不存在；应查询官方模块中的剪贴板读写模块，或在确需窗口内部处理时使用 cscode

**正确做法：** 优先查 [常用模块速查](modules.md)。未收录的模块继续查 Quicker 官方文档或从本机已有动作导出 JSON，核对真实的 `StepRunnerKey`、`InputParams` 和 `OutputParams`。只有经过其中一种方式确认后才能使用。

---

## CustomWindow 规范

### 多实例处理

一般将 `LimitSingleInstance` 设为 `false`。对于不允许重复打开的 CustomWindow，应显式处理多实例；若需求明确允许多个窗口，可以省略检测，但应使用可区分的 `windowId`。标准单窗口模式：

```
Variables: 先声明 windowList（Type=99）
Step 0: sys:customwindow (GetWindows) → windowList
Step 1: sys:simpleIf {windowList}.Any()
  IfSteps:
    - sys:customwindow (Close) 关闭旧窗口
    - sys:stop 退出
Step 2: sys:customwindow (Show) 主窗口
```

只要使用 `GetWindows → windowList`，就必须先在同一作用域的 `Variables` 中加入：

```json
{
  "Key": "windowList",
  "IsLocked": false,
  "Type": 99,
  "Desc": "已打开的自定义窗口列表",
  "DefaultValue": "",
  "SaveState": false,
  "IsInput": false,
  "IsOutput": false,
  "ParamName": "",
  "InputParamInfo": null,
  "OutputParamInfo": null,
  "TableDef": null,
  "CustomType": null,
  "Group": "窗口"
}
```

### windowId

单窗口动作默认用 `$=_context.ActionId`。同一动作需要同时显示多个窗口时，在动作 ID 后附加稳定后缀，例如 `$=_context.ActionId + ":settings"`。

### Show 与 ShowAndWaitClose

- CustomWindow 是动作的最后一个步骤，关闭窗口后没有任何后续逻辑时，默认使用 `Show`。它不会让动作执行线程一直等待窗口关闭，更方便调试、重新运行和更新动作。
- 只有窗口关闭后还要继续执行步骤、读取 `result` / `windowLocation`、或必须让动作生命周期覆盖窗口生命周期时，才使用 `ShowAndWaitClose`。
- 不要因为“主窗口”就默认选择 `ShowAndWaitClose`；应根据关闭后是否还有工作来决定。

### XAML 规范

- `xmlns:qk="https://getquicker.net"` 仅在使用 qk: 前缀控件（如 `qk:IconControl`）时才需要声明
- 不写 `x:Class`
- 不写 `WindowStartupLocation`（由 `winLocation` 参数控制）
- 事件绑定在 cscode 中处理，不写 XAML 字符串绑定
- 静态命令按钮优先用 `Tag` + `OnButtonClicked` 分发；右键、长按、拖拽、文本变化、动态控件等场景用 `+=` 绑定对应事件
- `Style` 必须用 `StaticResource`

### cscode 规范

- 不需要辅助 C# 时，`cscode` 设为空字符串
- 只要 `cscode` 写了 C# 代码，就必须定义 `OnWindowCreated`，即使方法体为空
- cscode 按 C# 5.0 语法编写，详见 [C# 规则](csharp-rules.md)
- **命名空间冲突检查（写 cscode 前必须核对）：** cscode 是完整 C# 代码，有 `using` 开头，多个命名空间同时引入时同名类型会冲突。常见冲突类型：
  - `Point` → `System.Windows.Point` 或 `System.Drawing.Point`
  - `Bitmap` → `System.Drawing.Bitmap`
  - `Image` → `System.Windows.Controls.Image` 或 `System.Drawing.Image`
  - 其他冲突类型详见 [C# 规则](csharp-rules.md)
- **只要代码中同时出现两组命名空间的类型，所有有歧义的类型一律写全名，不要依赖短名称**

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
- [ ] 每个 Variable 字段完整
- [ ] 词典变量的 DefaultValue 直接写 JSON，如 `{"key":"value"}`，不添加 `json:` 前缀
- [ ] InputParams / OutputParams 是字典，不是数组
- [ ] OutputParams 的 value 对应的变量已在 Variables 中声明（每写一个 OutputParams 就检查一次）
- [ ] InputParams 的非空 VarKey 对应的变量已声明
- [ ] `$={varName}` 表达式和 `$$...{varName}` 插值引用的变量已声明
- [ ] CustomWindow dataMapping 引用的动作变量已声明
- [ ] 手动使用 GetWindows 时已声明 Type=99 的 `windowList`

### 导入与更新
- [ ] 新动作校验后已调用 `create`，并收到 `已安装，动作Id：...`
- [ ] 已有动作通过 `info` 获取原 JSON，保留顶层 `Id`，修改后调用 `update`
- [ ] 修改已有动作时没有调用 `create`
- [ ] 通信失败时没有误报“已导入”或“已更新”

### CustomWindow
- [ ] `LimitSingleInstance = false`
- [ ] 不允许重复打开时，有显式多实例处理；允许多窗口时，`windowId` 能区分窗口
- [ ] 单窗口的 windowId 用 `$=_context.ActionId`；多窗口使用动作 ID 加稳定后缀
- [ ] CustomWindow 后无后续步骤时使用 `Show`；只有需要等待关闭后继续处理时才用 `ShowAndWaitClose`
- [ ] 使用 qk: 控件时声明了 `xmlns:qk`，未使用时不强制
- [ ] XAML 无 `x:Class`、无 `WindowStartupLocation`
- [ ] 事件在 cscode 中绑定，不写 XAML 字符串绑定

### C# 代码
- [ ] cscode 和 `sys:csscript` v1（`normal` / `low_permission`）无 C# 5.0 禁止语法
- [ ] `sys:csscript` v2（`normal_roslyn` / `low_permission_roslyn`）按 Roslyn/C# 7.3 规则检查，不套用 C# 5.0 禁止清单
- [ ] 非空 cscode 中定义了 `OnWindowCreated`
- [ ] 命名空间冲突已全限定 — cscode/csscript 有 `using` 开头，多命名空间同时引入时同名类型会冲突，有歧义的类型（`Point`、`Bitmap`、`Image` 等）一律写全名
- [ ] 无重复 `using` 声明
- [ ] Bitmap 变量用 `System.Drawing.Bitmap`，不用 `BitmapSource`
- [ ] Clipboard.GetImage() 返回的 BitmapSource 存入变量前已转换

### 设计
- [ ] JSON 字符串中的 XAML / C# 代码已用 `\n` 换行缩进，非挤成一行
- [ ] 能在 cscode 做的事没有拆成额外步骤
- [ ] 变量数量最小化（只定义需要跨步骤传递的）
- [ ] 没有多余的 csscript 步骤
- [ ] 所有 StepRunnerKey 都经过常用模块文档、Quicker 官方文档或真实导出动作确认，无臆想步骤
