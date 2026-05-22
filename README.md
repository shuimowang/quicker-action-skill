# Quicker Action Generator — Claude Code Skill

Claude Code 自定义 Skill，用于生成 [Quicker](https://getquicker.net/) 组合动作的 JSON 文件。

> **说明：** 这是一个 Claude Code Skill（`.claude/skills/quicker-action/`），
> 安装后 Claude Code 会自动加载，无需手动调用。用户直接描述需求即可。

## 安装

将 `.claude/skills/quicker-action/` 目录复制到你的项目下：

**PowerShell（Windows）：**

```powershell
New-Item -ItemType Directory -Force .claude\skills
Copy-Item -Recurse D:\path\to\quicker-action-skill\.claude\skills\quicker-action .claude\skills\
```

**Bash：**

```bash
mkdir -p .claude/skills
cp -r /path/to/quicker-action-skill/.claude/skills/quicker-action .claude/skills/
```

## 使用

直接告诉 Claude 你想要什么动作：

```
帮我做一个文本翻译动作
```

Claude 会：
1. 设计动作的步骤流程
2. 生成符合 Quicker 格式的 JSON 文件
3. 保存到当前工作目录

## 项目结构

```
quicker-action-skill/
├── .claude/skills/quicker-action/
│   ├── SKILL.md                  # 入口（生成规则、优先级、界面选型）
│   └── references/
│       ├── json-structure.md     # JSON 结构、Variables、VarType、步骤
│       ├── modules.md            # 模块定义（assign/csscript/pythonscript 等）
│       ├── form.md               # 多字段表单 sys:form（字段类型、设置窗口）
│       ├── customwindow.md       # 自定义窗口 XAML、回调、进阶用法
│       ├── csharp-rules.md       # C# 命名空间冲突、IStepContext、线程选择
│       └── checklist.md          # 生成后自检清单
├── examples/
│   ├── demo-text-toolbox.json    # 示例动作：文本工具箱（赋值表达式、设置窗口）
│   └── demo-calculator.json      # 示例动作：计算器（自定义窗口、XAML、回调）
└── README.md
```

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
| `sys:jsscript` | JavaScript 脚本 |
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
