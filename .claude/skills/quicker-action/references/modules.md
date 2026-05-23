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

**v2 Roslyn（C# 7.3）：** `mode` 改为 `"normal_roslyn"`，同样在 Quicker 进程内执行，可用 `Quicker.Utilities` 等内部程序集。

首次编译冷启动较慢，自动缓存程序集（代码不变可复用缓存）。

**低权限模式：** `mode` 为 `"lowtrust"` / `"lowtrust_roslyn"`，在 LPAgent 代理进程执行，**不能**访问动作变量和 Quicker 内部程序集，仅支持简单文本传递。

Exec 签名不同：`public static string Exec(string paramValue)`

**InputParams：**

| 参数 | 说明 | 值 |
|------|------|-----|
| `mode` | 模式 | `"normal"` v1 / `"normal_roslyn"` v2 / `"lowtrust"` 低权限v1 / `"lowtrust_roslyn"` 低权限v2 |
| `script` | C#代码 | 代码字符串 |
| `reference` | DLL引用 | 路径，每行一个 |
| `runOnUiThread` | 执行线程 | 详见 [C# 规则 - 线程选择](csharp-rules.md#线程选择) |
| `enableCache` | 缓存程序集 | `"0"` / `"1"`，允许缓存编译后的程序集以加快下次启动，版本升级时自动丢弃 |
| `stopIfFail` | 失败停止 | `"0"` / `"1"` |

**OutputParams：** `isSuccess`（是否成功）、`rtn`（返回值）、`errMessage`（错误信息）

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

详细参数和用法见 [form.md](form.md)。

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

InputParams：`subProgram`（子程序名）、`var:参数名`（参数值）、`stopIfFail`。OutputParams：`isSuccess`、`var:输出名`、`errMessage`。

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

表达式和 C# 步骤中可直接使用，详细说明见 [C# 规则 - 内置变量](csharp-rules.md#内置变量_context_eval_qk)。

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

### 环境限制
- .NET Framework 4.7.2
- 普通模式 v1：C# 5.0
- 普通模式 v2（Roslyn）：C# 7.3

**C# 5.0 禁止使用的语法（cscode 和 csscript 均适用）：**
- `$""` 字符串插值 → 用 `string.Format("{0}", arg)`
- `?.` null 条件运算符 → 用 `if (x != null) x.Method()`
- `=>` 表达式体成员（如 `public int X => 1;`）→ 用完整 `{ get { return 1; } }`。注意：**lambda 表达式允许**，如 `Func<int, int> f = x => x + 1;`
- `nameof()` → 用字符串字面量
- `when` 异常过滤器 → 不支持
- `using static` → 不支持
- `is Type var` 模式匹配（C# 7.0）→ 用 `as` + null 检查：`var x = obj as Type; if (x != null) { ... }`

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
