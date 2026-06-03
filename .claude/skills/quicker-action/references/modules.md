# Quicker 模块定义

## 赋值 (`sys:assign`)

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

---

## C# 脚本 (`sys:csscript`)

### 运行模式（`mode`）

| 值 | 名称 | 说明 |
|----|------|------|
| `normal` | 普通模式v1 (CodeDOM) | C# 5.0，在 Quicker 进程内执行 |
| `normal_roslyn` | 普通模式v2 (Roslyn) | C# 7.3，在 Quicker 进程内执行，可用内部程序集 |
| `low_permission` | 低权限模式v1 (CodeDOM) | 在 LPAgent 代理进程执行 |
| `low_permission_roslyn` | 低权限模式v2 (Roslyn) | 在 LPAgent 代理进程执行 |
| `generate_assembly` | 生成程序集 | 生成 DLL 程序集对象 |

### Exec 签名

**普通模式 / generate_assembly：**
```csharp
public static string Exec(Quicker.Public.IStepContext context)
{
    var value = context.GetVarValue("varName");
    context.SetVarValue("varName", "output");
    return "返回值";  // OutputParams 的 rtn 接收
}
```

**低权限模式：** 不能访问动作变量，仅支持简单文本传递。
```csharp
public static string Exec(string paramValue)
{
    return "结果";
}
```

### InputParams

| 参数 | Key | 适用模式 | 说明 |
|------|-----|----------|------|
| 运行模式 | `mode` | 全部 | 见上表 |
| 脚本内容 | `script` | `normal`, `normal_roslyn` | C# 代码字符串 |
| 脚本内容(低权限) | `scriptForLp` | `low_permission`, `low_permission_roslyn` | 低权限模式的 C# 代码 |
| 脚本内容(程序集) | `scriptForAssembly` | `generate_assembly` | 需包含 namespace + class |
| 引用DLL库 | `reference` | 全部 | 路径，每行一个 |
| 参数值 | `paramValue` | `low_permission`, `low_permission_roslyn` | 传递给 Exec 的参数 |
| 等待返回 | `waitResp` | `low_permission`, `low_permission_roslyn` | 是否等待脚本返回 |
| 最长等待时间(ms) | `waitMs` | `low_permission`, `low_permission_roslyn` | 默认 10000 |
| 执行线程 | `runOnUiThread` | `normal`, `normal_roslyn` | `"auto"` / `"ui"` / `"background"` / `"sta"` / `"staLongRun"` |
| 允许缓存程序集 | `enableCache` | `normal`, `low_permission` | `"0"` / `"1"` |
| 失败后停止 | `stopIfFail` | 全部 | `"0"` / `"1"` |

### OutputParams

| 参数 | Key | 适用模式 | 说明 |
|------|-----|----------|------|
| 是否成功 | `isSuccess` | 全部 | 操作是否成功 |
| 返回内容 | `rtn` | `normal`, `normal_roslyn` | Exec 方法的返回值 |
| 返回内容 | `resp` | `low_permission`, `low_permission_roslyn` | 脚本执行返回的结果文本 |
| 程序集对象 | `rtnAssembly` | `generate_assembly` | 生成的 Assembly 对象 |
| 程序集路径 | `assemblyPath` | `generate_assembly` | 生成的 DLL 路径 |

详细用法见 [C# 规则](csharp-rules.md)。

---

## Python 脚本 (`sys:pythonscript`)

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

## 多字段表单 (`sys:form`)

### 工作模式（`operation`，控制字段）

| 值 | 名称 | 表单定义参数 |
|----|------|-------------|
| `variables` | 编辑动作变量的值（默认） | `formDef` (Type 11) |
| `dict` | 编辑词典数据 | `formForDictDef` (Type 14) + `dictVar` |
| `dict_dynamic` | 编辑词典数据（动态） | `dynamicFormForDictDef` (JSON字符串) + `dictVar` |

### InputParams

| 参数 | Key | 适用模式 | 类型 | 说明 |
|------|-----|----------|------|------|
| 工作模式 | `operation` | — | 下拉 | `variables` / `dict` / `dict_dynamic` |
| 词典变量 | `dictVar` | dict, dict_dynamic | 词典(10) | 要编辑的词典变量（VarKey 引用） |
| 表单定义 | `formDef` | variables | 11 | 变量模式的表单定义 |
| 表单定义(词典) | `formForDictDef` | dict | 14 | 词典模式的表单定义 |
| 表单定义(动态) | `dynamicFormForDictDef` | dict_dynamic | 文本 | JSON 格式表单定义 |
| 窗口标题 | `title` | 全部 | 文本 | 默认"填写表单" |
| 提示文字 | `help` | 全部 | 多行文本 | 帮助用户填写的提示 |
| 帮助按钮内容 | `markdownhelp` | 全部 | 多行文本 | 点击弹出帮助，Markdown 格式（高级） |
| 标题列宽度 | `titleColumnWidth` | 全部 | 数字 | 默认 100。负值如 -200 表示自适应且最大 200 |
| 窗口宽度 | `windowWidth` | 全部 | 数字 | 默认 500，最小 400 |
| 窗口最大高度 | `windowHeight` | 全部 | 数字 | 0=默认，需 >100 |
| 输入框默认宽度 | `defaultInputWidth` | 全部 | 数字 | 0=自动宽度（高级） |
| 恢复活动窗口 | `restoreFocus` | 全部 | 布尔 | 关闭后是否恢复之前的焦点窗口 |
| 置顶显示 | `topMost` | 全部 | 布尔 | |
| 关闭Enter提交 | `disableEnterSubmit` | 全部 | 布尔 | 禁用 Enter 键提交表单 |
| 自定义确定按钮 | `confirm` | 全部 | 文本 | 如 `"保存(_S)"`，Alt+S 触发（高级） |
| 自定义按钮 | `customButtons` | 全部 | 多行文本 | 格式 `"标题\|返回值"`，多个换行（高级） |
| 默认选择分组 | `selectedGroup` | 全部 | 文本 | 分组标签页的默认选中项（高级） |
| 窗口位置 | `winLocation` | 全部 | 下拉 | 同 webview2 的 winLocation 选项（高级） |
| 自定义位置 | `winSize` | 全部 | 文本 | `winLocation=Manual` 时：`left,top,right,bottom`（高级） |
| 取消后停止 | `stopIfFail` | 全部 | 布尔 | 默认 true |

### OutputParams

| 参数 | Key | 说明 |
|------|-----|------|
| 是否成功 | `isSuccess` | 操作是否成功 |
| 点击的按钮 | `button` | 默认确定按钮返回空，自定义按钮返回自定义值 |
| 选择的分组 | `selectedGroup` | 关闭时所选的标签页分组 |

详细用法和 FormField 定义见 [form.md](form.md)。

---

## 获取选中文本 (`sys:getSelectedText`)

### InputParams

| 参数 | Key | 类型 | 说明 |
|------|-----|------|------|
| 文本数据格式 | `format` | 下拉 | `UnicodeText`（默认） / `Rtf` / `Html` / `CommaSeparatedValue`(csv) |
| 等待剪贴板时间 | `waitMs` | 整数 | 模拟复制后等待剪贴板变化的最长时间(ms)，默认 250 |
| 去除前后空白 | `trim` | 布尔 | 去除内容前后的空白和空行 |
| 不通过剪贴板获取 | `tryNoClipboard` | 布尔 | 通过 UIAutomation 获取（可能丢失换行信息） |
| 使用动作参数 | `useActionParam` | 布尔 | 如果传递了动作参数，直接使用参数值作为结果 |
| 失败后中止 | `stopIfFail` | 布尔 | |

### OutputParams

| 参数 | Key | 适用格式 | 说明 |
|------|-----|----------|------|
| 是否成功 | `isSuccess` | 全部 | |
| 内容 | `output` | 全部 | 获取的文本 |
| 去除封装的HTML | `cleanHtml` | Html | `<!--StartFragment-->` 和 `<!--EndFragment-->` 之间的部分 |
| URL编码的内容 | `outputEncoded` | 全部 | URL 编码后的结果，用于拼接网址 |
| 来源网址 | `url` | 全部 | 从网页复制时可能携带的网址信息 |

---

## 翻译 (`sys:translation`)

InputParams：`operation`（`"single"`）、`text`、`srcLang`/`dstLang`（`"Auto"` 等）、`vendor`（`"Baidu"` 等）。OutputParams：`resultText`。

---

## 显示文本 (`sys:showText`)

### 操作类型（`type`，控制字段）

| 值 | 名称 |
|----|------|
| `NO_WAIT` | 显示窗口，不等待关闭（默认） |
| `WAIT` | 显示窗口，等待关闭 |
| `CLOSE_WINDOW` | 关闭窗口 |
| `GET_WIN_INFO` | 获取窗口信息 |
| `APPEND_TEXT` | 追加内容 |
| `ACTIVATE_WINDOW` | 显示和激活窗口 |
| `WAIT_CLOSE` | 等待窗口关闭 |
| `GET_ALL_WINDOWS` | 获取所有文本窗口 |
| `GET_ACTION_WINDOWS` | 获取当前动作创建的所有文本窗口 |

### InputParams

| 参数 | Key | 适用类型 | 类型 | 说明 |
|------|-----|----------|------|------|
| 文本内容 | `text` | WAIT, NO_WAIT, APPEND_TEXT | 多行文本 | 要显示的文本 |
| 窗口标题 | `title` | WAIT, NO_WAIT | 文本 | 默认"文本窗口" |
| 文本窗口标识 | `autoCloseKey` | 除 GET_ALL/ACTION_WINDOWS | 文本 | `=` 表示当前动作 ID |
| 工具栏操作 | `operations` | WAIT, NO_WAIT | 多行文本 | 每行一个 `"显示文本\|值"`（高级） |
| 窗口位置 | `winLocation` | WAIT, NO_WAIT | 下拉 | 同 customwindow（高级） |
| 窗口尺寸/位置 | `winSize` | WAIT, NO_WAIT | 文本 | `宽,高` 或 `left,top,right,bottom`（高级） |
| 字体大小 | `fontsize` | WAIT, NO_WAIT | 数字 | 默认 14（高级） |
| 字体名称 | `fontfamily` | WAIT, NO_WAIT | 文本 | 多字体逗号分隔（高级） |
| 背景颜色 | `bgColor` | WAIT, NO_WAIT | 文本 | `#RRGGBB`（高级） |
| 文字颜色 | `textColor` | WAIT, NO_WAIT | 文本 | `#RRGGBB`（高级） |
| 语法高亮 | `highlight` | WAIT, NO_WAIT | 下拉 | 见下表（高级） |
| 自动保存到状态 | `autoSaveToState` | WAIT, NO_WAIT | 文本 | 状态 Key（高级） |
| 置顶显示 | `topMost` | WAIT, NO_WAIT | 布尔 | |
| Esc 键关闭窗口 | `enableEscClose` | WAIT, NO_WAIT | 布尔 | 默认 true（高级） |
| 失去焦点自动关闭 | `closeWhenLostFocus` | WAIT, NO_WAIT | 布尔 | （高级） |
| 显示行号 | `showLineNum` | WAIT, NO_WAIT | 布尔 | 默认 true（高级） |
| 自动换行显示 | `autoWrap` | WAIT, NO_WAIT | 布尔 | 默认 true（高级） |
| 显示内置工具栏 | `showBuildInToolbar` | WAIT, NO_WAIT | 布尔 | 默认 true（高级） |
| 未选中时复制整行 | `copyWholeLine` | WAIT, NO_WAIT | 布尔 | （高级） |
| 光标位置 | `caretPosition` | WAIT, NO_WAIT | 整数 | 0=最前，-1=最后（高级） |
| 高级设置 | `advancedSettings` | 全部 | 多行文本 | 参考模块文档（高级） |
| 存在时更新内容 | `updateIfExists` | NO_WAIT | 布尔 | 不关旧窗口直接更新（高级） |
| 失败后停止 | `stopIfFail` | 全部 | 布尔 | |

### highlight 语法高亮选项（常用）

`C#`、`C++`、`CSS`、`HTML`、`Java`、`JavaScript`、`Json`、`MarkDown`、`PHP`、`PowerShell`、`Python`、`Ruby`、`XML`、`TXT`（无）等 30+ 种。

### OutputParams

| 参数 | Key | 适用类型 | 说明 |
|------|-----|----------|------|
| 是否成功 | `isSuccess` | 全部 | |
| 窗口是否存在 | `isWindowExists` | GET_WIN_INFO | |
| 选择的项 | `selectedOperation` | WAIT | 用户选择的工具栏操作 |
| 结果文本 | `resultText` | WAIT, CLOSE_WINDOW, GET_WIN_INFO | 文本框内全部文本 |
| 选中的文本 | `selectedText` | WAIT, CLOSE_WINDOW, GET_WIN_INFO | |
| 光标位置 | `caretPosition` | WAIT, CLOSE_WINDOW, GET_WIN_INFO | 字符序号 |
| 窗口句柄 | `windowHandle` | NO_WAIT, GET_WIN_INFO | |
| 窗口位置 | `windowPosition` | WAIT, CLOSE_WINDOW, GET_WIN_INFO | 最终显示位置 |
| 所有窗口 | `allWindows` | GET_ALL_WINDOWS, GET_ACTION_WINDOWS | 词典(10)，key=句柄, value=标识 |

---

## 提示消息 (`sys:notify`)

### InputParams

| 参数 | Key | 类型 | 说明 |
|------|-----|------|------|
| 类型 | `type` | 下拉 | `Info` / `Success` / `Warning` / `Error` / `WindowsToast` |
| 消息内容 | `msg` | 多行文本 | |
| 最大行数 | `maxLines` | 整数 | 0=不限 |
| 风格 | `style` | 下拉 | `Default`（屏幕底部） / `Style2`（屏幕右侧） |
| 点击命令 | `clickAction` | 多行文本 | 仅 Default 风格，支持 Win+R 可执行的命令（网址等），默认复制文字 |

**无 OutputParams。**

---

## 调用子程序 (`sys:subprogram`)

### InputParams

| 参数 | Key | 类型 | 说明 |
|------|-----|------|------|
| 子程序 | `subProgram` | 文本 | 子程序名称或 `@@ID@版本@名称` 格式 |
| 失败后停止 | `stopIfFail` | 布尔 | 默认 true |
| 跳过调试输出 | `skipDebugOutput` | 布尔 | 调试时不输出子程序内部信息（高级） |

**传入参数：** 额外添加 `var:参数名` 键，值为要传入的内容：
```json
"InputParams": {
  "subProgram": {"VarKey": null, "Value": "子程序名"},
  "var:input1": {"VarKey": null, "Value": "值1"},
  "var:input2": {"VarKey": "myVar", "Value": null},
  "stopIfFail": {"VarKey": null, "Value": "1"}
}
```

### OutputParams

| 参数 | Key | 说明 |
|------|-----|------|
| 是否成功 | `isSuccess` | 子程序是否运行成功 |

**接收输出：** 额外添加 `var:输出名` 键，值为目标变量名：
```json
"OutputParams": {
  "isSuccess": "success",
  "var:result": "myResult"
}
```

---

## 条件判断 (`sys:if`)

If/Else 容器步骤，始终包含 IfSteps 和 ElseSteps 两个分支。

### InputParams

| 参数 | Key | 类型 | 说明 |
|------|-----|------|------|
| 如果 | `condition` | 布尔(多行) | 条件表达式，支持 `$=` 前缀 |

**无 OutputParams。**

---

## 条件判断 (`sys:simpleIf`)

简化版 If，ElseSteps 可省略（设为 `null`）。

### InputParams

| 参数 | Key | 类型 | 说明 |
|------|-----|------|------|
| 如果 | `condition` | 布尔(多行) | 条件表达式，支持 `$=` 前缀 |

**无 OutputParams。** 容器步骤，包含 `IfSteps` 和 `ElseSteps`。

```json
{
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": {
    "condition": {"VarKey": null, "Value": "$={varName}==\"value\""}
  },
  "OutputParams": {},
  "IfSteps": [ /* 条件为真时执行 */ ],
  "ElseSteps": [ /* 条件为假时执行（可选） */ ],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

---

## 步骤组 (`sys:group`)

容器步骤，将多个步骤分组执行。

### InputParams

| 参数 | Key | 类型 | 说明 |
|------|-----|------|------|
| 忽略错误 | `skipErr` | 布尔 | 忽略内部步骤的错误，继续执行后续步骤 |
| 调试时不输出 | `skipWhenDebugging` | 布尔 | 减少不必要的调试输出 |
| 使用多线程 | `useMultiThread` | 布尔 | ⚠️ 请阅读文档后再使用 |
| WaitAny 模式 | `waitAny` | 布尔 | 多线程时任意一个线程结束即可（配合 useMultiThread） |

### OutputParams

| 参数 | Key | 说明 |
|------|-----|------|
| 是否成功 | `isSuccess` | 内部步骤是否运行成功 |
| 错误消息 | `errorMessage` | 错误信息 |

---

## WebView2 浏览器窗口 (`sys:webview2`)

独立的浏览器窗口模块，支持打开网址、执行 JS、发送消息、多标签页等。详细参数和用法见 [webview2.md](webview2.md)。

---

## 自定义窗口 (`sys:customwindow`)

### 操作类型（`type`，控制字段）

| 值 | 名称 | 说明 |
|----|------|------|
| `ShowAndWaitClose` | 显示窗口并等待关闭 | 暂停直到窗口关闭 |
| `Show` | 显示窗口 | 不等待，后续步骤立即执行 |
| `Close` | 关闭窗口 | 通过 windowId 查找并关闭 |
| `GetWindows` | 获取窗口列表 | 检测已打开的窗口 |

### InputParams

| 参数 | Key | 适用类型 | 类型 | 说明 |
|------|-----|----------|------|------|
| 窗口XAML代码 | `windowMarkup` | Show, ShowAndWaitClose | 多行文本(XML) | WPF XAML 定义 |
| 数据映射 | `dataMapping` | Show, ShowAndWaitClose | 多行文本 | `数据名:{变量名}` 或 `数据名:=表达式`，每行一个 |
| 辅助C#代码 | `cscode` | Show, ShowAndWaitClose | 多行文本(C#) | OnWindowCreated/OnWindowLoaded/OnButtonClicked 回调（高级） |
| 事件 | `events` | Show, ShowAndWaitClose | 多行文本 | 事件处理（高级） |
| 窗口标识 | `windowId` | 全部 | 文本 | 用于查找/关闭窗口 |
| 自动关闭时间(S) | `autoCloseTime` | Show, ShowAndWaitClose | 数字 | >0.5秒，0=不自动关闭（高级） |
| 激活模式 | `activateMode` | Show, ShowAndWaitClose | 下拉 | 见下表（高级） |
| 窗口位置 | `winLocation` | Show, ShowAndWaitClose | 下拉 | 见下表（高级） |
| 窗口尺寸/位置 | `winSize` | Show, ShowAndWaitClose | 文本 | `宽,高` 或 `left,top,right,bottom`（高级） |
| 失去焦点后关闭 | `closeWhenDeactivate` | Show, ShowAndWaitClose | 下拉 | `true` / `false` / `closeIfNotTopmost` |
| 失败后停止 | `stopIfFail` | 全部 | 布尔 | |

### activateMode 选项

| 值 | 说明 |
|----|------|
| `NotActivatable` | 不支持激活（不占用焦点，仅鼠标操作） |
| `NotActivatableMouseThrough` | 不支持激活，鼠标穿透 |
| `NotActivated` | 支持激活，打开时不抢占焦点 |
| `AutoActivate` | 支持激活，打开时抢占焦点（默认） |

### winLocation 选项

| 值 | 名称 |
|----|------|
| `WithMouse1` | 跟随鼠标（指针周围） |
| `WithMouse2` | 跟随鼠标（指针右下） |
| `CenterScreen` | 屏幕中间 |
| `TopLeft` / `TopCenter` / `TopRight` | 屏幕上部 |
| `LeftCenter` / `RightCenter` | 屏幕中部两侧 |
| `BottomLeft` / `BottomCenter` / `BottomRight` | 屏幕下部 |
| `FullScreen` | 全屏 |
| `Maximized` | 最大化 |
| `Manual` | 自定义位置（需配合 winSize） |
| `Auto` | 系统默认 |

### OutputParams

| 参数 | Key | 适用类型 | 类型 | 说明 |
|------|-----|----------|------|------|
| 是否成功 | `isSuccess` | 全部 | bool | |
| 窗口结果 | `result` | ShowAndWaitClose, Close | 文本 | 通过 `close:result` 返回 |
| 窗口对象列表 | `windowList` | GetWindows | IList\<Window\> (98) | 已打开的窗口列表 |
| 窗口句柄 | `windowHandle` | Show | IntPtr (12) | |
| 关闭时窗口位置 | `windowLocation` | ShowAndWaitClose | 文本 | |

详细用法见 [customwindow.md](customwindow.md)。

---

## 停止 (`sys:stop`)

### InputParams

| 参数 | Key | 类型 | 说明 |
|------|-----|------|------|
| 操作类型 | `method` | 下拉 | `default`（停止动作/从子程序返回） / `forcestop`（强制停止整个动作） |
| 标记为出错 | `isError` | 布尔 | 用作子程序或被其他动作调用时，返回出错状态 |
| 返回值 | `return` | 多行文本 | 被其他动作调用时，返回的动作结果 |
| 提示消息 | `showMessage` | 多行文本 | 停止时显示的提示信息 |

**无 OutputParams。**

---

## 注释 (`sys:comment`)

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

表达式以 `$=` 开头，**任何步骤 InputParams 的 Value 字段都能用**，不限于赋值步骤。

常见用法：
- `sys:assign` 的 `input` — 计算并赋值
- `sys:simpleIf` 的 `condition` — 条件判断
- `sys:csscript` 的 `script` — 动态生成代码
- 其他步骤参数 — 动态计算任意值

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

### 在 simpleIf 条件中使用多行表达式

```json
{
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": {
    "condition": {
      "VarKey": null,
      "Value": "$=\r\n\r\nint number = new Random().Next(1, 11);\r\n\r\nreturn number % 2 == 0;"
    }
  }
}
```

表达式可以声明变量、调用方法，只要最终 `return` 一个 bool 结果即可。

### 变量引用
使用花括号：`{变量名}`

### 内置对象

**仅在表达式（`$=`）中可直接使用**，C# 脚本步骤用 `Exec` 的 `context` 参数。详细说明见 [C# 规则 - 内置变量](csharp-rules.md#内置变量_context_eval_qk)。

- `_context` — 动作上下文（`ActionExecuteContext`），可调用 `GetVarValue`/`SetVarValue`/`RunSp`/`WriteState`/`ReadCache` 等
- `_eval` — 表达式引擎（`EvalContext`），可注册自定义 DLL（`_eval.RegisterAssembly`）、注册方法、注册变量
- `_qk` — 内置功能封装，不常用

### 已注册类型（常用，可在表达式中直接使用）

**文件/IO：** `File`、`Directory`、`Path`、`FileInfo`、`DirectoryInfo`、`Stream`、`StreamReader`、`StreamWriter`、`FileStream`

**文本处理：** `Regex`、`Match`、`StringBuilder`、`Encoding`、`StringComparer`

**JSON（Newtonsoft）：** `JsonConvert`、`JObject`、`JArray`、`JToken`、`JValue`、`JProperty`

**XML：** `XmlDocument`、`XmlElement`、`XmlNode`、`XmlReader`、`XmlWriter`、`XDocument`、`XElement`、`XAttribute`

**数据：** `DataTable`、`DataSet`、`DataRow`、`DataColumn`、`DataView`

**网络：** `WebClient`、`HttpWebRequest`、`Uri`、`Dns`、`Socket`、`TcpClient`

**进程/线程：** `Process`、`Thread`、`Task`、`Parallel`

**基础类型：** `String`、`Int32`、`Double`、`Boolean`、`DateTime`、`Decimal`、`Math`、`Convert`、`Array`、`Enum`、`Environment`、`Console`

**反射：** `Assembly`、`Type`、`MethodInfo`、`PropertyInfo`、`FieldInfo`

**Linq：** `Enumerable`、`Queryable`、`Expression`

### 环境限制与 C# 语法

详见 [C# 规则](csharp-rules.md)：环境限制、C# 5.0 禁用语法、定义公共方法、Lambda 与委托。
