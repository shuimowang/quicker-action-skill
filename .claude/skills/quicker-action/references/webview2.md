# WebView2 浏览器窗口 (`sys:webview2`)

使用 Microsoft WebView2（Edge 浏览器内核）组件创建浏览器窗口。Windows 11 已预装 WebView2 运行时，其他系统需从 [Microsoft 开发者网站](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) 安装。

> **与 CustomWindow 嵌入 WebView2 的区别：**
> 本文档是 **WebView2 独立步骤模块**（StepRunnerKey 为 `sys:webview2`），直接创建浏览器窗口，无需 XAML。
> 如果需要在自定义窗口中嵌入 WebView2 控件（配合其他 WPF 控件），参见 [customwindow.md - WebView2 控件](customwindow.md#webview2-控件)。

---

## 操作类型（`type` 参数）

`type` 是控制字段，决定哪些参数可见。通过 `type` 参数的 `Value` 选择操作。

| type 值 | 名称 | 说明 |
|---------|------|------|
| `OpenUrl` | 打开网页 | 打开 URL 或 HTML，不等待加载，后续步骤立即执行 |
| `OpenAndWaitLoad` | 打开网页并等待加载完成 | 等待页面加载完成后才继续 |
| `OpenUrlAndWaitClose` | 打开网页并等待窗口关闭 | 暂停执行直到用户关闭窗口 |
| `SendMessage` | 发送消息 | 通过 `PostWebMessageAsJson` 向网页发送消息 |
| `ExecuteScript` | 执行脚本 | 在网页上下文中执行 JavaScript |
| `CheckWindowState` | 获取窗口状态 | 获取当前 URL、标题、加载状态、Cookie 等 |
| `Close` | 关闭窗口(如果尚未关闭) | 通过窗口标识关闭 |
| `Reload` | 重新加载/刷新 | 刷新当前网页 |
| `Stop` | 停止加载 | 停止页面加载 |
| `CheckInstalled` | 检查是否安装WebView2 | 检测运行时是否可用 |
| `MultiTab_OpenUrl` | 【多标签】打开网址 | 多个 URL 以标签页形式展示 |
| `MultiColumn_OpenUrl` | 【多列】打开网址 | 多个 URL 以左右分栏展示（适合移动端页面） |

---

## InputParams

### 网址或HTML内容

- **Key：** `url`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **类型：** 多行文本
- **说明：** 网页地址、文件路径或 HTML 代码内容

### 网址列表

- **Key：** `urlList`
- **适用操作：** `MultiTab_OpenUrl`, `MultiColumn_OpenUrl`
- **类型：** 多行文本
- **说明：** 每行一个，格式：
  ```
  网址
  标题|网址
  [图标]标题|网址
  ```

### 附加的浏览器参数

- **Key：** `additionalBrowserArguments`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **说明：** 用于设置代理等用途，如 `--proxy-server=http://127.0.0.1:8888`
- **注意：** 可能导致无法同时开启多个 WebView2 窗口

### 虚拟主机映射

- **Key：** `virtualHostToFolder`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **类型：** 多行文本
- **说明：** 将文件夹映射为虚拟主机名，格式：`主机名|文件夹路径`，多个时每行一个。在 HTML 中可用 `https://servername/path/to/file.png` 访问本地文件

### User Agent

- **Key：** `userAgent`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`, `MultiTab_OpenUrl`, `MultiColumn_OpenUrl`
- **说明：** 自定义 UserAgent

### 窗口标题

- **Key：** `title`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`, `MultiTab_OpenUrl`, `MultiColumn_OpenUrl`
- **说明：** 窗口标题文字。未设置时自动使用网页标题

### 窗口图标

- **Key：** `icon`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **说明：** 窗口左上角图标。支持 `fa:内置图标名:#RRGGBB` 或图标网址

### 默认背景色

- **Key：** `defaultBgColor`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **说明：** 设置窗口的默认背景色

### 窗口标识

- **Key：** `autoCloseKey`
- **适用操作：** 除 `CheckInstalled` 外所有操作
- **默认值：** `=`
- **说明：** 用于关闭之前打开的具有此标识的 WebView2 窗口。`=` 表示使用当前动作 ID

### 如果窗口已存在

- **Key：** `modeForExists`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`
- **默认值：** `SkipThisStep`

| 值 | 说明 |
|----|------|
| `SkipThisStep` | 跳过此步骤 |
| `UpdateUrl` | 更新网址 |
| `UpdateUrlAndPosition` | 更新网址和窗口位置 |
| `RecreateWindow` | 关闭并重建窗口 |
| `BringToFront` | 激活窗口 |

### JS脚本

- **Key：** `script`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`, `ExecuteScript`
- **类型：** 多行文本（JavaScript 高亮）
- **说明：**
  - 打开操作时：页面加载后注入的 JavaScript（通过 `AddScriptToExecuteOnDocumentCreatedAsync` 注入）
  - `ExecuteScript` 时：通过 `ExecuteScriptAsync` 执行的代码，仅在顶层文档执行，不对 iframe

### 消息内容

- **Key：** `sendMessage`
- **适用操作：** `SendMessage`
- **类型：** 多行文本
- **说明：** JSON 格式的消息内容。词典变量会自动转换成 JSON

### 附加对象

- **Key：** `additionalObjects`
- **适用操作：** `SendMessage`
- **类型：** 多行文本
- **说明：** `PostWebMessageAsJson` 的附加对象列表参数内容，目前支持路径的列表

### 窗口位置

- **Key：** `winLocation`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`, `MultiTab_OpenUrl`, `MultiColumn_OpenUrl`
- **默认值：** `CenterScreen`

| 值 | 名称 |
|----|------|
| `WithMouse1` | 跟随鼠标（指针周围） |
| `WithMouse2` | 跟随鼠标（指针右下） |
| `CenterScreen` | 屏幕中间 |
| `TopLeft` | 屏幕左上 |
| `TopCenter` | 屏幕中上 |
| `TopRight` | 屏幕右上 |
| `LeftCenter` | 屏幕左中 |
| `RightCenter` | 屏幕右中 |
| `BottomLeft` | 屏幕左下 |
| `BottomCenter` | 屏幕中下 |
| `BottomRight` | 屏幕右下 |
| `FullScreen` | 全屏 |
| `Maximized` | 最大化 |
| `Manual` | 自定义位置 |

### 窗口尺寸/位置

- **Key：** `winSize`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`, `MultiTab_OpenUrl`, `MultiColumn_OpenUrl`
- **说明：**
  - 默认格式：`宽度,高度`（支持像素数值或屏幕百分比如 `400,700` 或 `50%,50%`）
  - `winLocation` 为 `Manual` 时：格式为 `left,top,right,bottom`

### 默认下载文件夹

- **Key：** `defaultDownloadFolderPath`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`, `MultiTab_OpenUrl`, `MultiColumn_OpenUrl`
- **高级参数**
- **说明：** 默认的文件下载存储目录

### Profile

- **Key：** `profileName`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **高级参数**
- **说明：** 当需要同时登录一个网站的多个账号时，可以创建独立的 Profile

### 置顶显示

- **Key：** `topMost`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`, `MultiTab_OpenUrl`, `MultiColumn_OpenUrl`
- **类型：** 布尔（`true` / `false`）
- **高级参数**

### 显示任务栏图标

- **Key：** `showInTaskbar`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **类型：** 布尔
- **默认值：** `true`
- **高级参数**

### 不占用焦点

- **Key：** `noActivate`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **类型：** 布尔
- **高级参数**
- **说明：** 不占用焦点时也无法在窗口中输入文字

### 失去焦点后

- **Key：** `closeWhenLostFocus`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **高级参数**

| 值 | 说明 |
|----|------|
| `false` | 不执行操作 |
| `true` | 关闭窗口 |
| `hide` | 隐藏窗口 |
| `minimize` | 最小化窗口 |
| `close_if_not_topmost` | 如果未置顶，关闭窗口 |
| `hide_if_not_topmost` | 如果未置顶，隐藏窗口 |
| `minimize_if_not_topmost` | 如果未置顶，最小化窗口 |

### 按Esc关闭窗口

- **Key：** `escCloseWindow`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **类型：** 布尔
- **高级参数**

### 显示工具栏

- **Key：** `showToolbar`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **类型：** 布尔
- **高级参数**
- **说明：** 前进/后退/刷新/地址栏

### 窗口风格

- **Key：** `windowStyle`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **高级参数**

| 值 | 说明 |
|----|------|
| `normal` | 正常窗口 |
| `none` | 无边框 |

### 关闭窗口时清理Cookie

- **Key：** `clearCookies`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **类型：** 布尔（`"0"` / `"1"`）
- **高级参数**
- **说明：** 关闭窗口时清除当前页面的 Cookies（适合自动登出场景）

### 添加DevTools桥

- **Key：** `addDevTool`
- **适用操作：** `OpenUrl`, `OpenAndWaitLoad`, `OpenUrlAndWaitClose`
- **类型：** 布尔（`"0"` / `"1"`）
- **高级参数**

### 失败后停止

- **Key：** `stopIfFail`
- **适用操作：** 所有操作
- **类型：** 布尔（`"0"` / `"1"`）
- **默认值：** `true`
- **说明：** 失败后是否停止动作

---

## OutputParams

| Key | 名称 | 类型 | 适用操作 | 说明 |
|-----|------|------|----------|------|
| `isSuccess` | 是否成功 | bool | 所有 | 操作是否成功。获取窗口信息时，表示窗口是否存在 |
| `isInstalled` | 是否安装WebView2 | bool | `CheckInstalled` | WebView2 运行时是否已安装 |
| `hWnd` | 窗口句柄 | IntPtr | `OpenUrl`, `OpenAndWaitLoad`, `CheckWindowState` | 窗口句柄，可用于 Win32 API 操作 |
| `webView` | WebView2对象 | object | `OpenUrl`, `OpenAndWaitLoad`, `CheckWindowState` | 可在 C# 脚本中使用，需运行在 UI 线程中。注意避免循环引用 |
| `lastLocation` | 窗口位置 | string | `OpenAndWaitLoad`, `CheckWindowState`, `OpenUrlAndWaitClose` | 窗口坐标范围，格式：`left,top,right,bottom` |
| `currUri` | 当前网址 | string | `OpenAndWaitLoad`, `CheckWindowState` | 浏览器当前网址 |
| `docTitle` | 网页标题 | string | `OpenAndWaitLoad`, `CheckWindowState` | 当前页面标题 |
| `sourceCode` | 网页代码 | string | `OpenAndWaitLoad`, `CheckWindowState` | 当前页面源代码 |
| `cookies` | Cookie | string | `OpenAndWaitLoad`, `CheckWindowState` | 当前页面 Cookie |
| `previewImage` | 预览图 | byte[] | `CheckWindowState` | 窗口截图 |
| `isNavCompleted` | 导航是否已结束 | bool | `CheckWindowState` | 是否已完成网页加载过程 |
| `scriptResult` | 脚本运行结果 | string | `ExecuteScript` | JSON 编码的脚本运行结果内容 |

---

## 步骤 JSON 示例

### 打开网页（最基本的用法）

```json
{
  "StepRunnerKey": "sys:webview2",
  "InputParams": {
    "type": {"VarKey": null, "Value": "OpenUrl"},
    "url": {"VarKey": null, "Value": "https://www.bilibili.com/"},
    "additionalBrowserArguments": {"VarKey": null, "Value": ""},
    "virtualHostToFolder": {"VarKey": null, "Value": ""},
    "userAgent": {"VarKey": null, "Value": ""},
    "title": {"VarKey": null, "Value": ""},
    "icon": {"VarKey": null, "Value": ""},
    "defaultBgColor": {"VarKey": null, "Value": ""},
    "autoCloseKey": {"VarKey": null, "Value": "="},
    "modeForExists": {"VarKey": null, "Value": "SkipThisStep"},
    "script": {"VarKey": null, "Value": ""},
    "winLocation": {"VarKey": null, "Value": "CenterScreen"},
    "winSize": {"VarKey": null, "Value": ""},
    "stopIfFail": {"VarKey": null, "Value": "1"},
    "defaultDownloadFolderPath": {"VarKey": null, "Value": ""},
    "profileName": {"VarKey": null, "Value": ""},
    "topMost": {"VarKey": null, "Value": "false"},
    "showInTaskbar": {"VarKey": null, "Value": "true"},
    "noActivate": {"VarKey": null, "Value": "false"},
    "closeWhenLostFocus": {"VarKey": null, "Value": "false"},
    "escCloseWindow": {"VarKey": null, "Value": "false"},
    "showToolbar": {"VarKey": null, "Value": "false"},
    "windowStyle": {"VarKey": null, "Value": "normal"},
    "clearCookies": {"VarKey": null, "Value": "0"},
    "addDevTool": {"VarKey": null, "Value": "0"}
  },
  "OutputParams": {
    "isSuccess": null,
    "hWnd": null,
    "webView": null,
    "errMessage": null
  },
  "IfSteps": null, "ElseSteps": null,
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

### 打开网页并等待关闭

```json
{
  "StepRunnerKey": "sys:webview2",
  "InputParams": {
    "type": {"VarKey": null, "Value": "OpenUrlAndWaitClose"},
    "url": {"VarKey": null, "Value": "https://example.com"},
    "autoCloseKey": {"VarKey": null, "Value": "="},
    "title": {"VarKey": null, "Value": "示例页面"},
    "winLocation": {"VarKey": null, "Value": "CenterScreen"},
    "winSize": {"VarKey": null, "Value": "800,600"},
    "showToolbar": {"VarKey": null, "Value": "true"},
    "stopIfFail": {"VarKey": null, "Value": "1"}
  },
  "OutputParams": {
    "isSuccess": null,
    "lastLocation": "windowPos",
    "errMessage": null
  }
}
```

### 打开并等待加载（获取页面信息）

```json
{
  "StepRunnerKey": "sys:webview2",
  "InputParams": {
    "type": {"VarKey": null, "Value": "OpenAndWaitLoad"},
    "url": {"VarKey": null, "Value": "https://example.com"},
    "autoCloseKey": {"VarKey": null, "Value": "="},
    "stopIfFail": {"VarKey": null, "Value": "1"}
  },
  "OutputParams": {
    "isSuccess": null,
    "hWnd": null,
    "webView": null,
    "lastLocation": null,
    "currUri": "currentUrl",
    "docTitle": "pageTitle",
    "sourceCode": "pageSource",
    "cookies": "pageCookies",
    "errMessage": null
  }
}
```

### 执行 JavaScript

```json
{
  "StepRunnerKey": "sys:webview2",
  "InputParams": {
    "type": {"VarKey": null, "Value": "ExecuteScript"},
    "autoCloseKey": {"VarKey": null, "Value": "="},
    "script": {"VarKey": null, "Value": "document.title"}
  },
  "OutputParams": {
    "isSuccess": null,
    "scriptResult": "jsResult",
    "errMessage": null
  }
}
```

### 发送消息到网页

```json
{
  "StepRunnerKey": "sys:webview2",
  "InputParams": {
    "type": {"VarKey": null, "Value": "SendMessage"},
    "autoCloseKey": {"VarKey": null, "Value": "="},
    "sendMessage": {"VarKey": null, "Value": "$={jsonToSend}"}
  },
  "OutputParams": {
    "isSuccess": null,
    "errMessage": null
  }
}
```

### 获取窗口状态

```json
{
  "StepRunnerKey": "sys:webview2",
  "InputParams": {
    "type": {"VarKey": null, "Value": "CheckWindowState"},
    "autoCloseKey": {"VarKey": null, "Value": "="}
  },
  "OutputParams": {
    "isSuccess": "windowExists",
    "hWnd": null,
    "webView": null,
    "lastLocation": null,
    "currUri": "currentUrl",
    "docTitle": "pageTitle",
    "sourceCode": null,
    "cookies": null,
    "previewImage": null,
    "isNavCompleted": "loaded",
    "errMessage": null
  }
}
```

### 检查 WebView2 是否安装

```json
{
  "StepRunnerKey": "sys:webview2",
  "InputParams": {
    "type": {"VarKey": null, "Value": "CheckInstalled"},
    "stopIfFail": {"VarKey": null, "Value": "0"}
  },
  "OutputParams": {
    "isSuccess": null,
    "isInstalled": "wv2Installed",
    "errMessage": null
  }
}
```

### 多标签页打开

```json
{
  "StepRunnerKey": "sys:webview2",
  "InputParams": {
    "type": {"VarKey": null, "Value": "MultiTab_OpenUrl"},
    "urlList": {"VarKey": null, "Value": "首页|https://example.com\n搜索|https://google.com"},
    "title": {"VarKey": null, "Value": "多标签浏览器"},
    "autoCloseKey": {"VarKey": null, "Value": "="},
    "winLocation": {"VarKey": null, "Value": "CenterScreen"},
    "winSize": {"VarKey": null, "Value": "1024,768"},
    "stopIfFail": {"VarKey": null, "Value": "1"}
  },
  "OutputParams": {
    "isSuccess": null,
    "errMessage": null
  }
}
```

---

## JavaScript 交互（Bridge 对象）

WebView2 步骤模块通过 Bridge 对象让网页中的 JS 与 Quicker 动作交互（读写变量、调用子程序等）。

### 访问方式

| 访问方法 | 风格 | 说明 |
|----------|------|------|
| `window.chrome.webview.hostObjects.v` | 异步 | 原生异步访问 |
| `window.chrome.webview.hostObjects.sync.v` | 同步 | 原生同步访问 |
| `$quicker` | 异步 | v1.23.5+ 简写 |
| `$quickerSync` | 同步 | v1.23.5+ 简写 |

### 读写动作变量

**异步方式：**
```javascript
async function readWriteVar() {
    let v = await $quicker;
    let varValue = await v.getVar("变量名");      // 读取
    await v.setVar("变量名", newValue);            // 写入
}
```

**同步方式：**
```javascript
function readWriteVarSync() {
    let varValue = $quickerSync.getVar("text");    // 读取
    $quickerSync.setVar("text", "Hello from JS");  // 写入
}
```

支持简单变量（数字、文本）和列表变量。词典变量读取时自动转为 JSON 文本。**词典变量不能通过 `setVar` 写入。**

### 词典变量操作

JS 不能直接操作词典变量，需用以下辅助方法：

```javascript
// 设置整个词典（从 JSON）
$quickerSync.setDictByJson("dict", '{"a": 1, "b": 2}');

// 设置单个键值
$quickerSync.setDictItemValue("dict", "c", 3);

// 获取单个键的值
var value = $quickerSync.getDictItemValue("dict", "c");
```

### 调用子程序（v1.23.15+）

**必须用 `$quickerSp` 异步方式（已验证可用）：**
```javascript
async function callSubprogram() {
    var input = { inputParam1: "Hello", inputParam2: 3 };
    var result = await $quickerSp("子程序名", input);
    alert("输出: " + result.output);
}
```

- `spName`：子程序名称（对应子程序定义中的 `Name` 字段）
- `dataObj`：输入参数对象（键名对应子程序输入变量的 `ParamName`）
- 输入和输出均为**对象类型**
- 调用处必须用 `async function` + `await`

> **⚠️ `$quickerSync.subprogram` 在 WebView2 中不工作！**
> 同步方式的 `$quickerSync.subprogram("name", params)` 在 WebView2 直接加载 HTML 时调用无效（静默失败，不返回结果也不报错）。必须使用 `$quickerSp` 异步方式。

**旧方式（不推荐，WebView2 中不工作）：**
```javascript
// ❌ 在 WebView2 中静默失败，不要使用
$quickerSync.subprogram("子程序名", {input: "value"});

// ❌ 旧回调方式，同样不推荐
await $quicker.subprogram(
    "子程序名",
    JSON.stringify(inputParam),
    false,
    (success, data) => { }
);
```

### 网页端监听消息

当 Quicker 发送消息时，网页需预先注入监听代码：

```javascript
window.chrome.webview.addEventListener('message', event => {
    console.log('收到消息:', event.data);
    // 处理 event.data
});
```

---

## webView 对象（C# 中使用）

`OutputParams` 中的 `webView` 是 WebView2 控件对象（Type 98），可在后续 C# 脚本步骤中直接使用：

```csharp
// 获取 webView 对象（需运行在 UI 线程中）
var wv = context.GetVarValue("webViewVar") as Microsoft.Web.WebView2.Wpf.WebView2;

// 执行 JS
string result = await wv.CoreWebView2.ExecuteScriptAsync("document.title");

// 导航
wv.CoreWebView2.Navigate("https://new-url.com");
```

**注意：** 避免循环引用（webView 引用了动作变量，变量又引用 webView），否则可能导致内存泄漏。

---

## 注意事项

1. **变量重命名**：在 Quicker 动作编辑器中重命名变量时，JS 脚本中使用的变量名可能**不会**自动更新
2. **额外浏览器参数**：`additionalBrowserArguments` 可能导致无法同时开启多个 WebView2 窗口
3. **file:/// 路径**：含空格的 `file:///` 路径可能不被支持
4. **多标签页限制**：多标签页窗口目前无法对单个标签页执行 JS
5. **iframe 限制**：`ExecuteScriptAsync` 仅在顶层文档执行，不对 iframe 内部执行
6. **同步调用死锁**：复杂操作使用同步 JS 调用可能导致 UI 死锁，优先使用异步方式
7. **不占用焦点**：`noActivate` 为 `true` 时无法在窗口中输入文字
8. **WebView2 对象线程**：`webView` 输出的对象需在 UI 线程中使用
9. **直接加载 HTML 时 Web API 受限**：`url` 参数直接传入 HTML 内容时，页面 origin 为 `null`，以下 API 不可用：
   - `localStorage` / `sessionStorage` — 读写会抛出 `SecurityError`
   - `indexedDB` — 同样受 origin 限制
   - `fetch` / `XMLHttpRequest` — 无法发起跨域请求（同源策略下 origin 为 null 会被拒绝）
   - Cookie 相关操作
   - **替代方案**：用 JS 变量（内存）存储数据，或用 `$quickerSync.setVar` / `$quickerSync.getVar` 通过 Quicker 动作变量存取数据（不受 origin 限制）
10. **直接加载 HTML 时 JS 语法建议**：`url` 参数传 HTML 内容时，脚本在特殊环境中执行，建议：
    - 用 `try/catch` 包裹主逻辑，出错时能显示错误信息而非白屏
    - 优先用 `for` 循环而非 `forEach`/`find` 等 ES6 数组方法（兼容性更好）
    - 用 `document.onkeydown` 替代 `addEventListener`（更不容易出问题）
    - 简单 `onclick="..."` 内联事件通常比 `addEventListener` 更可靠
