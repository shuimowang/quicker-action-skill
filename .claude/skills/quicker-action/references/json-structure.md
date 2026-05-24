# Quicker 动作 JSON 结构

## 顶层

对应类型：`Quicker.Common.ActionItem`

```csharp
int Row                                                 // 行位置
int Col                                                 // 列位置
int ActionType                                          // 动作类型，24=普通动作
string Title                                            // 动作名称
string Description                                      // 描述
string Icon                                             // 图标（如 "fa:Solid_Star"）
string Path                                             // 路径
int DelayMs                                             // 延迟（毫秒）
string Data                                             // 主数据（JSON 字符串，XAction）
string Data2                                            // 附加数据2
string Data3                                            // 附加数据3
string Id                                               // 唯一标识（GUID）
bool AsSubProgram                                       // 是否作为子程序
bool AllowScrollTrigger                                 // 是否允许滚动触发
bool EnableEvaluateVariable                             // 是否启用变量求值
string ContextMenuData                                  // 右键菜单（多行文本）
string TemplateId                                       // 模板ID
int TemplateRevision                                    // 模板版本
bool UseTemplate                                        // 是否使用模板
string LastEditTimeUtc                                  // 最后编辑时间
string SharedActionId                                   // 共享动作ID
string ShareTimeUtc                                     // 共享时间
string CreateTimeUtc                                    // 创建时间
bool SkipWhenStopRunningActions                         // 停止运行时跳过
bool SkipCheckUpdate                                    // 跳过更新检查
bool AutoUpdate                                         // 自动更新
bool KeepInfoWhenUpdate                                 // 更新时保留信息
string MinQuickerVersion                                // 最低 Quicker 版本
bool IsTextProcessor                                    // 是否文本处理器
bool IsImageProcessor                                   // 是否图片处理器
Association Association                                  // 关联设置
bool DoNotClosePanel                                    // 不关闭面板
string UserLimitation                                   // 用户限制
```

```json
{
  "Row": 0, "Col": 0, "ActionType": 24,
  "Title": "动作名称", "Description": "描述",
  "Icon": "fa:Solid_Star", "Path": null, "DelayMs": 0,
  "Data": "{...JSON字符串...}",
  "Data2": null, "Data3": null, "Children": null,
  "Id": "GUID",
  "TemplateId": null, "TemplateRevision": 0, "UseTemplate": false,
  "LastEditTimeUtc": null, "SharedActionId": "", "ShareTimeUtc": null, "CreateTimeUtc": null,
  "AsSubProgram": false, "SkipWhenStopRunningActions": false, "SkipCheckUpdate": false,
  "AutoUpdate": true, "KeepInfoWhenUpdate": false, "MinQuickerVersion": "",
  "ContextMenuData": "", "AllowScrollTrigger": false, "EnableEvaluateVariable": false,
  "IsTextProcessor": false, "IsImageProcessor": false,
  "Association": { ... },
  "DoNotClosePanel": false, "UserLimitation": null
}
```

### ContextMenuData（右键菜单）

多行字符串，一行一个菜单项，格式：`[图标]显示文字|参数值`

```
[fa:Light_Cogs:#00A0D8]设置|Settings
[fa:Solid_Info]关于|About
```

用户点击菜单项时，动作会以参数值运行。在动作中通过 `{quicker_in_param}` 获取传递的参数。

### 内置变量

以下变量不在 Variables 列表中，可直接使用：

| 变量 | 说明 |
|------|------|
| `quicker_in_param` | 动作运行时传入的参数（右键菜单、外部调用等） |
| `_context.ActionId` | 当前动作的 Id |

## Data（JSON 字符串）

对应类型：`Quicker.Domain.Actions.X.XAction`

```json
{
  "LimitSingleInstance": false,  // 始终设为 false，多实例处理在步骤中实现
  "SummaryExpression": "$$",
  "SubPrograms": [],
  "Variables": [],
  "Steps": []
}
```

**字段定义：**

```csharp
// Quicker.Domain.Actions.X.XAction
IList<SubProgram> SubPrograms;       // 子程序列表
IList<ActionVariable> Variables;     // 动作变量列表
IList<ActionStep> Steps;             // 步骤列表
bool LimitSingleInstance;            // 是否限制单实例
```

## 图标（Icon 字段）

**动作 Icon 字段**（不带 `[]`）：

```
fa:Solid_Trash          # 矢量图标，系统颜色
fa:Solid_Pen:#FF0000    # 矢量图标，自定义颜色
```

**菜单/标题内联标记**（带 `[]`）：

```
[fa:Solid_Trash]              # 矢量图标
[fa:Solid_Pen:#FF0000]        # 自定义颜色
[url:https://example.png]     # 网络图片
[icon:.txt]                   # Windows 系统图标
```

**Font Awesome 图标库：** 内置 7000+ 图标，4 种风格：
`Solid`、`Regular`、`Light`、`Brands`。格式为 `风格_名称`。

搜索：https://fontawesome.com/icons

**图标名获取：** 面板腰栏 → 工具 → 图标库，选择后自动复制名称。

`null` 表示无图标（显示文字标题）。

## 子程序（SubPrograms 字段）

对应类型：`Quicker.Domain.Actions.X.SubPrograms.SubProgram`

子程序类似于函数，将步骤和变量封装成自定义模块。变量与主程序各自独立，同名变量值互不影响。但传入列表/词典等复杂对象时是引用传递，修改会相互影响。

### 三种子程序

| 类型 | 前缀 | 存储位置 | 使用范围 |
|------|------|----------|----------|
| 动作内子程序 | 无 | 动作内部 | 仅当前动作 |
| 公共子程序 | `%%` | 动作外部 | 所有本地动作，支持自动同步 |
| 网络共享子程序 | `@@` | Quicker 网站 | 拖放直接用，内容未经审核 |

子程序定义在 `SubPrograms` 数组中，变量用 `IsInput`/`IsOutput` 标记输入输出。

```csharp
string Id                                               // 唯一标识（GUID）
string Name                                             // 子程序名
string Description                                      // 描述
string SummaryExpression                                // 摘要表达式
string CreateTimeUtc                                    // 创建时间
string LastEditTimeUtc                                  // 最后编辑时间
bool IsLocalEdited                                      // 是否本地编辑过
bool IsProtected                                        // 是否受保护
IList<SubProgram> SubPrograms                           // 嵌套子程序
IList<ActionVariable> Variables                         // 变量列表
IList<ActionStep> Steps                                 // 步骤列表
string SharedId                                         // 共享ID
string ShareTimeUtc                                     // 共享时间
bool? UseServerVersion                                  // 是否使用服务器版本
```

```json
{
  "Id": "GUID", "Name": "子程序名", "Description": "描述",
  "SummaryExpression": "$$",
  "CreateTimeUtc": "...", "LastEditTimeUtc": "...",
  "IsLocalEdited": false, "IsProtected": false,
  "SubPrograms": [], "SharedId": null, "ShareTimeUtc": null, "UseServerVersion": null,
  "Variables": [
    { "Key": "inputVar", "Type": 0, "Desc": "输入", "IsInput": true, "IsOutput": false, "ParamName": "inputVar" },
    { "Key": "outputVar", "Type": 0, "Desc": "输出", "IsInput": false, "IsOutput": true, "ParamName": "outputVar" }
  ],
  "Steps": []
}
```

### 在 CustomWindow cscode 中调用子程序

CustomWindow 的 cscode 使用 C# 5.0，**不能写 await**，使用同步的 `RunSp`：

```csharp
var input = new Dictionary<string, object>();
input["paramName"] = value;
var output = winContext.RunSp("子程序名", input);
var result = output["outputVar"];
```

### 在 C# 脚本步骤中调用子程序

使用 `IStepContext.RunSp`：

```csharp
var input = new Dictionary<string, object>();
input["input1"] = "abc";
input["input2"] = 123;
var output = context.RunSp("子程序名", input);
var result = output["outputVar"];
```

## 变量

对应类型：`Quicker.Domain.Actions.X.Storage.ActionVariable`

```csharp
string Key                                              // 变量名
bool IsLocked                                           // 是否锁定
VarType Type                                            // 变量类型（见下方枚举）
string Desc                                             // 描述
string DefaultValue                                     // 默认值
bool SaveState                                          // 是否持久化（动作结束时自动保存）
bool IsInput                                            // 是否子程序输入参数
bool IsOutput                                           // 是否子程序输出参数
string ParamName                                        // 参数名
object InputParamInfo                                   // 输入参数信息
object OutputParamInfo                                  // 输出参数信息
object TableDef                                         // 表格定义
object CustomType                                       // 自定义类型
string Group                                            // 分组
```

```json
{
  "Key": "变量名", "IsLocked": false, "Type": 0, "Desc": "",
  "DefaultValue": "", "SaveState": false, "IsInput": false, "IsOutput": false,
  "ParamName": "", "InputParamInfo": null, "OutputParamInfo": null,
  "TableDef": null, "CustomType": null, "Group": ""
}
```

**字段说明：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `Key` | 是 | 变量名，步骤中用 `{Key}` 引用 |
| `Type` | 是 | VarType 枚举值（见下表） |
| `Desc` | 否 | 变量描述，显示在编辑器中 |
| `DefaultValue` | 否 | 初始值，见下方默认值写法 |
| `SaveState` | 否 | `true` 时动作结束后自动持久化，下次运行自动加载 |
| `IsLocked` | 否 | `true` 时用户不可在编辑器中修改 |
| `IsInput` | 否 | 子程序输入参数标记 |
| `IsOutput` | 否 | 子程序输出参数标记 |
| `ParamName` | 否 | 子程序参数的外部显示名（为空时用 Key） |
| `Group` | 否 | 变量分组名，编辑器中按组折叠显示 |

**变量类型与 .NET 类型的对应关系：**

| VarType | 名称 | .NET 类型 |
|---------|------|-----------|
| 3 | Bitmap | `System.Drawing.Bitmap` |
| 4 | List | `List<string>` |
| 10 | Dict | `System.Collections.Generic.Dictionary<string, object>` |
| 13 | Table | `System.Data.DataTable` |
| 98 | Object | `object` |
| 99 | Any | 动态类型（相当于 `var`，运行时确定具体类型） |

C# 脚本中读写这些变量时需用对应的 .NET 类型。例如 Bitmap 变量不能直接用 WPF 的 `BitmapSource`，需先转换。

### SaveState（作为状态使用）

设为 `true` 时，动作正常结束后自动将变量值持久化，下次运行时自动加载。

- 状态 key 格式：`$var:变量名`
- **只有动作正常结束才写入**，长期运行或异常退出不会保存
- 常配合 `sys:form` 用作设置窗口（详见 [form.md - 常见用法：设置窗口](form.md#常见用法设置窗口)）
- 需要实时持久化时，改用 `context.WriteState` 手动写入

### DefaultValue（默认值）

各类型的默认值写法：

| 类型 | 写法 | 示例 |
|------|------|------|
| 文本 | 直接写内容，支持多行 | `你好` |
| 布尔 | `true`/`1` 或 `false`/`0` | `true` |
| 数字 | 数字值 | `234.56` |
| 整数 | 整数 | `123` |
| 日期时间 | 日期值或天数偏移 | `2019-4-1 12:30:00` |
| 列表 | 多行，每行一项 | 多行文本 |
| 词典 | `json:` 前缀 + JSON | `json:{"key":"value"}` |

一般不要在 DefaultValue 中使用表达式或引用其他变量。

### IsInput / IsOutput（子程序参数）

子程序变量通过 `IsInput`/`IsOutput` 标记为输入/输出参数：

- **IsInput**：调用方传入值，子程序内部可读
- **IsOutput**：子程序返回值，调用方通过 `var:输出名` 接收
- `ParamName` 控制子程序在编辑器中显示的参数名（为空时用 Key）
- 调用子程序时用 `var:参数名` 前缀传参：`"var:输入名": {"VarKey": null, "Value": "值"}`

## VarType 枚举

对应类型：`Quicker.Domain.Actions.X.Storage.VarType`

```csharp
public enum VarType
{
    [Display(Name = "文本", Order = 10)]
    Text = 0,
    [Display(Name = "数字(小数)", Order = 2)]
    Number = 1,
    [Display(Name = "布尔(是否)", Order = 1)]
    Boolean = 2,
    [Display(Name = "图片(System.Drawing.Bitmap)", Order = 12)]
    Image = 3,
    [Display(Name = "文本列表", Order = 21)]
    List = 4,
    [Display(Name = "时间日期", Order = 11)]
    DateTime = 6,
    [Display(Name = "词典(System.Collections.Generic.Dictionary<string, object>)", Order = 22)]
    Dict = 10,
    [Display(Name = "表单", Order = 33)]
    Form = 11,
    [Display(Name = "数字(整数)", Order = 3)]
    Integer = 12,
    [Display(Name = "表格(System.Data.DataTable)", Order = 34)]
    Table = 13,
    [Display(Name = "对象(Object)", Order = 31)]
    Object = 98,
    [Display(Name = "任意类型", Order = 32)]
    Any = 99,
}
```

## 步骤基础结构

对应类型：`Quicker.Domain.Actions.X.ActionStep`

```csharp
string StepRunnerKey                                    // 步骤执行器键，如 "sys:csscript"
IDictionary<string, ActionStepParam> InputParams        // 输入参数字典
IDictionary<string, string> OutputParams                // 输出参数字典（键=输出名，值=目标变量名）
IList<ActionStep> IfSteps                               // 条件分支（if）的子步骤列表，支持嵌套
IList<ActionStep> ElseSteps                             // 条件分支（else）的子步骤列表
string Note                                             // 步骤备注
bool Disabled                                           // 是否禁用（true=不执行）
bool Collapsed                                          // 是否在编辑器中折叠显示
int DelayMs                                             // 执行后延迟（毫秒），再执行下一步骤
```

```json
{
  "StepRunnerKey": "sys:csscript",
  "InputParams": {
    "参数名": {"VarKey": null, "Value": "固定值"}
  },
  "OutputParams": {
    "输出名": "目标变量名"
  },
  "IfSteps": [],
  "ElseSteps": [],
  "Note": "",
  "Disabled": false,
  "Collapsed": false,
  "DelayMs": 0
}
```

**参数引用：**
- 变量：`{"VarKey": "变量名", "Value": null}`
- 固定值：`{"VarKey": null, "Value": "值"}`
- 文本插值：`{"VarKey": null, "Value": "$$你好，{name}"}`
- 表达式：`{"VarKey": null, "Value": "$=1+2"}`
