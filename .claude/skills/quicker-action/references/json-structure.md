# Quicker 动作 JSON 结构

## 顶层

```json
{
  "Row": 0, "Col": 0, "ActionType": 24,
  "Title": "动作名称", "Description": "描述",
  "Icon": "fa:Solid_Star", "Path": null, "DelayMs": 0,
  "Data": "{...JSON字符串...}",
  "Id": "GUID",
  "AsSubProgram": false, "AllowScrollTrigger": false, "EnableEvaluateVariable": true
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

**Font Awesome 图标库：** 内置 7000+ 图标，4 种风格：`Solid`、`Regular`、`Light`、`Brands`。格式为 `风格_名称`。搜索：https://fontawesome.com/icons

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
    {"Key": "inputVar", "Type": 0, "Desc": "输入", "IsInput": true, "IsOutput": false, "ParamName": "inputVar", ...},
    {"Key": "outputVar", "Type": 0, "Desc": "输出", "IsInput": false, "IsOutput": true, "ParamName": "outputVar", ...}
  ],
  "Steps": []
}
```

在 cscode 中调用子程序：
```csharp
var input = new Dictionary<string, object> { {"paramName", value} };
var output = await winContext.RunSpAsync("子程序名", input);
var result = output["outputVar"];
```

## 变量

```json
{
  "Key": "变量名", "IsLocked": false,
  "Type": 0,        // 见下方 VarType 枚举
  "Desc": "", "DefaultValue": "",
  "SaveState": false, "IsInput": false, "IsOutput": false,
  "ParamName": "", "InputParamInfo": null, "OutputParamInfo": null,
  "TableDef": null, "CustomType": null, "Group": ""
}
```

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
  "InputParams": { "参数名": {"VarKey": null, "Value": "固定值"} },
  "OutputParams": { "输出名": "目标变量名" },
  "IfSteps": [], "ElseSteps": [],
  "Note": "", "Disabled": false, "Collapsed": false, "DelayMs": 0
}
```

**参数引用：**
- 变量：`{"VarKey": "变量名", "Value": null}`
- 固定值：`{"VarKey": null, "Value": "值"}`
- 文本插值：`{"VarKey": null, "Value": "$$你好，{name}"}`
- 表达式：`{"VarKey": null, "Value": "$=1+2"}`
