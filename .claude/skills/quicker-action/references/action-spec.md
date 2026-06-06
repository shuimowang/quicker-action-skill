# Quicker 动作编写规范

## 设计原则

### 1. 能在 cscode 里做的就不要拆步骤

CustomWindow 的 cscode 可以在回调中做任何事（读剪贴板、操作图片、弹对话框、写文件等），不需要额外的 csscript 步骤。

**反面教材：**
- Step 0: csscript 获取剪贴板 → 变量 A
- Step 1: CustomWindow 显示变量 A → 输出变量 B/C/D/E
- Step 2: csscript 读变量 A/B/C/D/E → 裁剪保存

**正确做法：**
- Step 0: 多实例检测
- Step 1: CustomWindow（cscode 内部完成获取、显示、裁剪、保存）

步骤间变量传递有成本（类型转换、对齐），能避免就避免。

### 2. 只有多实例检测必须是独立步骤

GetWindows + simpleIf 必须在窗口创建前执行，无法放进 cscode。

### 3. 不要滥用 C# 脚本

能用内置步骤 + 表达式 `$=` 解决的，不写 C#。C# 只用于：
- 剪贴板、图片像素操作
- Win32 API / 外部 DLL
- 复杂对象构建
- 内置步骤无法覆盖的场景

### 4. 代码可读性

JSON 字符串中嵌入的 XAML、C# 代码必须用 `\n` 换行 + 缩进，不能挤成一行。

- **XAML**：每个属性独立一行或合理换行，子元素缩进 4 空格，添加注释分组（如 `<!-- 标题栏 -->`）
- **C# 代码**：保持正常代码格式，语句换行、花括号缩进
- **cscode** 已经用 `\n` 的保持不变；XAML 同样用 `\n` 而非拼成一行

**反面教材：**
```
"Value": "<Window xmlns=\"...\" Width=\"300\" Height=\"360\" WindowStyle=\"None\"><Grid><Grid.RowDefinitions><RowDefinition Height=\"28\"/><RowDefinition Height=\"*\"/></Grid.RowDefinitions>..."
```

**正确做法：**
```
"Value": "<Window xmlns=\"...\"\n        Width=\"300\" Height=\"360\"\n        WindowStyle=\"None\">\n    <Grid>\n        <Grid.RowDefinitions>\n            <RowDefinition Height=\"28\"/>\n            <RowDefinition Height=\"*\"/>\n        </Grid.RowDefinitions>\n..."
```

### 5. 变量最小化

- 不需要在步骤间传递的数据，用 cscode 局部变量（`static` 字段）
- 需要跨步骤传递的才定义为动作变量
- `SaveState: true` 仅用于需要持久化的配置

### 6. OutputParams 输出的变量必须在 Variables 中声明

`OutputParams` 是步骤的**输出变量词典**。key 是步骤模块定义的输出名，value 是你要存入的变量名。

```
"OutputParams": {
  "windowList": "windowList"
  ↑ 模块输出名     ↑ 存入哪个变量
}
```

这表示"把步骤的 `windowList` 输出存到名为 `windowList` 的变量中"。**这个变量必须在 `Variables` 数组中有定义，否则输出无处可存。**

**反面教材：**
```json
"Variables": [],   // ← 没有声明 windowList
"Steps": [{
  "StepRunnerKey": "sys:customwindow",
  "OutputParams": { "windowList": "windowList" }   // 输出到哪？变量不存在！
}, {
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": { "condition": "$={windowList}.Any()" }   // 读取为空！
}]
```

**正确做法：**
```json
"Variables": [
  { "Key": "windowList", "Type": 99, ... }   // 先声明变量
],
"Steps": [{
  "StepRunnerKey": "sys:customwindow",
  "OutputParams": { "windowList": "windowList" }   // 输出到已声明的变量
}, {
  "StepRunnerKey": "sys:simpleIf",
  "InputParams": { "condition": "$={windowList}.Any()" }   // 正常读取
}]
```

**规则：每写一个 OutputParams，就检查对应的变量是否已在 Variables 中声明。**

### 7. 不要臆想不存在的步骤

**StepRunnerKey 必须是 [模块定义](modules.md) 中列出的模块。** 不要凭记忆或想象编造模块名。

**常见臆想：**
- `sys:closeWindow` → 不存在，关闭窗口用 `sys:customwindow`（`type = "Close"`）
- `sys:messageBox` → 不存在，显示文本用 `sys:showText`
- `sys:inputBox` → 不存在，用户输入用 `sys:form`
- `sys:clipboard` → 不存在，读剪贴板在 cscode 中用 `Clipboard.GetText()`

**正确做法：** 用到某个步骤模块前，先查 [模块定义](modules.md) 确认 `StepRunnerKey` 和 `InputParams` 是否存在。不确定的不要用，宁可多查一次文档。

---

## CustomWindow 规范

### 多实例处理（必须）

每个使用 CustomWindow 的动作都必须处理多实例。标准模式：

```
Step 0: sys:customwindow (GetWindows) → windowList
Step 1: sys:simpleIf {windowList}.Any()
  IfSteps:
    - sys:customwindow (Close) 关闭旧窗口
    - sys:stop 退出
Step 2: sys:customwindow (ShowAndWaitClose) 主窗口
```

### windowId

统一用 `$=_context.ActionId`，确保同一动作的窗口共享 ID。

### XAML 规范

- `xmlns:qk="https://getquicker.net"` 仅在使用 qk: 前缀控件（如 `qk:IconControl`）时才需要声明
- 不写 `x:Class`
- 不写 `WindowStartupLocation`（由 `winLocation` 参数控制）
- 事件绑定在 cscode 中处理，不写 XAML 字符串绑定
- 静态命令按钮优先用 `Tag` + `OnButtonClicked` 分发；右键、长按、拖拽、文本变化、动态控件等场景用 `+=` 绑定对应事件
- `Style` 必须用 `StaticResource`

### cscode 规范

- 必须有 `OnWindowCreated`
- C# 5.0 语法限制详见 [C# 规则 - C# 5.0 禁止使用的语法](csharp-rules.md#c-50-禁止使用的语法cscode-和-csscript-均适用)
- **命名空间冲突检查（写 cscode 前必须核对）：** cscode 是完整 C# 代码，有 `using` 开头，多个命名空间同时引入时同名类型会冲突。常见冲突类型：
  - `Point` → `System.Windows.Point` 或 `System.Drawing.Point`
  - `Bitmap` → `System.Drawing.Bitmap`
  - `Image` → `System.Windows.Controls.Image` 或 `System.Drawing.Image`
  - 其他冲突类型详见 [C# 规则 - 命名空间冲突](csharp-rules.md#c-命名空间冲突最高频错误)
- **只要代码中同时出现两组命名空间的类型，所有有歧义的类型一律写全名，不要依赖短名称**

### 通知方式

cscode 中推荐用 `AppHelper`（`using Quicker.Utilities`）做 Toast 通知，不阻塞：

```csharp
using Quicker.Utilities;
AppHelper.ShowError("错误消息", false);   // 第二个参数 false 避免阻塞
AppHelper.ShowSuccess("成功消息");
AppHelper.ShowWarning("警告消息");
AppHelper.ShowInformation("提示消息");
```

`MessageBox.Show` 用于需要用户做选择（Yes/No）或其他需要阻塞等确认的场景。

### dataMapping

- 窗口需要读动作变量时才用 dataMapping
- 窗口内部产生的数据不需要通过 dataMapping 传出（cscode 直接处理）

---

## 变量类型对照

C# 脚本中读写变量必须用正确的 .NET 类型：

| VarType | .NET 类型 |
|---------|-----------|
| 3 | `System.Drawing.Bitmap` |
| 10 | `System.Collections.Generic.Dictionary<string, object>` |
| 13 | `System.Data.DataTable` |

**Bitmap 变量注意事项：**
- 剪贴板 `Clipboard.GetImage()` 返回 WPF `BitmapSource`，存入变量前需用 `CopyPixels` + `LockBits` 转为 `System.Drawing.Bitmap`
- cscode 中需要在 WPF Image 控件显示 Bitmap 变量时，用 `ToBitmapSource()` 转换（Bitmap → MemoryStream → BitmapImage）
- cscode 内部用 `static Bitmap` 字段持有数据，不要通过动作变量传递

---

## 步骤结构规范

### InputParams / OutputParams

必须是**对象（字典）**，不是数组：
```json
"InputParams": {"参数名": {"VarKey": null, "Value": "值"}}
"OutputParams": {"输出名": "变量名"}
```

### 顶层字段必须完整

ActionType=24，包含全部字段：Row, Col, ActionType, Title, Description, Icon, Path, DelayMs, Data, Data2, Data3, Children, Id, TemplateId, TemplateRevision, UseTemplate, LastEditTimeUtc, SharedActionId, ShareTimeUtc, CreateTimeUtc, AsSubProgram, SkipWhenStopRunningActions, SkipCheckUpdate, AutoUpdate, KeepInfoWhenUpdate, MinQuickerVersion, ContextMenuData, AllowScrollTrigger, EnableEvaluateVariable, IsTextProcessor, IsImageProcessor, Association, DoNotClosePanel, UserLimitation

### Variable 字段必须完整

Key, IsLocked, Type, Desc, DefaultValue, SaveState, IsInput, IsOutput, ParamName, InputParamInfo, OutputParamInfo, TableDef, CustomType, Group

---

## 复查清单

生成动作后，逐条检查：

### 结构
- [ ] ActionType = 24
- [ ] 顶层字段完整（34 个）
- [ ] Data 是合法的 JSON 字符串
- [ ] 每个 Variable 字段完整
- [ ] InputParams / OutputParams 是字典，不是数组
- [ ] OutputParams 的 value 对应的变量已在 Variables 中声明（每写一个 OutputParams 就检查一次）
- [ ] InputParams 中 `$={varName}` 引用的变量已在 Variables 中声明

### CustomWindow
- [ ] 有多实例检测（GetWindows + simpleIf + Close + stop）
- [ ] windowId 用 `$=_context.ActionId`
- [ ] 使用 qk: 控件时声明了 `xmlns:qk`，未使用时不强制
- [ ] XAML 无 `x:Class`、无 `WindowStartupLocation`
- [ ] 事件在 cscode 中绑定，不写 XAML 字符串绑定

### C# 代码
- [ ] 无 C# 5.0 禁止语法（`$""`、`?.`、`=>` 表达式体、`nameof()`）
- [ ] 命名空间冲突已全限定 — cscode/csscript 有 `using` 开头，多命名空间同时引入时同名类型会冲突，有歧义的类型（`Point`、`Bitmap`、`Image` 等）一律写全名
- [ ] 无重复 `using` 声明
- [ ] Bitmap 变量用 `System.Drawing.Bitmap`，不用 `BitmapSource`
- [ ] Clipboard.GetImage() 返回的 BitmapSource 存入变量前已转换

### 设计
- [ ] JSON 字符串中的 XAML / C# 代码已用 `\n` 换行缩进，非挤成一行
- [ ] 能在 cscode 做的事没有拆成额外步骤
- [ ] 变量数量最小化（只定义需要跨步骤传递的）
- [ ] 没有多余的 csscript 步骤
- [ ] 所有 StepRunnerKey 都是 [模块定义](modules.md) 中真实存在的模块，无臆想步骤

---

## 完整示例：文本计数动作

一个端到端示例，展示顶层字段、Variables、Steps、右键菜单、`sys:form` 设置窗口的完整结构。

**功能：** 右键菜单进入设置 → 获取选中文本 → 计算字符数 → 显示结果

```json
{
  "Row": 0, "Col": 0, "ActionType": 24,
  "Title": "文本计数", "Description": "统计选中文本的字符数",
  "Icon": "fa:Solid_Font", "Path": null, "DelayMs": 0,
  "Data": "{\"LimitSingleInstance\":false,\"SummaryExpression\":\"$$\",\"SubPrograms\":[],\"Variables\":[{\"Key\":\"config\",\"IsLocked\":false,\"Type\":10,\"Desc\":\"配置\",\"DefaultValue\":\"json:{\\\"ShowResult\\\":true}\",\"SaveState\":true,\"IsInput\":false,\"IsOutput\":false,\"ParamName\":\"\",\"InputParamInfo\":null,\"OutputParamInfo\":null,\"TableDef\":null,\"CustomType\":null,\"Group\":\"设置\"}],\"Steps\":[{\"StepRunnerKey\":\"sys:simpleIf\",\"InputParams\":{\"condition\":{\"VarKey\":null,\"Value\":\"$={quicker_in_param}==\\\"Settings\\\"\"}},\"OutputParams\":{},\"IfSteps\":[{\"StepRunnerKey\":\"sys:form\",\"InputParams\":{\"operation\":{\"VarKey\":null,\"Value\":\"dict\"},\"dictVar\":{\"VarKey\":\"config\",\"Value\":null},\"title\":{\"VarKey\":null,\"Value\":\"设置\"},\"formForDictDef\":{\"VarKey\":null,\"Value\":\"{\\\"Fields\\\":[{\\\"FieldKey\\\":\\\"ShowResult\\\",\\\"DictVarType\\\":2,\\\"Label\\\":\\\"显示结果\\\",\\\"InputMethod\\\":6}]}\"},\"stopIfFail\":{\"VarKey\":null,\"Value\":\"0\"}},\"OutputParams\":{\"isSuccess\":null,\"button\":null,\"errMessage\":null},\"IfSteps\":null,\"ElseSteps\":null,\"Note\":\"编辑配置\",\"Disabled\":false,\"Collapsed\":false,\"DelayMs\":0},{\"StepRunnerKey\":\"sys:stop\",\"InputParams\":{\"method\":{\"VarKey\":null,\"Value\":\"default\"},\"isError\":{\"VarKey\":null,\"Value\":\"0\"},\"return\":{\"VarKey\":null,\"Value\":\"\"},\"showMessage\":{\"VarKey\":null,\"Value\":\"\"}},\"OutputParams\":{},\"IfSteps\":null,\"ElseSteps\":null,\"Note\":\"设置完直接结束\",\"Disabled\":false,\"Collapsed\":false,\"DelayMs\":0}],\"ElseSteps\":null,\"Note\":\"右键菜单→设置\",\"Disabled\":false,\"Collapsed\":false,\"DelayMs\":0},{\"StepRunnerKey\":\"sys:getSelectedText\",\"InputParams\":{\"format\":{\"VarKey\":null,\"Value\":\"UnicodeText\"},\"waitMs\":{\"VarKey\":null,\"Value\":\"500\"},\"trim\":{\"VarKey\":null,\"Value\":\"1\"},\"stopIfFail\":{\"VarKey\":null,\"Value\":\"1\"}},\"OutputParams\":{\"isSuccess\":null,\"output\":\"selectedText\",\"errMessage\":null},\"IfSteps\":null,\"ElseSteps\":null,\"Note\":\"获取选中文本\",\"Disabled\":false,\"Collapsed\":false,\"DelayMs\":0},{\"StepRunnerKey\":\"sys:assign\",\"InputParams\":{\"input\":{\"VarKey\":null,\"Value\":\"$={selectedText}.Length\"},\"stopIfFail\":{\"VarKey\":null,\"Value\":\"1\"}},\"OutputParams\":{\"isSuccess\":null,\"output\":\"charCount\",\"errMessage\":null},\"IfSteps\":null,\"ElseSteps\":null,\"Note\":\"计算字符数\",\"Disabled\":false,\"Collapsed\":false,\"DelayMs\":0},{\"StepRunnerKey\":\"sys:simpleIf\",\"InputParams\":{\"condition\":{\"VarKey\":null,\"Value\":\"$={config}[\\\"ShowResult\\\"]\"}},\"OutputParams\":{},\"IfSteps\":[{\"StepRunnerKey\":\"sys:showText\",\"InputParams\":{\"type\":{\"VarKey\":null,\"Value\":\"NO_WAIT\"},\"text\":{\"VarKey\":null,\"Value\":\"$$字符数：{charCount}\"},\"title\":{\"VarKey\":null,\"Value\":\"计数结果\"},\"closeWhenLostFocus\":{\"VarKey\":null,\"Value\":\"true\"},\"winLocation\":{\"VarKey\":null,\"Value\":\"CenterScreen\"}},\"OutputParams\":{\"isSuccess\":null,\"errMessage\":null},\"IfSteps\":null,\"ElseSteps\":null,\"Note\":\"显示结果\",\"Disabled\":false,\"Collapsed\":false,\"DelayMs\":0}],\"ElseSteps\":null,\"Note\":\"根据配置决定是否显示\",\"Disabled\":false,\"Collapsed\":false,\"DelayMs\":0}],\"ContextMenuData\":\"[fa:Light_Cogs:#00A0D8]设置|Settings\"}",
  "Data2": null, "Data3": null, "Children": null,
  "Id": "a1b2c3d4-e5f6-7890-abcd-000000000001",
  "TemplateId": null, "TemplateRevision": 0, "UseTemplate": false,
  "LastEditTimeUtc": null, "SharedActionId": "", "ShareTimeUtc": null, "CreateTimeUtc": null,
  "AsSubProgram": false, "SkipWhenStopRunningActions": false, "SkipCheckUpdate": false,
  "AutoUpdate": true, "KeepInfoWhenUpdate": false, "MinQuickerVersion": "",
  "ContextMenuData": "[fa:Light_Cogs:#00A0D8]设置|Settings",
  "AllowScrollTrigger": false, "EnableEvaluateVariable": false,
  "IsTextProcessor": false, "IsImageProcessor": false,
  "Association": {"Trigger": null, "Condition": null, "Operations": null},
  "DoNotClosePanel": false, "UserLimitation": null
}
```

**Data 展开后（可读版）：**

```json
{
  "LimitSingleInstance": false,
  "SummaryExpression": "$$",
  "SubPrograms": [],
  "Variables": [
    {
      "Key": "config", "IsLocked": false, "Type": 10, "Desc": "配置",
      "DefaultValue": "json:{\"ShowResult\":true}", "SaveState": true,
      "IsInput": false, "IsOutput": false, "ParamName": "",
      "InputParamInfo": null, "OutputParamInfo": null,
      "TableDef": null, "CustomType": null, "Group": "设置"
    }
  ],
  "Steps": [
    {
      "StepRunnerKey": "sys:simpleIf",
      "InputParams": {
        "condition": {"VarKey": null, "Value": "$={quicker_in_param}==\"Settings\""}
      },
      "OutputParams": {},
      "IfSteps": [
        {
          "StepRunnerKey": "sys:form",
          "InputParams": {
            "operation": {"VarKey": null, "Value": "dict"},
            "dictVar": {"VarKey": "config", "Value": null},
            "title": {"VarKey": null, "Value": "设置"},
            "formForDictDef": {"VarKey": null, "Value": "{\"Fields\":[{\"FieldKey\":\"ShowResult\",\"DictVarType\":2,\"Label\":\"显示结果\",\"InputMethod\":6}]}"},
            "stopIfFail": {"VarKey": null, "Value": "0"}
          },
          "OutputParams": {"isSuccess": null, "button": null, "errMessage": null},
          "Note": "编辑配置"
        },
        {
          "StepRunnerKey": "sys:stop",
          "InputParams": {
            "method": {"VarKey": null, "Value": "default"},
            "isError": {"VarKey": null, "Value": "0"},
            "return": {"VarKey": null, "Value": ""},
            "showMessage": {"VarKey": null, "Value": ""}
          },
          "OutputParams": {},
          "Note": "设置完直接结束"
        }
      ],
      "Note": "右键菜单→设置"
    },
    {
      "StepRunnerKey": "sys:getSelectedText",
      "InputParams": {
        "format": {"VarKey": null, "Value": "UnicodeText"},
        "waitMs": {"VarKey": null, "Value": "500"},
        "trim": {"VarKey": null, "Value": "1"},
        "stopIfFail": {"VarKey": null, "Value": "1"}
      },
      "OutputParams": {"isSuccess": null, "output": "selectedText", "errMessage": null},
      "Note": "获取选中文本"
    },
    {
      "StepRunnerKey": "sys:assign",
      "InputParams": {
        "input": {"VarKey": null, "Value": "$={selectedText}.Length"},
        "stopIfFail": {"VarKey": null, "Value": "1"}
      },
      "OutputParams": {"isSuccess": null, "output": "charCount", "errMessage": null},
      "Note": "计算字符数"
    },
    {
      "StepRunnerKey": "sys:simpleIf",
      "InputParams": {
        "condition": {"VarKey": null, "Value": "$={config}[\"ShowResult\"]"}
      },
      "OutputParams": {},
      "IfSteps": [
        {
          "StepRunnerKey": "sys:showText",
          "InputParams": {
            "type": {"VarKey": null, "Value": "NO_WAIT"},
            "text": {"VarKey": null, "Value": "$$字符数：{charCount}"},
            "title": {"VarKey": null, "Value": "计数结果"},
            "closeWhenLostFocus": {"VarKey": null, "Value": "true"},
            "winLocation": {"VarKey": null, "Value": "CenterScreen"}
          },
          "OutputParams": {"isSuccess": null, "errMessage": null},
          "Note": "显示结果"
        }
      ],
      "Note": "根据配置决定是否显示"
    }
  ]
}
```

**要点：**
- `ContextMenuData` 在顶层和 Data 内都需要（顶层控制菜单显示，Data 内控制行为）
- `config` 词典变量用 `SaveState: true`，配合 `sys:form` 的 `dict` 模式做设置窗口
- 表达式 `$={selectedText}.Length` 直接调用属性，不需要 C#
- 文本插值 `$$字符数：{charCount}` 在 `sys:showText` 中拼接显示文本
