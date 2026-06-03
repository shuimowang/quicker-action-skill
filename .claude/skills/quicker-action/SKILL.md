---
name: quicker-action
description: Generate, analyze, and modify Quicker action JSON files for Claude Code, including Quicker step modules, variables, subprograms, C# scripts, Python scripts, forms, and CustomWindow XAML/C#.
---

# Quicker 动作生成器

根据用户的需求，生成、分析、修改 Quicker 组合动作的 JSON 文件。

## 分析/修改已有动作

当用户要求"分析"、"查看"、"修改"某个已有动作时，**必须先用通信动作查询**，不要假设要新建。

**流程：**
1. 用通信动作 `info:动作名或ID` 查询，获取导出的 JSON 文件路径
2. 读取 JSON 文件，分析现有实现
3. 基于分析结果给出建议或执行修改

### 通信动作

- **动作 ID：** `3c7892bf-ef2f-41af-b63f-7cd5f4fda288`
- **数据交换目录：** `{MyDocuments}\Quicker\kkj.quicker.action\exports\`

**命令格式（PowerShell）：**
```powershell
# 查询动作信息（按ID或名称，返回JSON文件路径）
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 info:动作ID或名称`"" -NoNewWindow -Wait -RedirectStandardOutput "输出文件路径"
Get-Content "输出文件路径"

# 创建新动作（自动分配位置，返回新动作ID）
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 create:文件路径`""

# 更新已有动作（按JSON中的ID匹配）
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 update:文件路径`""

# 调试运行动作
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 debug:动作ID或名称`""
```

**使用场景：**

| 场景 | 命令 | 说明 |
|------|------|------|
| 分析/查看已有动作 | `info:动作名或ID` | 导出 JSON 到 exports 目录 |
| 生成新动作后导入 | `create:文件路径` | 自动分配位置 |
| 修改已有动作后更新 | `update:文件路径` | 按 JSON 中的 ID 匹配 |
| 测试动作是否正常 | `debug:动作名或ID` | 运行动作并检查报错 |

**返回值（通过 -c 获取 stdout）：**

| 命令 | 返回值 |
|------|--------|
| `info` | JSON文件路径 或 `未找到动作` |
| `create` | `已安装，动作Id：xxx` |
| `update` | `更新成功` |
| `debug` | `调试完成，未报错` 或 `调试报错：xxx` |

**故障排除：**
- 无返回值 → 检查 QuickerStarter.exe 路径是否正确，或通信动作是否已安装
- `未找到动作` → 确认动作名称或 ID 是否正确
- 路径含空格时需用引号包裹

详见 [通信动作](references/communication-action.md)。

## 生成新动作

用户描述想要的动作功能时：
1. **开始前：通读 [动作编写规范](references/action-spec.md)**
2. 理解需求，设计动作的步骤流程
3. 生成符合 Quicker 格式的 JSON
4. 保存为 `.json` 文件到用户指定的位置（当前工作目录）
5. **完成后：按 [动作编写规范](references/action-spec.md) 复查清单逐条检查**

## 参考文档

生成动作时，按需查阅以下参考：

- **[动作编写规范](references/action-spec.md)** — 设计原则、CustomWindow 规范、变量类型对照、复查清单（**必读**）
- [通信动作](references/communication-action.md) — 动作的创建/更新/查询/调试（**分析已有动作必读**）
- [JSON 结构](references/json-structure.md) — 顶层结构、Data、Variables、VarType、步骤、图标、子程序、参数引用
- [模块定义](references/modules.md) — 所有 StepRunnerKey 的 InputParams/OutputParams
- [多字段表单](references/form.md) — `sys:form` 的字段类型、输入方式、动态表单JSON、自动计算
- [自定义窗口](references/customwindow.md) — XAML、cscode 回调、数据映射、进阶用法
- [WebView2 浏览器窗口](references/webview2.md) — 打开网址、执行 JS、发送消息、Bridge 交互、多标签页
- [C# 规则](references/csharp-rules.md) — 命名空间冲突、IStepContext、线程选择、语法限制、内置 DLL、变量语法、XAML 规则、性能
- [网络共享子程序](references/network-subprograms.md) — 常用网络子程序列表、调用格式、版本管理

## 实现优先级（严格遵守）

按以下顺序选择方案，**能用上层就不选下层**：

1. **Quicker 内置步骤模块**（`sys:assign`、`sys:simpleIf`、`sys:form` 等）
2. **表达式 `$=`**（步骤参数内的简单计算、判断）
3. **文本插值 `$$`**（步骤参数内的文本拼接）
4. **步骤组合**（多个步骤协作）
5. **步骤组 / 子程序**（复杂流程拆分）
6. **C# 脚本 `sys:csscript`**（兜底方案，不是默认方案）

**注意：** 这里的"C# 脚本"指独立的 `sys:csscript` 步骤。CustomWindow 的 cscode 不算独立步骤——如果用了 CustomWindow，相关的获取、处理、保存逻辑都应在 cscode 中完成，而不是拆成额外的 csscript 步骤。详见 [动作编写规范](references/action-spec.md)。

**判断标准：** 如果用内置步骤 + 表达式就能实现，就不要写 C# 脚本。
只有当内置步骤明显不够用（需要复杂对象构建、内部服务调用、多步逻辑组合等）时才用脚本。

**赋值表达式能做的事（不需要 C#）：**
- 读词典：`$={config}["key"]`
- 调用方法：`$={text}.ToUpper()`、`$={text}.ToLower()`、`$={text}.Trim()`
- 属性访问：`$={text}.Length`、`$={list}.Count`
- 三元运算：`$={n}>10?"多":"少"`
- 字符拼接：`$="Hello "+{name}`
- 类型转换：`$=int.Parse({numStr})`

**只有这些才需要 C# 脚本：** Base64 编解码、数组反转、Win32 API、外部 DLL 调用、复杂对象操作

## 界面选型规则

选择界面模块时遵循"能轻则轻"原则：

| 核心需求 | 选择 | 说明 |
|----------|------|------|
| 维护配置、填写参数 | `sys:form` | 字段明确，填写后回归主流程，支持自动计算、分组、验证 |
| 复杂布局、预览、拖拽、独立窗口 | `sys:customwindow` | XAML 级别控制，重量级 |

**升级条件：**
- form → customwindow：需要预览、拖拽、复杂事件、富展示

**不要因为"更高级"就默认用 customwindow。**

## 澄清提问规范

信息不足时才提问，遵循以下规则：
- **单次只问一个问题**，不要一次问多个
- **附带选项和推荐**，格式：
```
Q1: [问题]
A. [选项]
B. [选项]
推荐：B — [理由]
```
- 能从代码/文档自行解决的不要问用户
- 不要为了"确认"而问已经明确的信息

## 生成规则

0. **每次生成新动作前，必须通读 [动作编写规范](references/action-spec.md) 和相关 references/*.md 文档** — 不读不动手，不凭记忆写代码
1. `Data` 字段必须是 JSON 字符串（需要转义）
2. 按实现优先级选择方案，优先用内置模块和表达式
3. C# 脚本通过 `context.GetVarValue()` / `context.SetVarValue()` 访问变量
4. 不需要的 OutputParams 设为 `null`
5. 默认值直接写在变量的 `DefaultValue` 里，无需单独赋值步骤
6. XAML 不要写 `WindowStartupLocation`，窗口位置由 `winLocation` 参数控制
7. 如果不需要 C# 回调，`cscode` 设为空字符串
8. 文件名格式: `{动作名}_{日期}.json`，默认保存到当前工作目录
9. 涉及配置维护优先考虑 `sys:form`，复杂交互才用 `sys:customwindow`
10. 生成后必须通过 [动作编写规范 - 复查清单](references/action-spec.md#复查清单) 逐条验证

$ARGUMENTS
