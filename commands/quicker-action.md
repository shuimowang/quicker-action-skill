# Quicker 动作生成器

根据用户的需求，生成 Quicker 组合动作的 JSON 文件。

## 使用方式

用户会描述想要的动作功能，你需要：
1. 理解需求，设计动作的步骤流程
2. 生成符合 Quicker 格式的 JSON
3. 保存为 `.json` 文件到用户指定的位置（默认桌面）

## JSON 结构

### 顶层
```json
{
  "Row": 0, "Col": 0, "ActionType": 24,
  "Title": "动作名称", "Description": "描述",
  "Icon": "fa:Solid_Star", "Path": null, "DelayMs": 0,
  "Data": "{...JSON字符串...}",
  "Id": "GUID",
  "AsSubProgram": false, "AllowScrollTrigger": false, "EnableEvaluateVariable": true
}
```

### Data（JSON 字符串）
```json
{
  "LimitSingleInstance": false,
  "SummaryExpression": "$$",
  "SubPrograms": [],
  "Variables": [],
  "Steps": []
}
```

### 图标（Icon 字段）

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

**Font Awesome 图标库：** 内置 7000+ 图标，4 种风格：`Solid`、`Regular`、`Light`、`Brands`。格式为 `风格_名称`。搜索：https://fontawesome.com/icons

**图标名获取：** 面板腰栏 → 工具 → 图标库，选择后自动复制名称。

`null` 表示无图标（显示文字标题）。

### 子程序（SubPrograms 字段）

子程序定义在 `SubPrograms` 数组中，变量用 `IsInput`/`IsOutput` 标记输入输出。
```json
{
  "Id": "GUID",
  "Name": "子程序名",
  "Description": "描述",
  "SummaryExpression": "$$",
  "IsLocalEdited": false,
  "IsProtected": false,
  "SubPrograms": [],
  "SharedId": null,
  "ShareTimeUtc": null,
  "UseServerVersion": null,
  "Variables": [
    {"Key": "inputVar", "Type": 0, "Desc": "输入", "IsInput": true, "IsOutput": false, "ParamName": "inputVar", ...},
    {"Key": "outputVar", "Type": 0, "Desc": "输出", "IsInput": false, "IsOutput": true, "ParamName": "outputVar", ...}
  ],
  "Steps": []
}
```

在 cscode 中调用子程序：
```csharp
var input = new Dictionary<string, object> { {"paramName", value} };
var output = await winContext.RunSpAsync("子程序名", input);
var result = output["outputVar"];
```

### 变量
```json
{
  "Key": "变量名", "IsLocked": false,
  "Type": 0,        // 见下方 VarType 枚举
  "Desc": "", "DefaultValue": "",
  "SaveState": false, "IsInput": false, "IsOutput": false,
  "ParamName": "", "InputParamInfo": null, "OutputParamInfo": null,
  "TableDef": null, "CustomType": null, "Group": ""
}
```

### VarType 枚举
| 值 | 名称 | 说明 |
|----|------|------|
| 0 | Text | 文本 |
| 1 | Number | 数字(小数) |
| 2 | Boolean | 布尔(是否) |
| 3 | Image | 图片 |
| 4 | List | 文本列表 |
| 6 | DateTime | 时间日期 |
| 9 | Enum | 选项 |
| 10 | Dict | 词典 |
| 11 | Form | 表单 |
| 12 | Integer | 数字(整数) |
| 13 | Table | 表格 |
| 14 | FormForDict | 表单(词典) |
| 98 | Object | 对象 |
| 99 | Any | 任意类型 |

### 步骤基础结构
```json
{
  "StepRunnerKey": "模块类型",
  "InputParams": { "参数名": {"VarKey": null, "Value": "固定值"} },
  "OutputParams": { "输出名": "目标变量名" },
  "IfSteps": [], "ElseSteps": [],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

**参数引用：**
- 变量：`{"VarKey": "变量名", "Value": null}`
- 固定值：`{"VarKey": null, "Value": "值"}`
- 文本插值：`{"VarKey": null, "Value": "$$你好，{name}"}`
- 表达式：`{"VarKey": null, "Value": "$=1+2"}`

---

## 核心模块

### 1. 赋值 (`sys:assign`)

```json
{
  "StepRunnerKey": "sys:assign",
  "InputParams": {
    "input": {"VarKey": null, "Value": "Hello"},
    "stopIfFail": {"VarKey": null, "Value": "1"}
  },
  "OutputParams": {
    "isSuccess": null,
    "output": "目标变量名",
    "errMessage": null
  },
  "IfSteps": null, "ElseSteps": null,
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

**支持表达式：**
```json
"input": {"VarKey": null, "Value": "$=\r\nreturn {text}.ToUpper();"}
```

### 3. C# 脚本 (`sys:csscript`)

**普通模式 v1（C# 5.0）：**
```json
{
  "StepRunnerKey": "sys:csscript",
  "InputParams": {
    "mode": {"VarKey": null, "Value": "normal"},
    "script": {"VarKey": null, "Value": "C#代码"},
    "reference": {"VarKey": null, "Value": ""},
    "runOnUiThread": {"VarKey": null, "Value": "auto"},
    "enableCache": {"VarKey": null, "Value": "0"},
    "stopIfFail": {"VarKey": null, "Value": "1"}
  },
  "OutputParams": {
    "isSuccess": "isSuccessVar",
    "rtn": "resultVar",
    "errMessage": null
  },
  "IfSteps": [], "ElseSteps": [],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

**v2 Roslyn（C# 7.3）：** `mode` 改为 `"normal_roslyn"`，同样在 Quicker 进程内执行，可用 `Quicker.Utilities` 等内部程序集。首次编译冷启动较慢，自动缓存程序集（代码不变可复用缓存）。

**低权限模式：** `mode` 为 `"lowtrust"` / `"lowtrust_roslyn"`，在 LPAgent 代理进程执行，**不能**访问动作变量和 Quicker 内部程序集，仅支持简单文本传递。Exec 签名不同：`public static string Exec(string paramValue)`

**InputParams：**
| 参数 | 说明 | 值 |
|------|------|-----|
| `mode` | 模式 | `"normal"` v1 / `"normal_roslyn"` v2 / `"lowtrust"` 低权限v1 / `"lowtrust_roslyn"` 低权限v2 |
| `script` | C#代码 | 代码字符串 |
| `reference` | DLL引用 | 路径，每行一个 |
| `runOnUiThread` | 执行线程 | `"auto"` 自动 / `"ui"` UI线程 / `"mta"` 后台MTA / `"sta"` 共享STA / `"sta_new"` 独立STA |
| `enableCache` | 缓存程序集 | `"0"` / `"1"` |
| `stopIfFail` | 失败停止 | `"0"` / `"1"` |

**OutputParams：** `isSuccess`（是否成功）、`rtn`（返回值）、`errMessage`（错误信息）

**Exec 方法签名：**
```csharp
// 有返回值
public static string Exec(Quicker.Public.IStepContext context)
{
    var text = context.GetVarValue("varName") as string;
    context.SetVarValue("varName", value);
    return "返回值";
}

// 无返回值
public static void Exec(Quicker.Public.IStepContext context) { }
```

**IStepContext 完整方法列表：**

| 方法 | 说明 |
|------|------|
| `GetVarValue(string varName)` | 读取动作变量 |
| `SetVarValue(string varName, object value)` | 写入动作变量 |
| `EvalExpression(string expression, bool onUiThread)` | 求值 Quicker 表达式 |
| `RunSp(string spName, IDictionary<string, object> input)` | 调用子程序 |
| `ReadState(string key, string defaultValue)` | 读取持久状态（跨次运行） |
| `WriteState(string key, string value)` | 写入持久状态 |
| `ReadCache<T>(string key, T defaultValue)` | 读取缓存 |
| `WriteCache(string key, object value, int maxKeepSeconds)` | 写入缓存（带过期时间） |

**状态存取示例：**
```csharp
string old = context.ReadState("items_json", "[]");
context.WriteState("items_json", newJson);
```

**子程序调用示例：**
```csharp
var result = context.RunSp("子程序名", new Dictionary<string, object>
{
    { "input1", "abc" },
    { "input2", 123 }
});
```

**异步方法等待技巧：** Exec 是同步方法，不能直接 await。可以把 Task 存到变量，后续赋值步骤中 `await {task}` 等待：
```csharp
// csscript 步骤：启动异步，存 Task
var task = HttpClient.GetAsync(url);
context.SetVarValue("task", task);
// 后续赋值步骤：$= await {task}
```

**引用 DLL（v1）：**
```csharp
//css_reference C:\path\to\library.dll
//css_ref System.Net.Http.dll
```

**线程选择（`runOnUiThread`）：**

| 值 | 适用场景 |
|----|----------|
| `ui` | 需要 WPF 控件、窗口、剪贴板操作时 |
| `sta` | 需要 STA 线程但不想占用 UI 线程时 |
| `staLongRun` | 需要独立 STA 线程且运行时间较长时 |
| `background` | 普通后台逻辑（不涉及 UI） |
| `auto` | 仅在确认脚本不涉及 UI/STA 时使用，**不是默认选择** |

**关键：** 涉及 WPF、剪贴板、窗口操作时，**必须**显式选 `ui` 或 `sta`，不要依赖 `auto`。

**注意事项：**
- 程序集按代码内容缓存，代码不变可复用（避免用文本插值生成脚本）
- 普通模式自动提权，可能无法通过 COM 控制第三方程序
- v2 首次编译冷启动慢，后续自动缓存
- WinForm 控件用后台线程（前台线程中文输入可能异常）

**Quicker 内置可用 DLL（`C:\Program Files\Quicker\`）：**

| DLL | 用途 |
|-----|------|
| `Newtonsoft.Json.dll` | JSON 解析/序列化 |
| `HtmlAgilityPack.dll` | HTML 解析 |
| `CsvHelper.dll` | CSV 读写 |
| `NPOI.dll` | Excel/Word 读写 |
| `PdfSharp.dll` | PDF 生成 |
| `NAudio.dll` | 音频处理 |
| `FlaUI.Core.dll` / `FlaUI.UIA3.dll` | UI 自动化 |
| `AutoItX3.Assembly.dll` | AutoIt 自动化 |
| `ImageProcessor.dll` | 图片处理 |
| `zxing.dll` / `zxing.presentation.dll` | 二维码/条码 |
| `QRCoder.dll` | 二维码生成 |
| `Everything64.dll` | Everything 搜索 |
| `WindowsInput.dll` | 键鼠模拟 |
| `NCalc.dll` | 数学表达式求值 |
| `System.Data.SQLite.dll` | SQLite 数据库 |
| `MySqlConnector.dll` | MySQL 数据库 |
| `Jint.dll` | JavaScript 引擎 |
| `ToastNotifications.dll` | 通知提示 |
| `log4net.dll` | 日志 |

### 4. Python 脚本 (`sys:pythonscript`)

基于 pythonnet，仅支持 Python 3。**注意：** 分享动作时无法确定对方是否安装 Python，建议优先用 `sys:csscript`。

**InputParams：**
| 参数 | 说明 |
|------|------|
| `script` | Python 代码 |

**OutputParams：** `rtn`（返回值）、`isSuccess`（是否成功）

**变量访问：**
```python
text = quicker.context.GetVarValue('变量名')    # 读取
quicker.context.SetVarValue('变量名', value)     # 写入
```

**限制：**
- 必须用官方 Python（python.org），第三方环境可能无法运行
- 支持版本：Python 3.7 ~ 3.12，64 位系统需 64 位 Python
- 只访问简单类型变量（数字/文本），复杂类型有闪退风险
- 不能使用 COM 接口
- 可返回文本列表和简单词典，不建议返回复杂类型

---

## 其他常用模块

### 获取选中文本 (`sys:getSelectedText`)

InputParams：`format`（`"UnicodeText"` 等）、`waitMs`、`trim`、`stopIfFail`。OutputParams：`isSuccess`、`output`。

### 翻译 (`sys:translation`)

InputParams：`operation`（`"single"`）、`text`、`srcLang`/`dstLang`（`"Auto"` 等）、`vendor`（`"Baidu"` 等）。OutputParams：`resultText`。

### 显示文本 (`sys:showText`)

InputParams：`type`（`"NO_WAIT"`）、`text`、`title`、`fontsize`、`enableEscClose`、`autoWrap`。

### 提示消息 (`sys:notify`)

InputParams：`type`（`"Info"` / `"Success"` / `"Warning"` / `"Error"`）、`msg`。

### 调用子程序 (`sys:subprogram`)

InputParams：`subProgram`（子程序名）、`var:参数名`（参数值）、`stopIfFail`。OutputParams：`isSuccess`、`var:输出名`、`errMessage`。

### 条件判断 (`sys:simpleIf`)
```json
{
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": {
    "condition": {"VarKey": null, "Value": "$={varName}==\"value\""}
  },
  "OutputParams": {},
  "IfSteps": [ /* ... */ ],
  "ElseSteps": [ /* ... */ ],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

### 步骤组 (`sys:group`)

将多个步骤分组执行：
```json
{
  "StepRunnerKey": "sys:group",
  "InputParams": {
    "skipErr": {"VarKey": null, "Value": "0"},
    "skipWhenDebugging": {"VarKey": null, "Value": "0"},
    "useMultiThread": {"VarKey": null, "Value": "0"},
    "waitAny": {"VarKey": null, "Value": "0"}
  },
  "OutputParams": {
    "isSuccess": null,
    "errorMessage": null
  },
  "IfSteps": [ /* 组内步骤 */ ],
  "ElseSteps": [],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

### 停止 (`sys:stop`)
```json
{
  "StepRunnerKey": "sys:stop",
  "InputParams": {
    "returnType": {"VarKey": null, "Value": "none"},
    "returnValue": {"VarKey": null, "Value": ""}
  },
  "OutputParams": {},
  "IfSteps": [], "ElseSteps": [],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

### 注释 (`sys:comment`)
```json
{
  "StepRunnerKey": "sys:comment",
  "InputParams": {
    "comment": {"VarKey": null, "Value": "注释内容"}
  },
  "OutputParams": {},
  "IfSteps": [], "ElseSteps": [],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

---

## 表达式语法

表达式以 `$=` 开头，支持两种形式：

### 简单表达式
相当于 C# 赋值语句等号后面的部分：
- 变量运算：`$= {数字变量} +1`
- 布尔判断：`$= {数字变量} > 10`
- 字符串拼接：`$= "Hello " + {name}`

### 复杂表达式
支持 `if/else`、`return` 等控制流：
```
$= 
if ({number1} > {number2})
{
    return "较大值为number1:" + {number1};
}else{
    return "较大值为number2:" + {number2};
}
```

### 变量引用
使用花括号：`{变量名}`

### 内置对象
- `_context` — 动作上下文，可调用 `GetVarValue`/`SetVarValue`/`RunSp` 等
- `_qk` — 内置功能封装
- `_eval` — 表达式引擎，可注册方法 `_eval.AddMethod(code)`、注册变量 `_eval.RegisterGlobalVariable(name, value)`

### 已注册类型
`Regex`、`Path`、`JsonConvert`、`JArray`、`JObject`、`DateTime`、`File`、`Directory`、`Process`、`StringBuilder` 等

### 环境限制
- .NET Framework 4.7.2
- 普通模式 v1：C# 5.0
- 普通模式 v2（Roslyn）：C# 7.3

**C# 5.0 禁止使用的语法（cscode 和 csscript 均适用）：**
- `$""` 字符串插值 → 用 `string.Format("{0}", arg)`
- `?.` null 条件运算符 → 用 `if (x != null) x.Method()`
- `=>` 表达式体成员 → 用完整 `{ return ...; }`
- `nameof()` → 用字符串字面量
- `when` 异常过滤器 → 不支持
- `using static` → 不支持

### 定义公共方法
可在赋值中定义 `public` 方法，后续通过 `{方法名}` 调用：
```
$=
public int Add(int a, int b)
{
    return a + b;
}
```
输出给变量 `Add`，之后调用：`$= {Add}(4, 5)`

### Lambda 与委托
```csharp
// Func<参数类型, 返回类型>
Func<int, int, int> add = (x, y) => x + y;

// Action（无返回值）
Action<string> greet = name => Console.WriteLine("Hello " + name);
```

---

### 自定义窗口 (`sys:customwindow`)

创建 WPF 窗口，支持 XAML 布局和数据绑定。

**InputParams：**
| 参数 | 说明 |
|------|------|
| `type` | `"ShowAndWaitClose"` 显示并等待关闭 / `"Show"` 显示不等待 / `"Close"` 关闭窗口 |
| `windowMarkup` | WPF XAML 代码 |
| `dataMapping` | 数据映射（多行文本） |
| `windowId` | 窗口标识（用于关闭） |
| `cscode` | 辅助 C# 代码（可选） |
| `events` | 事件处理（可选） |
| `closeWhenDeactivate` | 失去焦点时关闭，`"true"` / `"false"` |
| `autoCloseTime` | 自动关闭秒数，0为不自动 |
| `activateMode` | `"AutoActivate"` 自动激活 / `"NoActivate"` 不自动激活 / `"None"` 不支持激活 |
| `winLocation` | 窗口位置：`"Auto"` / `"CenterScreen"` / `"TopRight"` / `"BottomRight"` / `"TopLeft"` / `"BottomLeft"` / `"TopCenter"` / `"BottomCenter"` / `"LastPosition"` / `"FullScreen"` / `"Manual"` / `"Maximized"` 等 |
| `winSize` | 窗口尺寸，如 `"300,200"` 或 `"50%,50%"` |
| `stopIfFail` | 失败停止，`"0"` / `"1"` |

**OutputParams：** `isSuccess`、`result`（窗口结果）、`windowLocation`、`errMessage`

**XAML 注意事项：**

自定义窗口步骤的 XAML 和普通 WPF 工程不同，有以下限制：
- 去掉 `x:Class` 属性
- 必须注册命名空间：`xmlns:qk="https://getquicker.net"`（即使不用 qk:Att.Action 也要加）
- **不能用字符串绑定事件**：`Loaded="OnLoaded"`、`Click="OnClick"` 等写法会报错，事件必须在 cscode 中通过代码绑定
- 按钮操作：`qk:Att.Action="操作内容"`

**搜索框等需要实时响应的控件**：不要用 `{Binding}`，在 cscode 中 `FindName` 获取控件后绑定 `TextChanged` 等事件。因为自定义窗口的 dataContext 是全部通知，绑定容易产生意外行为。

**数据映射格式（每行一个）：**
```
窗口数据名:{动作变量名}        # 关联变量（开窗口取值，关窗口写回）
数据项名:=(int)0               # 初始化内部数据
数据项名:$= {number1} + {number2}  # 动态计算
```

**按钮操作（冒号必须有，即使是关闭不返回值也要写 `close:`）：**
```
close:           # 关闭窗口，结果为空
close:返回值      # 关闭并返回结果
operation=copy&data={text}   # 复制到剪贴板
operation=paste&data={text}  # 粘贴到目标窗口
operation=open&data=https://example.com  # 打开网址
```

**辅助 C# 回调（必须引用）：**
```csharp
using System.Windows;
using System.Collections.Generic;
using Quicker.Public;  // ICustomWindowContext

// OnWindowCreated 必须存在，即使为空
public static void OnWindowCreated(Window win, IDictionary<string, object> dataContext, ICustomWindowContext winContext) { }
// 可选
public static void OnWindowLoaded(Window win, IDictionary<string, object> dataContext, ICustomWindowContext winContext) { }
// 可选，按钮点击回调：controlName 对应 x:Name，controlTag 对应 Tag 属性
public static bool OnButtonClicked(string controlName, object controlTag, Window win, IDictionary<string, object> dataContext, ICustomWindowContext winContext) { return true; }
```

**按钮触发回调（不关闭窗口）：** 用 `Tag="xxx"`，在 OnButtonClicked 中检查 `controlTag`，返回 `true` 保持窗口。

**按钮关闭窗口：** 用 `qk:Att.Action="close:返回值"`

### 自定义窗口进阶

**常用事件绑定：**
```csharp
btn.Click += (s, e) => { };                    // 左键点击
btn.MouseRightButtonUp += (s, e) => { };       // 右键点击
btn.PreviewMouseLeftButtonDown += (s, e) => { }; // 鼠标按下（用于长按检测）
win.MouseLeftButtonDown += (s, e) => { win.DragMove(); }; // 拖动窗口
```

**键盘模拟（需 using System.Windows.Forms）：**
```csharp
System.Windows.Forms.SendKeys.SendWait("{ENTER}");   // 发送按键
System.Windows.Forms.SendKeys.SendWait("^c");        // Ctrl+C
```

**长按/定时器（DispatcherTimer）：**
```csharp
var timer = new DispatcherTimer();
timer.Interval = TimeSpan.FromMilliseconds(400);
timer.Tick += (s, e) => { /* 重复操作 */ };
timer.Start();
// timer.Stop();
```

**通知提示（需 using Quicker.Utilities）：**

`AppHelper` 使用 ToastNotifications，不阻塞进程，仅在 cscode 和 C# 脚本步骤中可用：
```csharp
using Quicker.Utilities;
AppHelper.ShowInformation("提示消息");
AppHelper.ShowSuccess("成功消息");
AppHelper.ShowWarning("警告消息");
```

**获取网站 Favicon：**
```
https://helperservice.getquicker.cn/favicon/get/{域名}
```
例如：`https://helperservice.getquicker.cn/favicon/get/getquicker.net`，返回图片。可在 `qk:IconControl` 或 `<Image>` 中直接使用。

**单实例窗口（防止重复打开）：**

cscode 中有静态字段时，多次触发动作会产生多个窗口。在自定义窗口步骤前检测已有窗口，根据不同需求选择策略。

窗口通过 `windowId` 标识查找，GetWindows 和 ShowAndWaitClose 必须使用相同的 `windowId`。如果动作只有一个窗口，可以用 `$=_context.ActionId` 作为标识（即动作自身的 Id）。

```
步骤1: GetWindows → windowList
步骤2: If windowList.Any() → 执行策略
步骤3: ShowAndWaitClose → 显示新窗口（仅关闭/停止策略不需要此步）
```

**策略一：关闭旧窗口，打开新窗口**
```json
// 步骤1: 获取窗口列表
{
  "StepRunnerKey": "sys:customwindow",
  "InputParams": {
    "type": {"VarKey": null, "Value": "GetWindows"},
    "windowId": {"VarKey": null, "Value": "$=_context.ActionId"},
    "stopIfFail": {"VarKey": null, "Value": "0"}
  },
  "OutputParams": {"isSuccess": null, "windowList": "windowList", "errMessage": null}
}
// 步骤2: 关闭已有窗口
{
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": {"condition": {"VarKey": null, "Value": "$={windowList}.Any()"}},
  "IfSteps": [{
    "StepRunnerKey": "sys:assign",
    "InputParams": {
      "input": {"VarKey": null, "Value": "$=\r\nSystem.Windows.Window window = {windowList}[0];\r\nwindow.Dispatcher.Invoke(() => { window.Close(); });"},
      "stopIfFail": {"VarKey": null, "Value": "1"}
    },
    "OutputParams": {"isSuccess": null, "output": null, "errMessage": null}
  }]
}
// 步骤3: 显示新窗口
```

**策略二：停止动作，沿用旧窗口** — 步骤2 IfSteps 中放 `sys:stop`，无需步骤3。

**策略三：激活旧窗口** — 步骤2 IfSteps 中 assign：`window.Dispatcher.Invoke(() => { window.Activate(); window.Show(); window.WindowState = System.Windows.WindowState.Normal; })`，再加 `sys:stop`。

**最简示例（输入框+确定按钮）：**
```json
{
  "StepRunnerKey": "sys:customwindow",
  "InputParams": {
    "type": {"VarKey": null, "Value": "ShowAndWaitClose"},
    "windowMarkup": {"VarKey": null, "Value": "<Window xmlns=\"http://schemas.microsoft.com/winfx/2006/xaml/presentation\" xmlns:qk=\"https://getquicker.net\" Title=\"输入\" Width=\"300\" Height=\"150\">\n  <StackPanel Margin=\"10\">\n    <TextBox Text=\"{Binding [input]}\" Margin=\"0,0,0,10\"/>\n    <Button Content=\"确定\" qk:Att.Action=\"close:ok\"/>\n  </StackPanel>\n</Window>"},
    "dataMapping": {"VarKey": null, "Value": "input:{userInput}"},
    "windowId": {"VarKey": null, "Value": "$=_context.ActionId"},
    "cscode": {"VarKey": null, "Value": ""},
    "activateMode": {"VarKey": null, "Value": "AutoActivate"},
    "winLocation": {"VarKey": null, "Value": "CenterScreen"}
  },
  "OutputParams": {
    "isSuccess": "isSuccess",
    "result": "windowResult",
    "windowLocation": null,
    "errMessage": null
  },
  "IfSteps": [], "ElseSteps": [],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

---

## 澄清提问规范

信息不足时才提问，遵循以下规则：
- **单次只问一个问题**，不要一次问多个
- **附带选项和推荐**，格式：
```
Q1: [问题]
A. [选项]
B. [选项]
推荐：B — [理由]
```
- 能从代码/文档自行解决的不要问用户
- 不要为了"确认"而问已经明确的信息

- 默认值直接写在变量的 `DefaultValue` 里，无需单独赋值步骤
- XAML 不要写 `WindowStartupLocation`，窗口位置由 `winLocation` 参数控制
- 如果不需要 C# 回调，`cscode` 设为空字符串

## 实现优先级（严格遵守）

按以下顺序选择方案，**能用上层就不选下层**：

1. **Quicker 内置步骤模块**（`sys:assign`、`sys:simpleIf`、`sys:form` 等）
2. **表达式 `$=`**（步骤参数内的简单计算、判断）
3. **文本插值 `$$`**（步骤参数内的文本拼接）
4. **步骤组合**（多个步骤协作）
5. **步骤组 / 子程序**（复杂流程拆分）
6. **C# 脚本 `sys:csscript`**（兜底方案，不是默认方案）

**判断标准：** 如果用内置步骤 + 表达式就能实现，就不要写 C# 脚本。只有当内置步骤明显不够用（需要复杂对象构建、内部服务调用、多步逻辑组合等）时才用脚本。

## 界面选型规则

选择界面模块时遵循"能轻则轻"原则：

| 核心需求 | 选择 | 说明 |
|----------|------|------|
| 维护配置、填写参数 | `sys:form` | 字段明确，填写后回归主流程 |
| 提供操作集合、按钮菜单 | `sys:custompanel` | JSON 驱动，轻量交互 |
| 复杂布局、预览、拖拽、独立窗口 | `sys:customwindow` | XAML 级别控制，重量级 |

**升级条件：**
- form → custompanel：交互从"填写"变为"选择操作"
- custompanel → customwindow：需要预览、拖拽、复杂事件、富展示

**不要因为"更高级"就默认用 customwindow。**

## 生成规则

1. `Data` 字段必须是 JSON 字符串（需要转义）
2. 按实现优先级选择方案，优先用内置模块和表达式
3. C# 脚本通过 `context.GetVarValue()` / `context.SetVarValue()` 访问变量
4. 不需要的 OutputParams 设为 `null`
5. 文件名格式: `{动作名}_{日期}.json`，默认保存到桌面
6. 涉及配置维护优先考虑 `sys:form`，操作集合用 `sys:custompanel`，复杂交互才用 `sys:customwindow`

## 生成后自检清单

生成动作后，**必须逐条检查**以下问题，确认无误后再输出给用户。

### C# 命名空间冲突（最高频错误）

Quicker 自动注入的 using 包含 `System.Windows`、`System.Windows.Forms`、`System.Drawing`、`System.IO`、`System.Windows.Shapes`，以下类型**必须写全限定名**：

| 简写 | 冲突 | 正确写法 |
|------|------|----------|
| `Rectangle` | `System.Drawing` vs `System.Windows.Shapes` | 按用途写全名 |
| `ListBox` | `System.Windows.Controls` vs `System.Windows.Forms` | 按用途写全名 |
| `Path` | `System.IO` vs `System.Windows.Shapes` | `System.IO.Path` |
| `Control` | `System.Windows.Controls` vs `System.Windows.Forms` | 按用途写全名 |
| `NotifyIcon` | `System.Windows.Forms` | `System.Windows.Forms.NotifyIcon` |
| `DialogResult` | `System.Windows.Forms` | `System.Windows.Forms.DialogResult` |
| `Bitmap` | `System.Drawing` | `System.Drawing.Bitmap`（已有 using 一般不冲突，但注意） |
| `SolidBrush` | `System.Drawing` | `System.Drawing.SolidBrush` |
| `Pen` | `System.Drawing` | `System.Drawing.Pen` |
| `Font` | `System.Drawing` | `System.Drawing.Font` |
| `Form` | `System.Windows.Forms` | `System.Windows.Forms.Form` |
| `Point` | `System.Drawing` vs `System.Windows` | 按用途写全名 |

**规则：只要同时 using 了 `System.Windows` 和 `System.Windows.Forms`/`System.Drawing`，所有有歧义的类型一律写全名。**

### C# 变量与语法

- **`var` 不允许多声明**：`var a = 1, b = 2;` 是错的，必须拆成 `var a = 1; var b = 2;`。显式类型（`int`, `bool`）可以但不建议
- **同一方法内变量名不能重复**：检查所有局部变量名在方法内是否唯一，特别是多个用途的 `ox`/`oy` 等常见命名
- **类型别名不存在**：不要用 `F<Tb>` 这种自造别名，直接写 `F<TextBox>`
- **跨类访问**：从 `ColorResultWindow` 调用 `ColorPickerOverlay` 的方法，该方法必须是 `public static`
- **删除未使用的字段/变量**：编译器会警告，影响可信度

### XAML

- **Style 必须用 StaticResource**：`Style="{StaticResource Key}"`，不能写 `Style="{Key}"`
- **同一控件不能有重复属性**：特别是 `Text=` 同时有默认值和 Binding 的情况，只能保留一个
- **文件图标绑定**：`qk:IconControl` 需要 `icon:.txt` 格式，不能绑定完整路径。需要在数据模型中加 `IconKey` 属性

### 性能

- **避免逐像素 GetPixel**：读取多个像素时用 `BitBlt` + `GetBitmapBits` 批量读取，不要循环调用 `GetPixel`（每次都要和显卡通信，极慢）
- **Timer 间隔**：UI 刷新 Timer 不要低于 30ms，30-50ms 为宜

### 验证流程

1. 生成 Python 脚本
2. 运行脚本生成 JSON
3. 从 JSON 中提取 cscode 和 XAML
4. 用正则扫描 cscode：检查未限定的冲突类型名、`var` 多声明、重复变量名
5. 用正则扫描 XAML：检查 `Style="{` 非 StaticResource、重复属性
6. 修复所有问题后重新生成，再次验证直到无问题

$ARGUMENTS
