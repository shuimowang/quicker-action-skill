# 多字段表单 (`sys:form`)

显示一个多字段表单窗口，用于收集用户输入、编辑变量值或编辑词典数据。

## 工作模式

1. **编辑动作变量的值** — 表单显示时加载变量当前值，保存后写回变量
2. **编辑词典数据** — 修改词典变量内部指定键的值
3. **编辑词典数据（动态）** — 运行期间动态生成表单定义（JSON）

## InputParams

| 参数 | 说明 |
|------|------|
| `mode` | 工作模式 |
| `dictVariable` | 词典变量名（模式2/3时使用） |
| `title` | 窗口标题 |
| `formDefinition` | 表单定义（模式3传JSON，其他模式用设计器） |
| `hintText` | 表单下方提示文字，支持表达式 |
| `headerWidth` | 标题列宽度 |
| `windowWidth` | 窗口宽度 |
| `topMost` | 置顶显示 |
| `restoreActiveWindow` | 关闭后恢复输入焦点 |
| `stopOnCancel` | 取消后停止动作 |

## OutputParams

`isSuccess`、`errMessage`

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

`sys:form` 最常见的用途是作为动作的**设置窗口**，配合变量的 `SaveState` 实现跨次运行的配置持久化。

### 模式

1. 定义变量，设置 `DefaultValue`（默认值）和 `SaveState: true`
2. 用 `sys:form`（编辑动作变量模式）让用户修改这些变量
3. 用户保存后，变量值写回
4. 动作正常结束时，Quicker 自动将 SaveState 变量的值持久化
5. 下次运行时，自动读取上次保存的值

### 变量状态的 Key 格式

SaveState 变量在状态存储中的 key 为 `$var:变量名`。

也可以在 C# 脚本中通过 `context.ReadState("$var:变量名", "")` 手动读取。

### 注意事项

- **只有动作正常结束后才会写入状态**，长期运行的动作或异常退出不会保存
- 不适合需要实时持久化的场景（这种情况用 `context.WriteState` 手动写入）
- DefaultValue 支持表达式，但一般不要引用其他变量（顺序问题）

### 示例：翻译动作设置

变量定义：
```json
[
  {"Key": "srcLang", "Type": 0, "Desc": "源语言", "DefaultValue": "Auto", "SaveState": true},
  {"Key": "dstLang", "Type": 0, "Desc": "目标语言", "DefaultValue": "zh", "SaveState": true},
  {"Key": "vendor", "Type": 0, "Desc": "翻译引擎", "DefaultValue": "Baidu", "SaveState": true}
]
```

设置步骤（`sys:form` 编辑变量模式）：用户打开表单修改语言和引擎，保存后变量更新，动作结束自动持久化。
