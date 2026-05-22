# Quicker Action Generator — Claude Code Custom Command

Claude Code 自定义命令，用于生成 [Quicker](https://getquicker.net/) 组合动作的 JSON 文件。

> **说明：** 这是一个 Claude Code slash command（`/quicker-action`），不是 Claude Skill。安装后通过 `/quicker-action` 调用。

## 安装

将 `commands/quicker-action.md` 复制到你的项目的 `.claude/commands/` 目录下：

```bash
mkdir -p .claude/commands
cp commands/quicker-action.md .claude/commands/
```

## 使用

在 Claude Code 中输入：

```
/quicker-action 帮我做一个文本翻译动作
```

Claude 会：
1. 设计动作的步骤流程
2. 生成符合 Quicker 格式的 JSON 文件
3. 保存到当前工作目录

## 功能

- 生成可直接导入 Quicker 的动作 JSON
- 支持 C# 脚本、Python 脚本、自定义窗口等模块
- 自动处理 XAML 布局和数据绑定
- 内置实现优先级指导（内置模块 > 表达式 > C# 脚本）
- 内置界面选型规则（form > custompanel > customwindow）
- 内置常见错误自检（命名空间冲突、变量声明、XAML 语法等）

## 支持的模块

| 模块 | 说明 |
|------|------|
| `sys:assign` | 赋值/表达式 |
| `sys:csscript` | C# 脚本（v1/v2 Roslyn） |
| `sys:pythonscript` | Python 脚本 |
| `sys:simpleIf` | 条件判断 |
| `sys:form` | 参数表单 |
| `sys:custompanel` | 操作面板 |
| `sys:customwindow` | 自定义 WPF 窗口 |
| `sys:group` | 步骤组 |
| `sys:subprogram` | 子程序调用 |
| `sys:getSelectedText` | 获取选中文本 |
| `sys:translation` | 翻译 |
| `sys:showText` | 显示文本 |
| `sys:notify` | 通知提示 |

## 环境要求

- [Claude Code](https://claude.ai/code)
- [Quicker](https://getquicker.net/)（用于导入生成的动作）
