# Quicker 动作 JSON 结构

## 顶层

```json
{
  "Row": 0,
  "Col": 0,
  "ActionType": 24,
  "Title": "动作名称",
  "Description": "描述",
  "Icon": "fa:Solid_Star",
  "Path": null,
  "DelayMs": 0,
  "Data": "{...JSON字符串...}",
  "Id": "GUID",
  "AsSubProgram": false,
  "AllowScrollTrigger": false,
  "EnableEvaluateVariable": true
}
```

## Data（JSON 字符串）

```json
{
  "LimitSingleInstance": false,
  "SummaryExpression": "$$",
  "SubPrograms": [],
  "Variables": [],
  "Steps": []
}
```

## 图标（Icon 字段）

**动作 Icon 字段**（不带 `[]`）：

```
fa:Solid_Trash          # 矢量图标，系统颜色
fa:Solid_Pen:#FF0000    # 矢量图标，自定义颜色
```

**菜单/标题内联标记**（带 `[]`）：

```
[fa:Solid_Trash]              # 矢量图标
[fa:Solid_Pen:#FF0000]        # 自定义颜色
[url:https://example.png]     # 网络图片
[icon:.txt]                   # Windows 系统图标
```

**Font Awesome 图标库：** 内置 7000+ 图标，4 种风格：
`Solid`、`Regular`、`Light`、`Brands`。格式为 `风格_名称`。

搜索：https://fontawesome.com/icons

**图标名获取：** 面板腰栏 → 工具 → 图标库，选择后自动复制名称。

`null` 表示无图标（显示文字标题）。

## 子程序（SubPrograms 字段）

子程序定义在 `SubPrograms` 数组中，变量用 `IsInput`/`IsOutput` 标记输入输出。

```json
{
  "Id": "GUID",
  "Name": "子程序名",
  "Description": "描述",
  "SummaryExpression": "$$",
  "IsLocalEdited": false,
  "IsProtected": false,
  "SubPrograms": [],
  "SharedId": null,
  "ShareTimeUtc": null,
  "UseServerVersion": null,
  "Variables": [
    {
      "Key": "inputVar", "Type": 0, "Desc": "输入",
      "IsInput": true, "IsOutput": false, "ParamName": "inputVar"
    },
    {
      "Key": "outputVar", "Type": 0, "Desc": "输出",
      "IsInput": false, "IsOutput": true, "ParamName": "outputVar"
    }
  ],
  "Steps": []
}
```

### 在 CustomWindow cscode 中调用子程序

CustomWindow 的 cscode 使用 C# 5.0，**不能写 await**，使用同步的 `RunSp`：

```csharp
var input = new Dictionary<string, object>();
input["paramName"] = value;
var output = winContext.RunSp("子程序名", input);
var result = output["outputVar"];
```

### 在 C# 脚本步骤中调用子程序

使用 `IStepContext.RunSp`：

```csharp
var input = new Dictionary<string, object>();
input["input1"] = "abc";
input["input2"] = 123;
var output = context.RunSp("子程序名", input);
var result = output["outputVar"];
```

## 变量

```json
{
  "Key": "变量名",
  "IsLocked": false,
  "Type": 0,
  "Desc": "",
  "DefaultValue": "",
  "SaveState": false,
  "IsInput": false,
  "IsOutput": false,
  "ParamName": "",
  "InputParamInfo": null,
  "OutputParamInfo": null,
  "TableDef": null,
  "CustomType": null,
  "Group": ""
}
```

### SaveState（作为状态使用）

设为 `true` 时，动作正常结束后自动将变量值持久化，下次运行时自动加载。

- 状态 key 格式：`$var:变量名`
- **只有动作正常结束才写入**，长期运行或异常退出不会保存
- 常配合 `sys:form` 用作设置窗口（详见 [form.md - 常见用法：设置窗口](form.md#常见用法设置窗口)）
- 需要实时持久化时，改用 `context.WriteState` 手动写入

### DefaultValue（默认值）

各类型的默认值写法：

| 类型 | 写法 | 示例 |
|------|------|------|
| 文本 | 直接写内容，支持多行 | `你好` |
| 布尔 | `true`/`1` 或 `false`/`0` | `true` |
| 数字 | 数字值 | `234.56` |
| 整数 | 整数 | `123` |
| 日期时间 | 日期值或天数偏移 | `2019-4-1 12:30:00` |
| 列表 | 多行，每行一项 | 多行文本 |
| 词典 | `json:` 前缀 + JSON | `json:{"key":"value"}` |

一般不要在 DefaultValue 中使用表达式或引用其他变量。

## VarType 枚举

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | Text | 文本 |
| 1 | Number | 数字(小数) |
| 2 | Boolean | 布尔(是否) |
| 3 | Image | 图片 |
| 4 | List | 文本列表 |
| 6 | DateTime | 时间日期 |
| 9 | Enum | 选项 |
| 10 | Dict | 词典 |
| 11 | Form | 表单 |
| 12 | Integer | 数字(整数) |
| 13 | Table | 表格 |
| 14 | FormForDict | 表单(词典) |
| 98 | Object | 对象 |
| 99 | Any | 任意类型 |

## 步骤基础结构

```json
{
  "StepRunnerKey": "模块类型",
  "InputParams": {
    "参数名": {"VarKey": null, "Value": "固定值"}
  },
  "OutputParams": {
    "输出名": "目标变量名"
  },
  "IfSteps": [],
  "ElseSteps": [],
  "Note": "",
  "Disabled": false,
  "Collapsed": false,
  "DelayMs": 0
}
```

**参数引用：**
- 变量：`{"VarKey": "变量名", "Value": null}`
- 固定值：`{"VarKey": null, "Value": "值"}`
- 文本插值：`{"VarKey": null, "Value": "$$你好，{name}"}`
- 表达式：`{"VarKey": null, "Value": "$=1+2"}`
