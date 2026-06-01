# KkjQuicker 参考文档 (v1.0.7)

KkjQuicker 是 Quicker 的扩展 DLL 包。
XAML 命名空间：`xmlns:kk="https://kkjquicker.net/xaml"`

---

## AI：OpenAI 兼容客户端

**命名空间：** `KkjQuicker.AI.OpenAI`

### OpenAiCompatibleClient

```csharp
var ai = new OpenAiCompatibleClient(apiUrl, apiKey, model);

// 简单调用
string result = await ai.ChatAsync("你好");
await ai.ChatStreamAsync("你好", chunk => { /* 处理每个 chunk */ }, token);

// 完整请求
var response = await ai.ChatAsync(request);
await ai.ChatStreamAsync(request, chunk => { ... }, token);

// 会话管理
IReadOnlyList<ChatMessage> history = ai.GetHistory(sessionId);
ai.ClearSession(sessionId);
ai.ClearAllSessions();
```

**特性：** 基于会话的多轮对话管理、SSE 流式解析、自动适配多种 OpenAI 兼容端点（DeepSeek、OpenAI 等）、线程安全会话存储、可配置最大消息数。

### ChatRequest（Fluent Builder）

```csharp
var request = new ChatRequest("用户消息")
    .WithSystem("系统提示词")
    .WithSession("session-1")        // 与 WithHistory 互斥
    .WithTemperature(0.7)            // 0~2
    .WithTopP(0.9)                   // 0~1
    .WithMaxTokens(4096)
    .WithStop("STOP")
    .WithResponseFormat("json_object")
    .WithExtra("key", value);        // 自定义参数，不可覆盖保留键
```

**保留键（WithExtra 不可覆盖）：** model, messages, stream, max_tokens, temperature, top_p, stop, response_format

### 图片请求（多模态）

```csharp
var request = new ChatRequest().WithRawMessages(new List<object>
{
    new
    {
        role = "user",
        content = new object[]
        {
            new { type = "image_url", image_url = new { url = base64String } },
            new { type = "text", text = "描述这张图片" }
        }
    }
});
```

### ChatResponse

```csharp
ChatResponse response = await ai.ChatAsync(request);
string content = response.Content;              // 快捷取第一个 choice
string id = response.Id;
List<ChatResponseChoice> choices = response.Choices;
TokenUsage usage = response.Usage;              // PromptTokens, CompletionTokens, TotalTokens
```

### ChatMessage

```csharp
ChatMessage.User("内容");
ChatMessage.Assistant("内容");
ChatMessage.System("内容");
// 属性：Role, Content（只读）
```

---

## AI：阿里云实时语音识别 (ASR)

**命名空间：** `KkjQuicker.AI.ASR.AliyunRealtime`

### AliyunRealtimeAsrClient

```csharp
var options = new AliyunRealtimeAsrOptions
{
    Language = "zh-CN",
    AutoStartAudio = true,
    EnableServerVad = true,
    SilenceDurationMs = 800,
    VadThreshold = 0.5
};

var client = new AliyunRealtimeAsrClient(options);

// 连接并开始识别
await client.StartAsync(token);

// 发送音频数据
await client.AppendAudioAsync(pcm16Bytes, token);

// 结束
await client.SendCommitAsync(token);
await client.StopAsync(token);

// 状态
bool isRunning = client.IsRunning;
bool isConnected = client.IsConnected;
```

---

## 音频处理

**命名空间：** `KkjQuicker.Audio`

### AudioDeviceHelper

```csharp
bool hasInput = AudioDeviceHelper.HasInputDevice();
bool hasOutput = AudioDeviceHelper.HasOutputDevice();
int count = AudioDeviceHelper.GetInputDeviceCount();
IReadOnlyList<string> names = AudioDeviceHelper.GetInputDeviceNames();
string defaultOutput = AudioDeviceHelper.GetDefaultOutputDeviceName();
```

### 音频源

```csharp
// 系统音频采集
var loopback = new LoopbackAudioSource();
loopback.Start();
bool running = loopback.IsRunning;
loopback.Stop();
loopback.Dispose();

// 麦克风采集
var mic = new MicrophoneAudioSource();
mic.Start();
// ...
mic.Stop();
mic.Dispose();
```

---

## 网络：WebSocket 客户端

**命名空间：** `KkjQuicker.Net.WebSockets`

### ReliableWebSocketClient

```csharp
var options = new WebSocketClientOptions
{
    Url = "wss://example.com/ws",
    ConnectTimeout = TimeSpan.FromSeconds(10),
    KeepAliveInterval = TimeSpan.FromSeconds(30),
    MaxMessageBytes = 1024 * 1024,
    Headers = new Dictionary<string, string> { { "Authorization", "Bearer xxx" } },
    Reconnect = new WebSocketReconnectOptions
    {
        Enabled = true,
        InitialDelay = TimeSpan.FromSeconds(1),
        MaxDelay = TimeSpan.FromSeconds(30),
        MaxRetries = 5,
        UseExponentialBackoff = true
    }
};

var client = new ReliableWebSocketClient(options);
await client.ConnectAsync(token);

bool connected = client.IsConnected;
WebSocketState state = client.State;

await client.SendTextAsync("message", token);
await client.SendBinaryAsync(data, token);

await client.DisconnectAsync();
client.Dispose();
```

---

## 网络：HTTP 客户端

**命名空间：** `KkjQuicker.Net.Http`

### HttpClients

```csharp
HttpClient client = HttpClients.Default;   // 进程级单例，自动 GZip/Deflate
HttpClient client = HttpClients.Create();   // 独立实例
HttpClient client = HttpClients.Create(handler => { /* 配置 */ }, TimeSpan.FromSeconds(30));
```

### SseStreamReader

```csharp
var reader = new SseStreamReader();
await reader.ReadAsync(response, message => {
    // 处理每个 SSE 消息
}, token);
```

---

## 剪贴板历史

**命名空间：** `KkjQuicker.Domain.ClipboardHistory`

### ClipboardItem（基类）

```csharp
ClipboardItem item = ...;
string id = item.Id;
string itemType = item.ItemType;
string copiedFrom = item.CopiedFrom;
bool isFavorite = item.IsFavorite;
DateTime recordTime = item.RecordTime;
```

### TextClipboardItem

```csharp
TextClipboardItem textItem = ...;
string text = textItem.Text;
string html = textItem.HtmlText;
string icon = textItem.Icon;
```

### FileClipboardItem

```csharp
FileClipboardItem fileItem = ...;
string[] paths = fileItem.FilePaths;
```

### ImageClipboardItem

```csharp
ImageClipboardItem imgItem = ...;
string path = imgItem.ImagePath;
string hash = imgItem.ImageHash;
int width = imgItem.PixelWidth;
int height = imgItem.PixelHeight;
```

---

## 覆盖层引擎

**命名空间：** `KkjQuicker.Overlay`

### OverlayRunner（静态便捷方法）

```csharp
// 全屏截图覆盖层 → 返回裁剪后的 BitmapSource
BitmapSource screenshot = await OverlayRunner.RunScreenshotLayer();

// 屏幕位置水波纹通知
OverlayRunner.NotifyWithRipple(screenCenterDip, rippleColor);

// 呼吸边框警报，返回 IDisposable 句柄
IDisposable alert = OverlayRunner.StartBreathingAlert(
    color, thickness, cycleSeconds, priority, autoCloseSeconds);
```

### OverlaySidebarHost（侧边栏）

```csharp
var sidebar = new OverlaySidebarHost();
sidebar.Dock = OverlaySidebarDock.Right;
sidebar.Alignment = OverlaySidebarAlignment.Center;
sidebar.SidebarWidth = 300;
sidebar.SidebarHeight = 600;
sidebar.Gap = 10;
sidebar.TopMost = true;
sidebar.ForceTopMostViaWin32 = true;

sidebar.Open();
sidebar.Close();
sidebar.Toggle();

sidebar.ApplyChrome();
sidebar.ApplyLayout();
sidebar.UpdateLayout(dock, alignment, width, height, gap);

bool isOpen = sidebar.IsOpen;
```

### ScreenshotEditorLayer（截图编辑器）

```csharp
var options = new EditorOptions
{
    DefaultThickness = 3.0,
    MosaicPixelSize = 10,
    MosaicStrokeThickness = 20.0,
    OnError = ex => { /* 处理错误 */ }
};

var layer = new ScreenshotEditorLayer(options);
// 在覆盖层引擎中使用
```

---

## 窗口停靠

**命名空间：** `KkjQuicker.Overlay.Docking`

### WindowDockManager

```csharp
var manager = new WindowDockManager();
manager.Configure(new WindowDockOptions
{
    EdgeTriggerPixels = 5,
    AnimationDurationSeconds = 0.3,
    HideFromTaskbarWhenDocked = true,
    BounceBackOnMouseUp = true
});

manager.Start();
manager.Stop();

bool added = manager.TryAdd(hwnd);
bool removed = manager.Remove(hwnd);
bool toggled = manager.Toggle(hwnd);
bool contains = manager.Contains(hwnd);

WindowDockSnapshot[] items = manager.GetItems();
int count = manager.Count;
bool isRunning = manager.IsRunning;

manager.RestoreAll();
manager.Clear();
```

### WindowDockSnapshot

```csharp
WindowDockSnapshot snapshot = ...;
IntPtr handle = snapshot.Handle;
string title = snapshot.Title;
string processPath = snapshot.ProcessFilePath;
DockSide side = snapshot.Side;      // Left, Right, Top, Bottom
bool isDocked = snapshot.IsDocked;
bool taskbarHidden = snapshot.TaskbarHiddenByEngine;
```

---

## UI 基础设施

**命名空间：** `KkjQuicker.UI`

### ViewModelBase

```csharp
public class MyViewModel : ViewModelBase
{
    private string _name;
    public string Name
    {
        get { return _name; }
        set { SetProperty(ref _name, value); }
    }
}
```

自动将 PropertyChanged 编组到 Dispatcher 线程。`SuspendNotifications()` 返回可嵌套的暂停作用域。

### CommandFactory

```csharp
var cmd = CommandFactory.Create(() => DoSomething());
var cmd = CommandFactory.Create<string>(text => Process(text));
var cmd = CommandFactory.CreateAsync(async () => await DoWork());           // 单次执行
var cmd = CommandFactory.CreateAsync<string>(async (text, token) => ...);   // 最新优先
```

### NotifierHelper

```csharp
var notifier = new NotifierHelper();
notifier.ShowSuccess("操作成功", () => { /* 点击回调 */ });
notifier.ShowError("操作失败", null);
notifier.ShowWarning("警告信息", null);
notifier.ShowInformation("提示信息", null);
bool initialized = notifier.IsInitialized;
```

### UiThread

```csharp
bool isUi = UiThread.CheckAccess();
UiThread.Run(() => { /* 在 UI 线程执行 */ });
UiThread.RunAndWait(() => { /* 同步等待 UI 线程执行 */ });
```

### DialogHelper

```csharp
string path = DialogHelper.ShowSaveFileDialog(filter, defaultName);
string path = DialogHelper.ShowSelectFileDialog(filter, defaultName);
string path = DialogHelper.ShowSelectFolderDialog(defaultPath);
```

---

## 全局钩子

**命名空间：** `KkjQuicker.Utilities.Hooks`

### GlobalKeyboardHook

```csharp
var hook = new GlobalKeyboardHook();
hook.KeyDown += (sender, e) => {
    uint vk = e.VirtualKeyCode;
    bool alt = e.IsAltDown;
    e.Handled = true;  // 阻止传递
};
hook.Install();
hook.Uninstall();
hook.Dispose();
```

### GlobalMouseHook

```csharp
var hook = new GlobalMouseHook();
hook.MouseMove += (sender, e) => {
    int x = e.X, y = e.Y;
    MouseMessage msg = e.Message;
    e.Handled = true;
};
hook.Install();
hook.Uninstall();
hook.Dispose();
```

### GlobalHotkey

```csharp
var hotkey = new GlobalHotkey(hwnd, id, modifiers, key, callback);
hotkey.Dispose();
```

---

## 窗口监控

**命名空间：** `KkjQuicker.Utilities.Win32`

### ForegroundWindowMonitor

```csharp
var monitor = new ForegroundWindowMonitor();
monitor.ForegroundChanged += (sender, e) => {
    ForegroundWindowInfo activated = e.ActivatedWindow;
    ForegroundWindowInfo deactivated = e.DeactivatedWindow;
};

monitor.Start();
monitor.Start(refreshImmediately: true);
monitor.Stop();

ForegroundWindowInfo current = monitor.CurrentWindow;
ForegroundWindowInfo lastExternal = monitor.LastExternalWindow;
IntPtr currentHwnd = monitor.CurrentHwnd;

monitor.Refresh();
monitor.Refresh(forceRaise: true);
bool activated = monitor.TryActivateLastExternalWindow();
```

### ForegroundWindowInfo

```csharp
ForegroundWindowInfo info = ...;
IntPtr handle = info.Handle;
string title = info.Title;
string className = info.ClassName;
int pid = info.Pid;
string processName = info.ProcessName;
string exePath = info.ExePath;
bool isEmpty = info.IsEmpty;
```

---

## IME 输入法管理

**命名空间：** `KkjQuicker.Utilities.Input`

### ImeHelper

```csharp
var ime = new ImeHelper();

ImeState state = ime.GetState(hwnd);
bool isChinese = ime.IsChineseMode(hwnd);
bool isOpen = ime.IsImeOpen(hwnd);
bool isFull = ime.IsFullShape(hwnd);

ime.SetChineseMode(true, hwnd);
ime.SetImeOpen(true, hwnd);

// 临时切换模式（返回 IDisposable，Dispose 时恢复）
using (ime.PushEnglishMode(hwnd)) { /* 英文模式 */ }
using (ime.PushImeOff(hwnd)) { /* IME 关闭 */ }
using (ime.PushState(targetState, hwnd)) { /* 指定状态 */ }

// 延迟配置
ime.StateChangeDelayMs = 50;
ime.SendMessageTimeoutMs = 100;
```

---

## FFmpeg 工具

**命名空间：** `KkjQuicker.Utilities.FFmpeg`

### FFmpegProcessHelper

```csharp
var helper = new FFmpegProcessHelper();

// 启动进程
Process process = helper.Start(ffmpegPath, arguments, workingDir,
    output => { /* stdout */ },
    error => { /* stderr */ });

// 同步执行
FFmpegProcessResult result = helper.Run(ffmpegPath, arguments, workingDir,
    timeoutMs, output => { }, error => { });

// 异步执行
FFmpegProcessResult result = await helper.RunAsync(ffmpegPath, arguments, workingDir,
    timeoutMs, token, output => { }, error => { });

// 停止
helper.TryKill(process);
bool stopped = helper.TryStopGracefully(process, waitMs);
```

### FFmpegCommandHelper

```csharp
var helper = new FFmpegCommandHelper();
string args = helper.BuildScreenRecordArguments(ffmpegPath, outputPath, options);
string quoted = helper.Quote(value);
```

---

## 文件系统工具

**命名空间：** `KkjQuicker.Utilities.FileSystemHelper`

```csharp
var fs = new FileSystemHelper();

// 读写
byte[] data = fs.ReadAllBytes(path);
string text = fs.ReadAllText(path);
string text = await fs.ReadAllTextAsync(path);
fs.WriteAllText(path, content);
await fs.WriteAllTextAsync(path, content);
fs.WriteAllBytes(path, bytes);

// 文件操作
fs.CopyFile(src, dst, overwrite);
fs.MoveFile(src, dst, overwrite);
fs.DeleteFile(path);
string renamed = fs.RenameFile(path, newName, overwrite);

// 目录操作
string dir = fs.EnsureDirectory(path);
fs.ClearDirectory(path);
fs.DeleteDirectory(path);

// 信息
long size = fs.GetFileSize(path);
string readable = fs.GetReadableFileSize(size);
string safeName = fs.GetSafeFileName(fileName);
string uniquePath = fs.GetUniqueFilePath(filePath);
string target = fs.GetLnkTargetPath(lnkPath);
Encoding enc = fs.GetTextFileEncoding(path);

// 资源管理器
fs.LocateInExplorer(path);
```

---

## XAML 转换器

**命名空间：** `KkjQuicker.UI.Converters`

| 转换器 | 说明 |
|--------|------|
| `BoolToVisibilityConverter` | True→Visible, False→Collapsed, 支持 IsReversed |
| `BoolToStringConverter` | True→"True", False→"False", ConverterParameter 可覆盖 |
| `EqualityToVisibilityConverter` | 相等→Visible, 不等→Collapsed, 支持 IsReversed, Comparison |
| `EqualityToStringConverter` | 相等→"True", 不等→"False" |
| `EqualityToBoolConverter` | 相等→true, 不等→false |
| `EqualityToObjectConverter` | 相等/不等→自定义对象 |
| `ValueCombineConverter` | 多值合并（拼接/求和），Separator 属性 |
| `ItemIndexConverter` | ItemsControl 容器的 1-based 索引 |
| `TakeConverter` | 取前 N 行/项 |
| `PathToFileNameConverter` | 路径→文件名 |
| `RelativeTimeConverter` | DateTime→相对时间 |
| `ColorAdjustConverter` | 颜色调整：Tint/Shade/Alpha |

Equality 系列 ConverterParameter 格式：`"CompareValue|TrueValue|FalseValue|NotEqualValue"`，支持 `{null}` 和 `{empty}` 占位符。

---

## 工具扩展

**命名空间：** `KkjQuicker.Utilities.Extensions`

### ObjectDictionaryExtensions

```csharp
string val = dict.GetString("key", "default");
bool flag = dict.GetBool("key", false);
int num = dict.GetInt("key", 0, min: 0, max: 100);
double dbl = dict.GetDouble("key", 0.0);
T obj = dict.GetValueOrNull("key") as T;
bool has = dict.HasValue("key");
```

### JsonExtensions

```csharp
string json = obj.ToJson(indented: true, ignoreNull: false, camelCase: true);
T obj = json.FromJson<T>();
bool valid = json.IsJson();
T clone = obj.DeepClone();
bool equal = JsonExtensions.JsonEquals(obj1, obj2);
```

### StringExtensions

```csharp
bool match = text.IsMatch(pattern);
string value = text.MatchValue(pattern, groupIndex);
bool any = text.ContainsAny("a", "b", "c");
bool starts = text.StartsWithAny(ignoreCase: true, "http://", "https://");
string[] lines = text.SplitLines(removeEmpty: true);
string preview = text.ToPreviewText(maxChars: 100, maxLines: 3);
string resolved = text.ResolveTemplate(template);
```

### ListExtensions

```csharp
list.AddRange(items);
T item = list.GetOrDefault(index);
int index = list.IndexOfByReference(item);
bool contains = list.ContainsByReference(item);
int removed = list.RemoveAll(x => x.IsDone);
List<T> distinct = source.DistinctBy(x => x.Id);
```

### IDictionaryExtensions

```csharp
target.MergeFrom(source, overwriteExisting: true);
target.EnsureDefaults(defaults);
IDictionary<string, object> ignoreCase = dict.ToIgnoreCase();
```

---

## 历史记录管理

**命名空间：** `KkjQuicker.Utilities.History`

### HistoryManager

```csharp
var manager = new HistoryManager(maxCapacity: 100);

manager.Execute(command);    // 执行并加入历史
manager.Push(command);       // 仅加入历史

bool canUndo = manager.CanUndo;
bool canRedo = manager.CanRedo;
manager.Undo();
manager.Redo();

bool isDirty = manager.IsDirty;
manager.MarkClean();

HistoryState state = manager.State;
manager.Clear();
manager.Dispose();
```

---

## Overlay UI 组件

**命名空间：** `KkjQuicker.UI.Adorners`

### OverlayPanel

```csharp
var panel = new OverlayPanel();
panel.AddChild(element, OverlayAnchor.TopLeft, offsetX: 10, offsetY: 10);
panel.RefreshVisibility();
IReadOnlyList<IOverlayItem> items = panel.Items;
```

### OverlayActionContext

```csharp
OverlayActionContext ctx = ...;
OverlayPanel panel = ctx.Panel;
T data = ctx.As<T>();
T result = ctx.Dispatch(func, defaultValue);
ctx.Dispatch(action);
```
