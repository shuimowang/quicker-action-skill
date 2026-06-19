# 自定义窗口 (`sys:customwindow`)

创建 WPF 窗口，支持 XAML 布局和数据绑定。

## InputParams

| 参数 | 说明 |
|------|------|
| `type` | `"ShowAndWaitClose"` 显示并等待关闭 / `"Show"` 显示不等待 / `"Close"` 关闭窗口 / `"GetWindows"` 检测已有窗口（OutputParams 中 `windowList` 接收结果） |
| `windowMarkup` | WPF XAML 代码 |
| `dataMapping` | 数据映射（多行文本） |
| `windowId` | 窗口标识（用于关闭） |
| `cscode` | 辅助 C# 代码（可选） |
| `events` | 事件处理（可选） |
| `closeWhenDeactivate` | 失去焦点时关闭，`"true"` / `"false"` |
| `autoCloseTime` | 自动关闭秒数，0为不自动 |
| `activateMode` | `"NotActivatable"` / `"NotActivatableMouseThrough"` / `"NotActivated"` / `"AutoActivate"` |
| `winLocation` | 窗口位置：`"Auto"` / `"CenterScreen"` / `"TopRight"` / `"BottomRight"` / `"TopLeft"` / `"BottomLeft"` / `"TopCenter"` / `"BottomCenter"` / `"LastPosition"` / `"FullScreen"` / `"Manual"` / `"Maximized"` 等 |
| `winSize` | 窗口尺寸，如 `"300,200"` 或 `"50%,50%"` |
| `stopIfFail` | 失败停止，`"0"` / `"1"` |

## OutputParams

`isSuccess`、`result`（窗口结果）、`windowLocation`、`errMessage`

## XAML 注意事项

自定义窗口步骤的 XAML 和普通 WPF 工程不同，有以下限制：

- 去掉 `x:Class` 属性
- `xmlns:qk="https://getquicker.net"` 仅在使用 `qk:` 前缀控件（如 `qk:IconControl`）时才需要声明，等价于 `Quicker.View.Controls`
- **不能用字符串绑定事件**：`Loaded="OnLoaded"`、`Click="OnClick"` 等写法会报错，
  事件必须在 cscode 中处理
- 静态命令按钮优先用 `Tag` + `OnButtonClicked` 分发；右键、长按、拖拽、文本变化、动态控件等场景用 `+=` 绑定对应事件
- 按钮操作：`qk:Att.Action="操作内容"`（存在但不推荐，复杂逻辑放在 cscode 中）

### 自定义标题栏（WindowStyle="None"）

使用 `WindowStyle="None"` 时，建议添加 `WindowChrome` 保持窗口圆角一致：

```xml
<Window ...
        xmlns:shell="clr-namespace:System.Windows.Shell;assembly=PresentationFramework"
        WindowStyle="None" AllowsTransparency="True" Background="Transparent">
    <shell:WindowChrome.WindowChrome>
        <shell:WindowChrome GlassFrameThickness="0" CornerRadius="5" CaptionHeight="0"/>
    </shell:WindowChrome.WindowChrome>
    <Border BorderThickness="1" CornerRadius="5" Background="White">
        <!-- 内容 -->
    </Border>
</Window>
```

`WindowChrome` 让窗口边框和内容区的圆角对齐，避免默认直角与自定义圆角不一致。

**搜索框等需要实时响应的控件**：不要用 `{Binding}`，
在 cscode 中 `FindName` 获取控件后绑定 `TextChanged` 等事件。
因为自定义窗口的 dataContext 是全部通知，绑定容易产生意外行为。

## 数据映射格式（每行一个）

```
窗口数据名:{动作变量名}           # 关联变量（开窗口取值，关窗口写回）
数据项名:=(int)0                  # 初始化内部数据
数据项名:$= {number1} + {number2} # 动态计算
```

## 按钮操作

冒号必须有，即使是关闭不返回值也要写 `close:`：

```
close:           # 关闭窗口，结果为空
close:返回值      # 关闭并返回结果
operation=copy&data={text}   # 复制到剪贴板
operation=paste&data={text}  # 粘贴到目标窗口
operation=open&data=https://example.com  # 打开网址
```

## 辅助 C# 回调

cscode 只支持以下三个回调，不存在 `OnWindowClosing`、`OnWindowClosed` 等其他回调。不需要辅助 C# 时将 `cscode` 设为空字符串；只要填写了 C# 代码，就必须定义 `OnWindowCreated`，即使方法体为空。

cscode 使用 **C# 5.0**，不能写 `$""` 插值、`?.`、表达式体成员等。

### 回调执行时序

反编译确认的 Quicker 内部流程：

```
Window win = XamlReader.Load(xaml) as Window;   // XAML 解析成完整 Window 对象
win.DataContext = dataContext;                    // 挂载数据上下文
winContext.Window = win;                          // 赋值窗口引用
// 注册部分宿主级事件（拖动、缩放等）
★ OnWindowCreated(win, dataContext, winContext)   // 回调
win.Show();                                       // 显示窗口
// WPF 加载流程 → window.Loaded 事件触发
★ OnWindowLoaded(win, dataContext, winContext)    // 回调（通过 Loaded += delegate 注册）
```

**OnWindowCreated 时的状态：**
- `XamlReader.Load` 已完成，XAML 中带 `x:Name` 的控件已实例化
- `win.FindName("xxx")` 可用，能找到控件
- DataContext 已挂载，数据绑定已生效
- 窗口尚未 Show，不在可视化树中，Loaded 尚未触发

**OnWindowLoaded 时的状态：**
- 窗口已进入可视化树，WPF `Loaded` 事件已触发
- 适合绑定需要可视化树参与的事件（键盘、焦点等）

### ICustomWindowContext 接口

```csharp
// Quicker.Public.ICustomWindowContext
public interface ICustomWindowContext
{
    Task<IDictionary<string, object>> RunSpAsync(string spName, IDictionary<string, object> inputParams);
    Task<IDictionary<string, object>> RunSpAsync(string spName, object inputParams);
    IDictionary<string, object> RunSp(string spName, IDictionary<string, object> inputParams);
    IDictionary<string, object> RunSp(string spName, object inputParams);
}
```

只有这 4 个方法，没有 `Close` 等其他方法。

```csharp
using System.Windows;
using System.Collections.Generic;
using Quicker.Public;  // ICustomWindowContext

// OnWindowCreated 必须存在，即使为空
public static void OnWindowCreated(
    Window win,
    IDictionary<string, object> dataContext,
    ICustomWindowContext winContext) { }

// 可选
public static void OnWindowLoaded(
    Window win,
    IDictionary<string, object> dataContext,
    ICustomWindowContext winContext) { }

// 可选，按钮点击回调
// controlName 对应 x:Name，controlTag 对应 Tag 属性
public static bool OnButtonClicked(
    string controlName,
    object controlTag,
    Window win,
    IDictionary<string, object> dataContext,
    ICustomWindowContext winContext)
{
    return true; // 返回 true 保持窗口不关闭
}
```

**静态命令按钮：** 用 `Tag="xxx"`，在 `OnButtonClicked` 中检查 `controlTag`；返回 `true` 保持窗口。

**特殊交互按钮：** 需要右键、长按、拖拽、动态生成等事件时，用 `+=` 绑定具体事件。

**按钮关闭窗口：** 在 `OnButtonClicked` 或对应事件中用 `win.Close()`，复杂逻辑不要依赖 `qk:Att.Action`。

```csharp
// XAML: <Button x:Name="btnClose" Content="关闭" Tag="Close"/>
if (controlName == "btnClose")
{
    win.Close();
    return false;
}
```

## 进阶用法

### 隐藏启动

自定义窗口模块的 `Show()` 无法被阻止，如果需要窗口创建后不立即显示（如托盘图标、后台窗口），用 `Opacity=0` 吞掉首次显示：

XAML 需要设置（配合 WindowChrome 保持圆角一致）：
```xml
<Window ...
        xmlns:shell="clr-namespace:System.Windows.Shell;assembly=PresentationFramework"
        WindowStyle="None" AllowsTransparency="True" Background="Transparent" Opacity="0">
    <shell:WindowChrome.WindowChrome>
        <shell:WindowChrome GlassFrameThickness="0" CornerRadius="5" CaptionHeight="0"/>
    </shell:WindowChrome.WindowChrome>
    <Border BorderThickness="1" CornerRadius="5" Background="White">
        <!-- 内容 -->
    </Border>
</Window>
```

cscode：
```csharp
public static void OnWindowLoaded(Window win, IDictionary<string, object> dataContext, ICustomWindowContext winContext)
{
    win.Hide();       // 隐藏窗口
    win.Opacity = 1;  // 恢复透明度，后续 Show 时正常显示
}
```

原理：`Opacity=0` 让首次 Show 不可见，`OnWindowLoaded` 中立即 Hide 并恢复透明度。之后调用 `win.Show()` 即可正常显示。

### 常用事件绑定

```csharp
btn.Click += (s, e) => { };                       // 左键点击
btn.MouseRightButtonUp += (s, e) => { };          // 右键点击
btn.PreviewMouseLeftButtonDown += (s, e) => { };   // 鼠标按下（长按检测）
win.MouseLeftButtonDown += (s, e) => { win.DragMove(); }; // 拖动窗口
```

### 键盘模拟（需 using System.Windows.Forms）

```csharp
System.Windows.Forms.SendKeys.SendWait("{ENTER}");   // 发送按键
System.Windows.Forms.SendKeys.SendWait("^c");        // Ctrl+C
```

### 长按/定时器（DispatcherTimer）

```csharp
var timer = new DispatcherTimer();
timer.Interval = TimeSpan.FromMilliseconds(400);
timer.Tick += (s, e) => { /* 重复操作 */ };
timer.Start();
// timer.Stop();
```

### 通知提示（需 using Quicker.Utilities）

`AppHelper` 使用 ToastNotifications，不阻塞进程，
仅在 cscode 和 C# 脚本步骤中可用：

```csharp
using Quicker.Utilities;
AppHelper.ShowInformation("提示消息");
AppHelper.ShowSuccess("成功消息");
AppHelper.ShowWarning("警告消息");
AppHelper.ShowError("错误消息", false); // 第二个参数 false 避免阻塞
```

### WebView2 控件

嵌入浏览器渲染 HTML/JS，需引用：

```csharp
using Microsoft.Web.WebView2.Wpf;  // WebView2 控件
using Microsoft.Web.WebView2.Core;  // CoreWebView2
using System.IO;                     // Path
```

XAML：

```xml
<Window xmlns:wv2="clr-namespace:Microsoft.Web.WebView2.Wpf;assembly=Microsoft.Web.WebView2.Wpf">
  <wv2:WebView2 x:Name="webView" />
</Window>
```

初始化 boilerplate：

```csharp
public static WebView2 webView;

webView = win.FindName("webView") as WebView2;

win.SourceInitialized += async (sender, e) =>
{
    // 指定数据目录，防止默认路径权限问题
    var folder = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
        "Quicker", "WebView2");
    var env = await CoreWebView2Environment.CreateAsync(null, folder).ConfigureAwait(true);

    webView.CoreWebView2InitializationCompleted += (s, args) =>
    {
        if (args.IsSuccess)
        {
            webView.CoreWebView2.Navigate("https://example.com/");
        }
        else
        {
            AppHelper.ShowError("WebView2 初始化失败:" + args.InitializationException.Message, false);
        }
    };

    await webView.EnsureCoreWebView2Async(env).ConfigureAwait(true);
};

win.Closed += (sender, e) =>
{
    if (webView != null) webView.Dispose();
};
```

### 获取网站 Favicon

```
https://helperservice.getquicker.cn/favicon/get/{域名}
```

例如：`https://helperservice.getquicker.cn/favicon/get/getquicker.net`，
返回图片。可在 `qk:IconControl` 或 `<Image>` 中直接使用。

## 多实例处理

一般将 `LimitSingleInstance` 设为 `false`。不允许重复打开窗口时，应显式处理多实例；需求明确允许多个窗口时，可省略检测，但不同窗口应使用可区分的 `windowId`。

### 推荐：网络共享子程序

使用"自定义窗口检测"网络共享子程序，一步搞定（详见 [网络共享子程序](network-subprograms.md)）：

```json
{
  "StepRunnerKey": "sys:subprogram",
  "InputParams": {
    "subProgram": {"VarKey": null, "Value": "@@3d7a8957-8ae3-4cd7-5327-08ddb0c7f7f4@7@自定义窗口检测"},
    "var:窗口标识": {"VarKey": null, "Value": "$=_context.ActionId"},
    "var:窗口操作": {"VarKey": null, "Value": "关闭窗口"},
    "stopIfFail": {"VarKey": null, "Value": "1"},
    "skipDebugOutput": {"VarKey": null, "Value": "1"}
  },
  "OutputParams": {"isSuccess": null, "errMessage": null}
}
```

在 `ShowAndWaitClose` 步骤前执行此子程序即可确保单实例。

### 手动实现

窗口通过 `windowId` 标识查找，GetWindows 和 ShowAndWaitClose 必须使用相同的 `windowId`。
如果动作只有一个窗口，可以用 `$=_context.ActionId` 作为标识。

```
步骤1: GetWindows → windowList
步骤2: If windowList.Any() → 执行策略
步骤3: ShowAndWaitClose → 显示新窗口（仅停止策略不需要此步）
```

#### 策略选择（按优先级）

| 优先级 | 做法 | 说明 |
|--------|------|------|
| 1 | `sys:stop` 停止动作，沿用旧窗口 | 最简单，旧窗口继续运行 |
| 2 | 关闭旧窗口，停止动作 | 需要刷新窗口内容 |
| 3 | 激活旧窗口，停止新实例 | 需要保留旧窗口状态 |

#### 策略一：停止动作（推荐）

步骤2 IfSteps 中放 `sys:stop`，无需步骤3。

### 策略二：关闭旧窗口，停止动作

```json
// 步骤1: 获取窗口列表
{
  "StepRunnerKey": "sys:customwindow",
  "InputParams": {
    "type": {"VarKey": null, "Value": "GetWindows"},
    "windowId": {"VarKey": null, "Value": "$=_context.ActionId"},
    "stopIfFail": {"VarKey": null, "Value": "0"}
  },
  "OutputParams": {
    "isSuccess": null,
    "windowList": "windowList",
    "errMessage": null
  }
}
// 步骤2: 关闭已有窗口并停止
{
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": {
    "condition": {"VarKey": null, "Value": "$={windowList}.Any()"}
  },
  "IfSteps": [
    {
      "StepRunnerKey": "sys:assign",
      "InputParams": {
        "input": {"VarKey": null, "Value": "$=\r\nSystem.Windows.Window window = {windowList}[0];\r\nwindow.Dispatcher.Invoke(() => { window.Close(); });"},
        "stopIfFail": {"VarKey": null, "Value": "1"}
      },
      "OutputParams": {"isSuccess": null, "output": null, "errMessage": null}
    },
    {
      "StepRunnerKey": "sys:stop",
      "InputParams": {
        "method": {"VarKey": null, "Value": "default"},
        "isError": {"VarKey": null, "Value": "0"},
        "return": {"VarKey": null, "Value": ""},
        "showMessage": {"VarKey": null, "Value": ""}
      },
      "OutputParams": {}
    }
  ]
}
// 步骤3: 显示新窗口（如果步骤2没有停止）
```

### 策略三：激活旧窗口，停止新实例

步骤2 IfSteps 中先 assign 激活，再 `sys:stop`：

```csharp
window.Dispatcher.Invoke(() => {
    window.Activate();
    window.Show();
    window.WindowState = System.Windows.WindowState.Normal;
});
```

## 最简示例（输入框+确定按钮+Escape关闭）

XAML：

```xml
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="输入" Width="300" Height="150">
  <StackPanel Margin="10">
    <TextBox x:Name="InputBox" Margin="0,0,0,10"/>
    <StackPanel Orientation="Horizontal" HorizontalAlignment="Right">
      <Button Content="确定" Tag="ok" Margin="0,0,8,0"/>
      <Button Content="取消" Tag="cancel"/>
    </StackPanel>
  </StackPanel>
</Window>
```

cscode：

```csharp
using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Collections.Generic;
using Quicker.Public;

static Window _win;
static TextBox _inputBox;

public static void OnWindowCreated(Window win, IDictionary<string, object> dataContext, ICustomWindowContext winContext)
{
    _win = win;
}

public static void OnWindowLoaded(Window win, IDictionary<string, object> dataContext, ICustomWindowContext winContext)
{
    _inputBox = win.FindName("InputBox") as TextBox;
    win.PreviewKeyDown += OnWindowKeyDown;
}

public static bool OnButtonClicked(string controlName, object controlTag, Window win, IDictionary<string, object> dataContext, ICustomWindowContext winContext)
{
    string tag = controlTag != null ? controlTag.ToString() : "";

    if (tag == "ok")
    {
        dataContext["result"] = _inputBox.Text;
        win.Close();
        return false;
    }

    if (tag == "cancel")
    {
        win.Close();
        return false;
    }

    return true;
}

static void OnWindowKeyDown(object sender, KeyEventArgs e)
{
    if (e.Key == Key.Escape)
    {
        _win.Close();
        e.Handled = true;
    }
}
```

## 最简示例（输入框+确定按钮，旧写法参考）

> 此示例使用 `qk:Att.Action="close:ok"` 关闭窗口（旧写法）。
> 推荐方式是在 cscode 中用 `win.Close()` 关闭，见上方"按钮关闭窗口"。

完整 JSON：

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
  "IfSteps": [],
  "ElseSteps": [],
  "Note": "",
  "Disabled": false,
  "Collapsed": false,
  "DelayMs": 0
}
```
