# C# 脚本规则

## Exec 方法签名

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

| 属性 | 说明 |
|------|------|
| `ActionId` | 当前动作 ID（常用作窗口标识 `$=_context.ActionId`） |
| `InputParam` | 右键菜单/外部调用传入的参数 |
| `ParentWindow` | 父窗口引用 |
| `ActiveWindowHwnd` | 当前活动窗口句柄 |
| `RootContext` | 主程序上下文 |
| `ParentContext` | 直接调用者上下文 |
| `TextData` | 文本数据 |
| `ImageData` | 图片数据 |

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

## IStepContext 完整方法列表

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
