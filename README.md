# Quicker Action Generator

生成 [Quicker](https://getquicker.net/) 组合动作 JSON 文件的 AI Skill，支持 Claude Code 和 Codex CLI。

## 支持的工具

| 工具 | 指令文件 | 说明 |
|------|----------|------|
| [Claude Code](https://claude.ai/code) | `.claude/skills/quicker-action/SKILL.md` | 通过 `/quicker-action` 或自动触发 |
| [Codex CLI](https://github.com/openai/codex) | `AGENTS.md` | 自动读取项目根目录指令 |

两个工具共享同一套参考文档（`references/`），无需维护两份。

## 安装

将 `.claude/skills/quicker-action/` 目录和 `AGENTS.md` 复制到你的项目下：

**PowerShell（Windows）：**

```powershell
New-Item -ItemType Directory -Force .claude\skills
Copy-Item -Recurse path\to\quicker-action-skill\.claude\skills\quicker-action .claude\skills\
Copy-Item path\to\quicker-action-skill\AGENTS.md .
```

**Bash：**

```bash
mkdir -p .claude/skills
cp -r /path/to/quicker-action-skill/.claude/skills/quicker-action .claude/skills/
cp /path/to/quicker-action-skill/AGENTS.md .
```

## 使用

直接告诉 AI 你想要什么动作：

```
帮我做一个文本翻译动作
```

AI 会：
1. 设计动作的步骤流程
2. 生成符合 Quicker 格式的 JSON 文件
3. 在 `%TEMP%\quicker-action\<任务标识>\` 中保存并校验临时工作文件
4. 默认通过通信动作自动导入 Quicker；修改已有动作时自动更新原动作，不重复安装

## 项目结构

```
quicker-action-skill/
├── AGENTS.md                       # Codex CLI 指令文件
├── .claude/skills/quicker-action/
│   ├── SKILL.md                    # Claude Code 入口
│   └── references/
│       ├── action-spec.md          # 设计原则、复查清单
│       ├── json-structure.md       # JSON 结构、Variables、VarType
│       ├── modules.md              # 模块定义
│       ├── form.md                 # 多字段表单 sys:form
│       ├── customwindow.md         # 自定义窗口 XAML、回调
│       ├── webview2.md             # WebView2 浏览器窗口
│       ├── csharp-rules.md         # C# 规则、命名空间冲突
│       ├── communication-action.md # 通信动作（创建/更新/查询）
│       └── network-subprograms.md  # 网络共享子程序
└── README.md
```

## 功能

- 生成可直接导入 Quicker 的动作 JSON
- 支持 C# 脚本、自定义窗口等模块
- 自动处理 XAML 布局和数据绑定
- 内置实现优先级指导（内置模块 > 表达式 > C# 脚本）
- 内置界面选型规则（form > customwindow）
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
| `sys:showText` | 显示文本 |
| `sys:notify` | 通知提示 |

## 环境要求

- [Claude Code](https://claude.ai/code) 或 [Codex CLI](https://github.com/openai/codex)
- [Quicker](https://getquicker.net/)（用于导入生成的动作）
