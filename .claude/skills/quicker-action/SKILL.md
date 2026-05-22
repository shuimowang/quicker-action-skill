---
name: quicker-action
description: Generate Quicker action JSON files for Claude Code, including Quicker step modules, variables, subprograms, C# scripts, Python scripts, forms, custom panels, and CustomWindow XAML/C#.
---

# Quicker 动作生成器

根据用户的需求，生成 Quicker 组合动作的 JSON 文件。

## 使用方式

用户会描述想要的动作功能，你需要：
1. 理解需求，设计动作的步骤流程
2. 生成符合 Quicker 格式的 JSON
3. 保存为 `.json` 文件到用户指定的位置（当前工作目录）

## 参考文档

生成动作时，按需查阅以下参考：

- [JSON 结构](references/json-structure.md) — 顶层结构、Data、Variables、VarType、步骤、图标、子程序、参数引用
- [模块定义](references/modules.md) — 所有 StepRunnerKey 的 InputParams/OutputParams
- [自定义窗口](references/customwindow.md) — XAML、cscode 回调、数据映射、进阶用法
- [C# 规则](references/csharp-rules.md) — 命名空间冲突、IStepContext、线程选择、语法限制、内置 DLL
- [生成后自检](references/checklist.md) — 逐条检查 C#、XAML、性能问题

## 实现优先级（严格遵守）

按以下顺序选择方案，**能用上层就不选下层**：

1. **Quicker 内置步骤模块**（`sys:assign`、`sys:simpleIf`、`sys:form` 等）
2. **表达式 `$=`**（步骤参数内的简单计算、判断）
3. **文本插值 `$$`**（步骤参数内的文本拼接）
4. **步骤组合**（多个步骤协作）
5. **步骤组 / 子程序**（复杂流程拆分）
6. **C# 脚本 `sys:csscript`**（兜底方案，不是默认方案）

**判断标准：** 如果用内置步骤 + 表达式就能实现，就不要写 C# 脚本。
只有当内置步骤明显不够用（需要复杂对象构建、内部服务调用、多步逻辑组合等）时才用脚本。

## 界面选型规则

选择界面模块时遵循"能轻则轻"原则：

| 核心需求 | 选择 | 说明 |
|----------|------|------|
| 维护配置、填写参数 | `sys:form` | 字段明确，填写后回归主流程 |
| 提供操作集合、按钮菜单 | `sys:custompanel` | JSON 驱动，轻量交互 |
| 复杂布局、预览、拖拽、独立窗口 | `sys:customwindow` | XAML 级别控制，重量级 |

**升级条件：**
- form → custompanel：交互从"填写"变为"选择操作"
- custompanel → customwindow：需要预览、拖拽、复杂事件、富展示

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

1. `Data` 字段必须是 JSON 字符串（需要转义）
2. 按实现优先级选择方案，优先用内置模块和表达式
3. C# 脚本通过 `context.GetVarValue()` / `context.SetVarValue()` 访问变量
4. 不需要的 OutputParams 设为 `null`
5. 默认值直接写在变量的 `DefaultValue` 里，无需单独赋值步骤
6. XAML 不要写 `WindowStartupLocation`，窗口位置由 `winLocation` 参数控制
7. 如果不需要 C# 回调，`cscode` 设为空字符串
8. 文件名格式: `{动作名}_{日期}.json`，默认保存到当前工作目录
9. 涉及配置维护优先考虑 `sys:form`，操作集合用 `sys:custompanel`，复杂交互才用 `sys:customwindow`
10. 生成后必须通过 [自检清单](references/checklist.md) 逐条验证

$ARGUMENTS
