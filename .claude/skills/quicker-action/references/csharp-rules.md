# C# 脚本规则

## Exec 方法签名

> **⚠️ `sys:csscript` 的 script 参数必须包含一个 `public static` 的 `Exec` 方法。**
> 没有 Exec 方法的代码会被编译但不会执行，静默无输出。方法可以有返回值（`string`）或无返回值（`void`）。

```csharp
// 有返回值（OutputParams 的 rtn 接收返回值）
public static string Exec(Quicker.Public.IStepContext context)
{
    var text = context.GetVarValue("varName") as string;
    context.SetVarValue("varName", value);
    return "返回值";
}

// 无返回值
public static void Exec(Quicker.Public.IStepContext context) { }
```

- 必须是 `public static`
- 参数类型必须是 `Quicker.Public.IStepContext`（不是 `ActionExecuteContext`）
- 用 `context.GetVarValue()` / `context.SetVarValue()` 读写变量（不是 `_context`）

## 内置变量（`_context`、`_eval`、`_qk`）

表达式和 C# 步骤中可直接使用三个内置变量。

### `_eval`（表达式引擎）

类型：`Z.Expressions.EvalContext`，承载动作代码的执行环境。

```csharp
// 注册自定义 DLL，后续步骤即可使用其中的类型
_eval.RegisterAssembly(typeof(MyClass).Assembly);

// 注册全局变量
_eval.RegisterGlobalVariable("myVar", value);

// 添加自定义方法
_eval.AddMethod("MyMethod", (Func<int, int, int>)((a, b) => a + b));
```

`C:\Program Files\Quicker\` 下的 DLL（Newtonsoft.Json、NAudio、HtmlAgilityPack 等）已内置可用，**不需要注册**。

### `_context`（动作执行上下文）

类型：`Quicker.Domain.Actions.ActionExecuteContext`，实现 `IActionContext` 接口。

**IActionContext 完整接口：**

```csharp
// Quicker.Public.Interfaces.IActionContext
public interface IActionContext
{
    int Id { get; }
    bool IsRootContext { get; }
    string ActionId { get; }
    string ActionTitle { get; }
    ActionExtraContextData ExtraData { get; }
    CancellationToken? CancellationToken { get; }

    IDictionary<string, object> GetVariables();
    void SetVarValue(string varName, object value);
    object GetVarValue(string varName);
    object TryGetValue(string var, object defaultValue);
    bool IsVarExists(string varName);

    IActionContext GetRootContext();
    IActionContext GetParentContext();

    IDictionary<string, object> RunSp(string spName, IDictionary<string, object> inputParams);
    IDictionary<string, object> RunSp(string spName, object inputParams);
    Task<IDictionary<string, object>> RunSpAsync(string spName, IDictionary<string, object> inputParams);
    Task<IDictionary<string, object>> RunSpAsync(string spName, object inputParams);

    void WriteState(string key, string value);
    string ReadState(string key, string defaultValue);
    void WriteCache(string key, object value, int maxKeepSeconds);
    T ReadCache<T>(string key, T defaultValue);
    object RemoveCache(string key);
    void ClearCache();

    void UpdateVariablesFromDict(IDictionary<string, object> dict);
    void UpdateVariablesFromJson(string dictJson);
    void RegisterDisposable(IDisposable disposableObject);
    object EvalExpression(string expression, bool onUiThread = false);
    void ExecuteCommonOperationItem(CommonOperationItem item);
    bool IsShouldStopAction();
}
```

**ActionExecuteContext 额外属性（`_context` 可直接访问）：**

```csharp
// Quicker.Domain.Actions.ActionExecuteContext
// 除 IActionContext 继承的成员外，还有以下属性：

ActionTrigger ActionTrigger { get; set; }
DateTime StartTime { get; set; }
Window ParentWindow { get; set; }
IXProgram XProgram { get; set; }
ActionDataType LastDataType { get; set; }
AppServer AppServer { get; }
string InputParam { get; set; }
string TextData { get; set; }            // 设置时自动标记 LastDataType = Text
Image ImageData { get; set; }            // 设置时自动标记 LastDataType = Image
IList<int> CurrentCodeLine { get; }
bool IsDebugging { get; }
IActionLogger ActionLogger { get; set; }
IDictionary<string, object> CustomData { get; }  // 变量存储
ActionStopFlag StopFlag { get; set; }
bool BreakFlag { get; set; }
bool HideWarning { get; set; }
string ErrorMessage { get; set; }
IntPtr ActiveWindowHwnd { get; set; }
Point? WaiteUserWindowTopLeft { get; }
string SuccessMessage { get; set; }
bool ContinueFlag { get; set; }
PointTargetInfo TargetInfo { get; set; }
string WaiteUserWindowResult { get; set; }
bool IsStoppedByUser { get; set; }
bool SkipStopWarning { get; set; }
bool? IsImeEnabled { get; }
IDictionary<string, object> States { get; }      // 跨步骤状态存储
ActionExecuteContext ChildContext { get; set; }
bool ReturnError { get; set; }
string ReturnResult { get; set; }
object ReturnResultObject { get; set; }
TargetBrowserInfo TargetBrowser { get; set; }
bool HasImageParamUsed { get; set; }
ActionExtraContextData ExtraData { get; }
int ClipboardSeqBeforeCtrlC { get; set; }
```

**ActionExecuteContext 额外方法：**

```csharp
// 等待用户窗口
void AddWaiteWindow(string key, WaitUserWindow waitWindow);
void UpdateWaiteWindowLocation(Point windowTopLeft);
void OnWaitWindowClosed(string key, string selectedOperation);
bool IsWaitWindowClosed(string key);
void CloseWaitWin(string key);
WaitUserWindow GetWaitWindow(string key);

// 执行控制
void StopAction(ActionStopFlag stopFlag, string reason, bool skipCloseWaitWindow = false);
void SetBreakFlag();
bool IsShouldBreak();
void ClearBreakFlag();
void SetContinueFlag();
bool ShouldContinue();
void ClearContinueFlag();

// 媒体
MediaPlayer GetMediaPlayer();

// 通知
void ShowWarning(string message, ActionStep step);

// 输入法
void SaveImeState(bool isEnabled);

// 表达式引擎
EvalContext GetEvalContext();

// 窗口位置记忆
void SaveTextWindowLocation(string autoCloseKey, Window w);
Rect? GetTextWindowLocation(string autoCloseKey);
WindowState? GetTextWindowState(string autoCloseKey);

// 资源管理
void RegisterDisposable(IDisposable disposableObject);
void TryDisposeObjects();

// 子程序结果
bool IsSubProgramSuccess();
```

**存储机制：**

| 机制 | 方法 | 类型 | 生命周期 | 说明 |
|------|------|------|----------|------|
| 变量 | `GetVarValue` / `SetVarValue` | 任意 | 动作运行期间 | 最临时 |
| 缓存 | `ReadCache<T>` / `WriteCache` | 泛型 T | Quicker 进程存活期间 | 支持任意类型，进程退出丢失 |
| 状态 | `ReadState` / `WriteState` | string | 永久（写文件，有防抖） | 复杂数据需序列化为 JSON |

```csharp
// 变量
_context.SetVarValue("name", "value");
var name = _context.GetVarValue("name") as string;

// 缓存（支持泛型，进程级）
_context.WriteCache("data", myObject, 3600);  // 保留 1 小时
var data = _context.ReadCache<MyType>("data", null);

// 状态（永久，写文件，带防抖）
_context.WriteState("config_json", json);
var json = _context.ReadState("config_json", "{}");
```

**上下文层级：**

主程序和子程序各有独立的 `_context` 实例，形成父子链：

```
主程序 _context
  └─ 子程序 A: GetParentContext() → 主程序, GetRootContext() → 主程序
       └─ 子程序 B: GetParentContext() → A, GetRootContext() → 主程序
```

### `_qk`

内部功能封装，方法不常用，一般不需要关注。

## IStepContext 接口

C# 脚本步骤的 `context` 参数类型。`IStepContext` 继承 `IActionContext`，拥有 `IActionContext` 的全部方法。

```csharp
// Quicker.Public.Interfaces.IStepContext
public interface IStepContext : IActionContext
{
    // 继承 IActionContext 的所有方法（见上方 _context 章节）
    // IStepContext 本身无额外方法
}
```

### 状态存取示例

```csharp
string old = context.ReadState("items_json", "[]");
context.WriteState("items_json", newJson);
```

### 子程序调用示例

```csharp
var result = context.RunSp("子程序名", new Dictionary<string, object>
{
    { "input1", "abc" },
    { "input2", 123 }
});
```

### 异步方法等待技巧

Exec 是同步方法，不能直接 await。可以把 Task 存到变量，后续赋值步骤中 `await {task}` 等待：
```csharp
// csscript 步骤：启动异步，存 Task
var task = HttpClient.GetAsync(url);
context.SetVarValue("task", task);
// 后续赋值步骤：$= await {task}
```

## 线程选择（`runOnUiThread`）

| 值 | 适用场景 |
|----|----------|
| `ui` | 需要 WPF 控件、窗口、剪贴板操作时 |
| `sta` | 需要 STA 线程但不想占用 UI 线程时 |
| `staLongRun` | 需要独立 STA 线程且运行时间较长时 |
| `background` | 普通后台逻辑（不涉及 UI） |
| `auto` | 仅在确认脚本不涉及 UI/STA 时使用，**不是默认选择** |

**关键：** 涉及 WPF、剪贴板、窗口操作时，**必须**显式选 `ui` 或 `sta`，不要依赖 `auto`。

## 引用 DLL（v1）

```csharp
//css_reference C:\path\to\library.dll
//css_ref System.Net.Http.dll
```

## 注意事项

- 程序集按代码内容缓存，代码不变可复用（避免用文本插值生成脚本）
- 普通模式自动提权，可能无法通过 COM 控制第三方程序
- v2 首次编译冷启动慢，后续自动缓存
- WinForm 控件用后台线程（前台线程中文输入可能异常）

## C# 命名空间冲突（最高频错误）

命名冲突只出现在 **cscode / csscript**（完整 C# 代码）中，因为有 `using` 开头，多个命名空间同时引入时同名类型会冲突。赋值环境（`$=` 表达式）是简单代码片段，不会有命名冲突。

以下类型在 cscode/csscript 中**必须写全限定名**：

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

## C# 变量与语法

- **`var` 不允许多声明**：`var a = 1, b = 2;` 是错的，必须拆成 `var a = 1; var b = 2;`。显式类型（`int`, `bool`）可以但不建议
- **同一方法内变量名不能重复**：检查所有局部变量名在方法内是否唯一，特别是多个用途的 `ox`/`oy` 等常见命名
- **类型别名不存在**：不要用 `F<Tb>` 这种自造别名，直接写 `F<TextBox>`
- **跨类访问**：从一个类调用另一个类的方法，该方法必须是 `public static`
- **删除未使用的字段/变量**：编译器会警告，影响可信度

## XAML 规则

- **Style 必须用 StaticResource**：`Style="{StaticResource Key}"`，不能写 `Style="{Key}"`
- **同一控件不能有重复属性**：特别是 `Text=` 同时有默认值和 Binding 的情况，只能保留一个
- **文件图标绑定**：`qk:IconControl` 需要 `icon:.txt` 格式，不能绑定完整路径。需要在数据模型中加 `IconKey` 属性

## 性能

- **避免逐像素 GetPixel**：读取多个像素时用 `BitBlt` + `GetBitmapBits` 批量读取，不要循环调用 `GetPixel`（每次都要和显卡通信，极慢）
- **Timer 间隔**：UI 刷新 Timer 不要低于 30ms，30-50ms 为宜

## 环境限制

- .NET Framework 4.7.2
- 普通模式 v1：C# 5.0
- 普通模式 v2（Roslyn）：C# 7.3

## C# 5.0 禁止使用的语法（cscode 和 csscript 均适用）

| 写法 | 替代方案 |
|------|----------|
| `$"Hello {name}"` | `string.Format("Hello {0}", name)` 或 `"Hello " + name` |
| `obj?.Method()` | `if (obj != null) obj.Method()` |
| `public int X => 1;` | `public int X { get { return 1; } }` |
| `nameof(param)` | `"param"` |
| `catch (Exception ex) when (...)` | 不支持，拆成多个 catch |
| `using static System.Math;` | 不支持，写全名 `Math.Abs()` |
| `if (obj is Type v)` | `var v = obj as Type; if (v != null)` |

> **注意：** lambda 表达式允许，如 `Func<int, int> f = x => x + 1;`

## 定义公共方法

可在赋值表达式中定义 `public` 方法，后续通过 `{方法名}` 调用：

```
$=
public int Add(int a, int b)
{
    return a + b;
}
```

输出给变量 `Add`，之后调用：`$= {Add}(4, 5)`

## Lambda 与委托

```csharp
// Func<参数类型, 返回类型>
Func<int, int, int> add = (x, y) => x + y;

// Action（无返回值）
Action<string> greet = name => Console.WriteLine("Hello " + name);
```

## Quicker 内置可用 DLL（`C:\Program Files\Quicker\`）

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
