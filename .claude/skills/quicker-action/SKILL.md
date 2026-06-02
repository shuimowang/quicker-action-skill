---
name: quicker-action
description: Generate Quicker action JSON files for Claude Code, including Quicker step modules, variables, subprograms, C# scripts, Python scripts, forms, and CustomWindow XAML/C#.
---

# Quicker 动作生成器

根据用户的需求，生成 Quicker 组合动作的 JSON 文件。

## 使用方式

用户会描述想要的动作功能，你需要：
1. **开始前：通读 [动作编写规范](references/action-spec.md)**
2. 理解需求，设计动作的步骤流程
3. 生成符合 Quicker 格式的 JSON
4. 保存为 `.json` 文件到用户指定的位置（当前工作目录）
5. **完成后：按 [动作编写规范](references/action-spec.md) 复查清单逐条检查**

## 参考文档

生成动作时，按需查阅以下参考：

- **[动作编写规范](references/action-spec.md)** — 设计原则、CustomWindow 规范、变量类型对照、复查清单（**必读**）
- [JSON 结构](references/json-structure.md) — 顶层结构、Data、Variables、VarType、步骤、图标、子程序、参数引用
- [模块定义](references/modules.md) — 所有 StepRunnerKey 的 InputParams/OutputParams
- [多字段表单](references/form.md) — `sys:form` 的字段类型、输入方式、动态表单JSON、自动计算
- [自定义窗口](references/customwindow.md) — XAML、cscode 回调、数据映射、进阶用法
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
11. **生成后自动导入：** 使用 QuickerStarter.exe 调用导入动作，无需用户手动操作

## Skill 与 Quicker 通信

通过通信动作实现 skill 与 Quicker 的交互（创建、更新、查询、调试动作）。

**通信动作 ID：** `3c7892bf-ef2f-41af-b63f-7cd5f4fda288`

### 数据交换目录

```
{MyDocuments}\Quicker\kkj.quicker.action\
└── exports\          ← info 命令导出的 JSON 存放于此
```

- `{MyDocuments}` = `Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)`
- 通信动作自动管理此目录（不存在会自动创建）
- `info:` 命令导出动作到 `exports/动作名_ID.json`
- `create:` / `update:` 从指定路径读取 JSON（不限于此目录）

### 命令格式

```powershell
# 创建新动作（自动分配位置，返回新动作ID）
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 create:文件路径`""

# 更新已有动作（按JSON中的ID匹配）
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 update:文件路径`""

# 查询动作信息（按ID或名称，返回JSON文件路径）
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 info:动作ID或名称`""

# 调试运行动作
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 debug:动作ID或名称`""
```

### 使用场景

| 场景 | 命令 | 说明 |
|------|------|------|
| **生成后创建** | `create:文件路径` | 新动作，自动找空位安装 |
| **生成后更新** | `update:文件路径` | 已有动作，按ID更新 |
| **查询现有动作** | `info:动作ID或名称` | 导出JSON供分析 |
| **测试动作** | `debug:动作ID或名称` | 调试运行，返回结果 |

### 返回值

通过 `-c` 参数获取 stdout 返回值：
- `create` → `已安装，动作Id：xxx`
- `update` → `更新成功`
- `info` → JSON文件路径 或 `未找到动作`
- `debug` → `调试完成，未报错` 或 `调试报错：xxx`

**故障排除：** 如果调用通信动作一直没有返回值，说明该动作未安装。请提示用户先安装通信动作 `3c7892bf-ef2f-41af-b63f-7cd5f4fda288`。

### 验证流程（必须）

**每次导入动作（create 或 update）后都必须验证：**

```
1. create/update: 文件路径 → 获取结果
2. info: 动作ID → 获取导出的JSON文件路径
3. 读取导出的JSON，与原始数据比较
4. 如果严重不符：
   a. 查阅文档找出问题
   b. 修复JSON文件
   c. update: 文件路径 → 更新动作
   d. 再次 info 验证直到正确
```

**比较要点：**
- ActionType 是否为 24
- Steps 的 StepRunnerKey 是否正确
- InputParams 参数名是否正确（如 `script` 不是 `code`）
- OutputParams 参数名是否正确（如 `rtn` 不是 `result`）
- 变量 Key 和 Type 是否正确

**Why:** Quicker 导入可能静默失败或丢失字段，验证可及时发现问题并修复。

**How to apply:** 每次 create 或 update 后立即 info 查询验证，不通过则修复后重新 update，循环直到正确。

## 外部启动参考

详见 [Quicker 外部启动文档](https://getquicker.net/kc/manual/doc/quicker-starter)

### 命令行调用

```powershell
# 基本格式
"C:\Program Files\Quicker\QuickerStarter.exe" runaction:动作ID

# 传递参数（问号分隔）
"C:\Program Files\Quicker\QuickerStarter.exe" runaction:动作ID?参数内容

# 获取返回值（-c 等待20秒，-c数字 指定超时秒数）
"C:\Program Files\Quicker\QuickerStarter.exe" -c "runaction:动作ID 参数"
```

### URI 协议调用

```
quicker:runaction:动作ID
quicker:runaction:动作名称?参数
```

可在 Win+R、网页链接、快捷方式中使用。

### 动作标识方式

- **动作ID**：UUID格式，如 `00cd3048-813a-4759-98bb-7f5ef2931c50`
- **动作名称**：直接写名称（需唯一）
- **动作库ID**：从动作库安装的ID

获取动作ID：动作右键 → 信息 → 复制动作ID或URI

$ARGUMENTS
