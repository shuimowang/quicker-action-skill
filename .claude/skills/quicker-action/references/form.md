# 多字段表单 (`sys:form`)

显示一个多字段表单窗口，用于收集用户输入、编辑变量值或编辑词典数据。

## 工作模式

1. **编辑动作变量的值** — 表单显示时加载变量当前值，保存后写回变量
2. **编辑词典数据** — 修改词典变量内部指定键的值
3. **编辑词典数据（动态）** — 运行期间动态生成表单定义（JSON）

## InputParams

**编辑动作变量模式（默认）：**

| 参数 | 说明 |
|------|------|
| `title` | 窗口标题 |
| `help` | 表单下方提示文字，支持表达式 |
| `titleColumnWidth` | 标题列宽度 |
| `windowWidth` | 窗口宽度 |
| `topMost` | 置顶显示 |
| `restoreFocus` | 关闭后恢复输入焦点，`"0"` / `"1"` |
| `stopIfFail` | 取消后停止动作，`"0"` / `"1"` |

**编辑词典模式（设置窗口常用）：**

| 参数 | 说明 |
|------|------|
| `operation` | `"dict"` — 编辑词典数据 |
| `dictVar` | 词典变量（VarKey 引用） |
| `formForDictDef` | 表单定义 JSON 字符串（见下方） |

## OutputParams

`isSuccess`、`button`（点击的按钮）、`selectedGroup`、`errMessage`

## 支持的字段数据类型（VarType）

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | Text | 文本 |
| 1 | Number | 数字(小数) |
| 2 | Boolean | 布尔(是否) |
| 4 | List | 文本列表 |
| 6 | DateTime | 时间日期 |
| 12 | Integer | 数字(整数) |

## 支持的输入方式（InputMethod）

| 值 | 名称 | 适用类型 |
|----|------|----------|
| 0 | None | 无（不显示输入控件） |
| 1 | TextBox | 单行文本框 |
| 2 | TextEditor | 多行文本框 |
| 3 | DropDown | 下拉选择框 |
| 4 | Slider | 滑块 |
| 5 | DatePicker | 日期选择框 |
| 6 | CheckBox | 检查框 |
| 7 | NumberBox | 数字输入框 |
| 8 | CheckComboBox | 多选下拉框 |
| 9 | ColorPicker | 颜色选择器 |
| 10 | PasswordBox | 密码框 |
| 11 | EditableDropDown | 带选择的文本框 |
| 12 | FontFamilySelector | 字体选择器 |
| 13 | EditableAutoCompleteDropDown | 带选择的文本框(支持筛选) |
| 14 | DictEditor | 键-值对编辑器 |
| 41 | DisplayText | 显示文本(只读) |
| 100 | Separator | 分隔线 |

## 文本选择工具（TextToolType）

TextField 的 `TextTools` 字段，多个工具用英文逗号分隔：

| 名称 | 说明 |
|------|------|
| `EditInCodeWindow` | 在编辑器中修改 |
| `SelectSingleFile` | 选择一个文件 |
| `SelectMultiFile` | 选择多个文件 |
| `SelectSingleFolder` | 选择文件夹 |
| `SelectProcessPath` | 选择窗口并获取进程路径 |
| `SelectWindowTitle` | 选择窗口并获取标题 |
| `SelectLocationPoint` | 选择屏幕位置 |
| `SelectLocationArea` | 选择屏幕区域 |
| `SelectColor` | 选择屏幕颜色 |
| `SelectSavePath` | 选择保存路径 |
| `SelectIcon` | 选择图标 |
| `CaptureToFile` | 截图 |

## FormField 对象定义（动态表单JSON）

```json
{
  "FieldKey": "变量名或词典键名",
  "Label": "字段标题",
  "HelpText": "帮助提示文字",
  "InputMethod": 1,
  "DictVarType": 0,
  "IsRequired": true,
  "MinValue": "0",
  "MaxValue": "100",
  "MaxLength": 200,
  "SelectionItems": "选项1\n选项2\n选项3",
  "TextTools": "SelectSingleFile,EditInCodeWindow",
  "VisibleExpression": "$={showAdvanced}==true",
  "Group": "分组名称"
}
```

**字段属性说明：**

| 属性 | 说明 |
|------|------|
| `FieldKey` | 对应变量名或词典键名 |
| `Label` | 字段标题，支持 `_X` 标记快捷键 |
| `HelpText` | 帮助提示文字 |
| `HelpLink` | 帮助链接 |
| `InputMethod` | 输入方式（见上表） |
| `DictVarType` | 编辑词典时的值数据类型 |
| `SelectionItems` | 下拉选项，换行分隔 |
| `IsRequired` | 是否必填 |
| `MinValue` / `MaxValue` | 最小/最大值（数字、滑块） |
| `Pattern` | 验证正则表达式 |
| `MaxLength` | 最大字符数 |
| `ImeState` | 输入法状态控制 |
| `TextTools` | 文本选择工具，逗号分隔 |
| `VisibleExpression` | 可见性表达式 |
| `Group` | 分组名称 |

## 扩展设置指令

在字段的「扩展设置」参数中可添加的指令（每行一条）：

| 指令 | 说明 |
|------|------|
| `refresh_items` | 其它字段值变化时，动态刷新下拉框可选值 |
| `refresh_help` | 其它字段值变化时，刷新帮助提示内容 |
| `height:80` | 多行文本框初始高度（逻辑像素） |
| `depd:变量名1,变量名2` | 指定自动计算字段所依赖的源字段 |
| `compute:表达式` | 根据其它字段值自动计算当前字段值 |
| `notify_on_change` | 多行文本框每次修改即触发刷新，不等丢失焦点 |

## 自动计算字段

使用扩展设置中的 `depd` + `compute` 实现字段联动：

```
# 扩展设置（每行一条）
depd:单价,数量
compute:={单价} * {数量}
```

表单打开时和依赖字段变化时自动计算结果。

## JSON 示例（完整动态表单）

```json
[
  {
    "FieldKey": "name",
    "Label": "姓名",
    "HelpText": "请输入真实姓名",
    "InputMethod": 1,
    "IsRequired": true,
    "MaxLength": 20,
    "DictVarType": 0,
    "Group": "基本信息"
  },
  {
    "FieldKey": "age",
    "Label": "年龄",
    "InputMethod": 7,
    "DictVarType": 12,
    "MinValue": "1",
    "MaxValue": "150",
    "Group": "基本信息"
  },
  {
    "FieldKey": "gender",
    "Label": "性别",
    "InputMethod": 3,
    "SelectionItems": "男\n女\n其他",
    "DictVarType": 0,
    "Group": "基本信息"
  },
  {
    "FieldKey": "is_active",
    "Label": "是否激活",
    "InputMethod": 6,
    "DictVarType": 2,
    "Group": "基本信息"
  },
  {
    "FieldKey": "score",
    "Label": "分数",
    "InputMethod": 4,
    "DictVarType": 1,
    "MinValue": "0",
    "MaxValue": "100",
    "Group": "详细信息"
  },
  {
    "FieldKey": "notes",
    "Label": "备注",
    "InputMethod": 2,
    "DictVarType": 0,
    "Group": "详细信息"
  },
  {
    "FieldKey": "tags",
    "Label": "标签",
    "InputMethod": 8,
    "SelectionItems": "标签A\n标签B\n标签C",
    "DictVarType": 4,
    "Group": "详细信息"
  },
  {
    "FieldKey": "password",
    "Label": "密码",
    "InputMethod": 10,
    "IsRequired": true,
    "DictVarType": 0
  }
]
```

## 编辑词典时访问动作变量

在编辑词典数据模式下，可见性表达式中如需访问动作本身的变量：

```
$= _context.GetRootContext().GetVarValue("变量名")
```

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Tab` / `Shift+Tab` | 跳转下/上个控件 |
| `Ctrl+Tab` / `Ctrl+↓` | 跳转下个字段 |
| `Ctrl+↑` | 跳转上个字段 |
| `Alt+S` | 保存 |
| `Alt+C` / `Esc` | 取消 |
| `Alt+R` | 重置表单内容 |

## 常见用法：设置窗口

`sys:form` 最常见的用途是作为动作的**设置窗口**，配合词典变量的 `SaveState` 和右键菜单实现完整的设置入口。

### 完整模式

1. 定义一个**词典变量**（Type=10）如 `config`，设 `SaveState: true`，DefaultValue 为 JSON
2. 在动作的 `ContextMenuData` 中添加设置菜单项
3. 动作开头判断 `{quicker_in_param}`，如果是设置入口则显示表单并停止
4. 否则执行主逻辑，从 `config` 词典中读取配置

### SaveState 注意事项

- **只有主步骤的变量才能勾选 SaveState**，子程序变量不行
- **只有动作正常结束后才会写入状态**，长期运行的动作或异常退出不会保存
- 不适合需要实时持久化的场景（这种情况用 `context.WriteState` 手动写入）
- 状态 key 格式：`$var:变量名`

### 示例：带设置入口的动作

**顶层字段：**
```json
{
  "ContextMenuData": "[fa:Light_Cogs:#00A0D8]设置|Settings"
}
```

**变量定义：**
```json
[
  {
    "Key": "config",
    "Type": 10,
    "Desc": "配置",
    "DefaultValue": "{\"IsSelected\":true}",
    "SaveState": true
  }
]
```

**步骤流程：**

```
步骤1: If {quicker_in_param} == "Settings"
  → 步骤1.1: sys:form（编辑词典模式，词典变量=config）
  → 步骤1.2: sys:stop（设置完直接结束）

步骤2: If {config}["IsSelected"]
  → 步骤2.1: sys:getSelectedText（获取文本）

步骤3: sys:showText（显示结果）
```

**sys:form 编辑词典的关键参数：**

```json
{
  "StepRunnerKey": "sys:form",
  "InputParams": {
    "operation": {"VarKey": null, "Value": "dict"},
    "dictVar": {"VarKey": "config", "Value": null},
    "title": {"VarKey": null, "Value": "设置"},
    "formForDictDef": {"VarKey": null, "Value": "{\"Fields\":[{\"FieldKey\":\"IsSelected\",\"DictVarType\":2,\"Label\":\"是否获取文本\",\"InputMethod\":6}]}"},
    "titleColumnWidth": {"VarKey": null, "Value": "100"},
    "windowWidth": {"VarKey": null, "Value": "500"},
    "stopIfFail": {"VarKey": null, "Value": "0"}
  },
  "OutputParams": {"isSuccess": null, "button": null, "errMessage": null}
}
```

`formForDictDef` 是 JSON 字符串，`Fields` 数组中每个对象对应词典的一个键。
`DictVarType` 对应 VarType 枚举值，`InputMethod` 对应输入方式。
