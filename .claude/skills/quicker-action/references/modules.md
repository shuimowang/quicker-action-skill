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

InputParams：`format`（`"UnicodeText"` 等）、`waitMs`、`trim`、`stopIfFail`。OutputParams：`isSuccess`、`output`。

---

## 翻译 (`sys:translation`)

InputParams：`operation`（`"single"`）、`text`、`srcLang`/`dstLang`（`"Auto"` 等）、`vendor`（`"Baidu"` 等）。OutputParams：`resultText`。

---

## 显示文本 (`sys:showText`)

InputParams：

| 参数 | 说明 |
|------|------|
| `type` | `"NO_WAIT"` 不等待关闭 |
| `text` | 显示的文本内容 |
| `title` | 窗口标题 |
| `fontsize` | 字体大小 |
| `fontfamily` | 字体 |
| `enableEscClose` | ESC 关闭，`"true"` / `"false"` |
| `autoWrap` | 自动换行，`"true"` / `"false"` |
| `topMost` | 置顶，`"true"` / `"false"` |
| `bgColor` | 背景颜色 |
| `textColor` | 文字颜色 |
| `highlight` | 高亮 |
| `showLineNum` | 显示行号，`"true"` / `"false"` |
| `showBuildInToolbar` | 显示内置工具栏，`"true"` / `"false"` |
| `copyWholeLine` | 点击复制整行，`"true"` / `"false"` |
| `autoCloseKey` | 自动关闭快捷键 |
| `closeWhenLostFocus` | 失去焦点关闭，`"true"` / `"false"` |
| `caretPosition` | 光标位置 |
| `winLocation` | 窗口位置 |
| `winSize` | 窗口尺寸 |
| `operations` | 操作 |
| `autoSaveToState` | 自动保存到状态 |
| `updateIfExists` | 已存在时更新，`"0"` / `"1"` |
| `stopIfFail` | 失败停止，`"0"` / `"1"` |
| `advancedSettings` | 高级设置 |

OutputParams：`isSuccess`、`windowHandle`、`errMessage`。

---

## 提示消息 (`sys:notify`)

InputParams：`type`（`"Info"` / `"Success"` / `"Warning"` / `"Error"`）、`msg`、`maxLines`（最大行数，0 不限）、`style`（`"Default"` 屏幕中下 / `"Style2"` 屏幕右上）、`clickAction`（点击执行的动作，仅 Default 风格）。

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

## 条件判断 (`sys:simpleIf`)

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

---

## 步骤组 (`sys:group`)

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

---

## WebView2 浏览器窗口 (`sys:webview2`)

独立的浏览器窗口模块，支持打开网址、执行 JS、发送消息、多标签页等。详细参数和用法见 [webview2.md](webview2.md)。

---

## 停止 (`sys:stop`)

```json
{
  "StepRunnerKey": "sys:stop",
  "InputParams": {
    "method": {"VarKey": null, "Value": "default"},
    "isError": {"VarKey": null, "Value": "0"},
    "return": {"VarKey": null, "Value": ""},
    "showMessage": {"VarKey": null, "Value": ""}
  },
  "OutputParams": {},
  "IfSteps": [], "ElseSteps": [],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

| 参数 | 说明 |
|------|------|
| `method` | `"default"` 停止当前动作/从子程序返回（子程序中不停止主动作），`"forcestop"` 强制停止整个动作（即使在子程序中） |
| `isError` | `"0"` 正常停止，`"1"` 错误停止 |
| `return` | 返回值（子程序场景） |
| `showMessage` | 停止时显示的消息 |

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
