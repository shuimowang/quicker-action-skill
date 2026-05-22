# 自定义窗口 (`sys:customwindow`)

创建 WPF 窗口，支持 XAML 布局和数据绑定。

## InputParams

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
| `activateMode` | `"AutoActivate"` / `"NoActivate"` / `"None"` |
| `winLocation` | 窗口位置：`"Auto"` / `"CenterScreen"` / `"TopRight"` / `"BottomRight"` / `"TopLeft"` / `"BottomLeft"` / `"TopCenter"` / `"BottomCenter"` / `"LastPosition"` / `"FullScreen"` / `"Manual"` / `"Maximized"` 等 |
| `winSize` | 窗口尺寸，如 `"300,200"` 或 `"50%,50%"` |
| `stopIfFail` | 失败停止，`"0"` / `"1"` |

## OutputParams

`isSuccess`、`result`（窗口结果）、`windowLocation`、`errMessage`

## XAML 注意事项

自定义窗口步骤的 XAML 和普通 WPF 工程不同，有以下限制：

- 去掉 `x:Class` 属性
- 必须注册命名空间：`xmlns:qk="https://getquicker.net"`
  （即使不用 qk:Att.Action 也要加）
- **不能用字符串绑定事件**：`Loaded="OnLoaded"`、`Click="OnClick"` 等写法会报错，
  事件必须在 cscode 中通过代码绑定
- 按钮操作：`qk:Att.Action="操作内容"`

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

cscode 使用 **C# 5.0**，不能写 `$""` 插值、`?.`、表达式体成员等。

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

**按钮触发回调（不关闭窗口）：** 用 `Tag="xxx"`，在 OnButtonClicked 中检查 `controlTag`，返回 `true` 保持窗口。

**按钮关闭窗口：** 用 `qk:Att.Action="close:返回值"`

## 进阶用法

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
```

### 获取网站 Favicon

```
https://helperservice.getquicker.cn/favicon/get/{域名}
```

例如：`https://helperservice.getquicker.cn/favicon/get/getquicker.net`，
返回图片。可在 `qk:IconControl` 或 `<Image>` 中直接使用。

## 单实例窗口（防止重复打开）

cscode 中有静态字段时，多次触发动作会产生多个窗口。
在自定义窗口步骤前检测已有窗口，根据不同需求选择策略。

窗口通过 `windowId` 标识查找，GetWindows 和 ShowAndWaitClose 必须使用相同的 `windowId`。
如果动作只有一个窗口，可以用 `$=_context.ActionId` 作为标识。

```
步骤1: GetWindows → windowList
步骤2: If windowList.Any() → 执行策略
步骤3: ShowAndWaitClose → 显示新窗口（仅关闭/停止策略不需要此步）
```

### 策略一：关闭旧窗口，打开新窗口

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
// 步骤2: 关闭已有窗口
{
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": {
    "condition": {"VarKey": null, "Value": "$={windowList}.Any()"}
  },
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

### 策略二：停止动作，沿用旧窗口

步骤2 IfSteps 中放 `sys:stop`，无需步骤3。

### 策略三：激活旧窗口

步骤2 IfSteps 中 assign：

```csharp
window.Dispatcher.Invoke(() => {
    window.Activate();
    window.Show();
    window.WindowState = System.Windows.WindowState.Normal;
});
```

再加 `sys:stop`。

## 最简示例（输入框+确定按钮）

XAML 内容（`windowMarkup` 的 Value）：

```xml
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:qk="https://getquicker.net"
        Title="输入" Width="300" Height="150">
  <StackPanel Margin="10">
    <TextBox Text="{Binding [input]}" Margin="0,0,0,10"/>
    <Button Content="确定" qk:Att.Action="close:ok"/>
  </StackPanel>
</Window>
```

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
