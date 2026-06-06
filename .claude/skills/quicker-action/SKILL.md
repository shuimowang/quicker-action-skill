---
name: quicker-action
description: Generate, inspect, import, debug, and modify Quicker action JSON files on Windows. Use when Codex needs to build Quicker combined actions, query or update existing Quicker actions through QuickerStarter, design steps, variables, subprograms, sys:form forms, sys:customwindow XAML/C# windows, WebView2 windows, or C# script modules.
---

# Quicker Action

Create, analyze, and update Quicker combined-action JSON files. Prefer practical Quicker modules and valid JSON over clever code.

## Core Workflow

1. Classify the request:
   - Existing action: query it first with `info:<action id or name>`, then read the exported JSON.
   - New action: design the step flow, variables, and UI, then write a `.json` file.
   - Import/update/debug: use the communication action through QuickerStarter.
2. Load only the references needed for the requested feature. Always load `references/action-spec.md` before generating or changing action JSON.
3. Use built-in modules first, expressions second, C# only when the feature clearly requires it.
4. Save generated files as `{action-name}_{yyyyMMdd}.json` in the current workspace unless the user gives another path.
5. Validate against the checklist in `references/action-spec.md#复查清单` before importing or reporting completion.

## Quicker Communication

Use the installed communication action to query, create, update, or debug Quicker actions.

- Communication action ID: `3c7892bf-ef2f-41af-b63f-7cd5f4fda288`
- Export directory: `{MyDocuments}\Quicker\kkj.quicker.action\exports\`
- Default QuickerStarter path: `C:\Program Files\Quicker\QuickerStarter.exe`

Prefer the bundled helper script because it handles stdout redirection and quoting:

```powershell
python "<skill-dir>\scripts\quicker_comm.py" info "动作名或ID"
python "<skill-dir>\scripts\quicker_comm.py" create "D:\path\action.json"
python "<skill-dir>\scripts\quicker_comm.py" update "D:\path\action.json"
python "<skill-dir>\scripts\quicker_comm.py" debug "动作名或ID"
```

If the helper cannot be used, invoke QuickerStarter directly:

```powershell
Start-Process "C:\Program Files\Quicker\QuickerStarter.exe" -ArgumentList "-c `"runaction:3c7892bf-ef2f-41af-b63f-7cd5f4fda288 info:动作名或ID`"" -NoNewWindow -Wait -RedirectStandardOutput "输出文件路径"
Get-Content "输出文件路径"
```

Expected responses:

| Command | Success response |
| --- | --- |
| `info` | JSON file path, or `未找到动作` |
| `create` | `已安装，动作Id：xxx` |
| `update` | `更新成功` |
| `debug` | `调试完成，未报错`, or `调试报错：xxx` |

When analyzing or modifying an existing action, never start from a blank action until `info` confirms the existing action cannot be found.

## Implementation Rules

Choose the lightest implementation that satisfies the requirement:

1. Quicker built-in modules such as `sys:assign`, `sys:simpleIf`, `sys:form`
2. Step parameter expressions with `$=`
3. Text interpolation with `$$`
4. Multiple coordinated steps
5. Step groups or subprograms
6. `sys:csscript` as a fallback

Use `sys:form` for configuration and ordinary parameter entry. Use `sys:customwindow` only for rich layouts, previews, drag/drop, complex events, or standalone windows. If using CustomWindow, keep related UI data handling in `cscode` instead of splitting simple callbacks into separate `sys:csscript` steps.

Do not use C# when an expression or built-in step is enough. C# is appropriate for Base64 encode/decode, array reversal, Win32 APIs, external DLLs, or complex object construction/manipulation.

## JSON Rules

- Keep `Data` as an escaped JSON string.
- Put default values in variable `DefaultValue`; do not add a separate initialization step unless the value is computed at runtime.
- Access variables in C# with `context.GetVarValue()` and `context.SetVarValue()`.
- Set unused `OutputParams` to `null`.
- Do not write `WindowStartupLocation` in XAML; use the `winLocation` parameter.
- Set `cscode` to an empty string when no callback code is needed.
- Preserve action IDs when updating existing actions.

## Clarifying Questions

Ask only when a required detail cannot be inferred from the request or existing action JSON. Ask one question at a time, with options and a recommendation:

```text
Q1: [question]
A. [option]
B. [option]
推荐：B - [reason]
```

## References

- `references/action-spec.md`: required for generation and modification; design principles, variables, CustomWindow rules, and final checklist.
- `references/communication-action.md`: QuickerStarter communication action details.
- `references/json-structure.md`: top-level JSON, `Data`, variables, steps, icons, subprograms, and parameter references.
- `references/modules.md`: StepRunnerKey module definitions and input/output parameters.
- `references/form.md`: `sys:form` field types, dynamic form JSON, input modes, and automatic calculation.
- `references/customwindow.md`: XAML, callbacks, data mapping, and advanced CustomWindow patterns.
- `references/webview2.md`: WebView2 URL loading, JavaScript execution, Bridge messages, and tabs.
- `references/csharp-rules.md`: C# namespaces, `IStepContext`, threading, syntax limits, built-in DLLs, variable syntax, XAML rules, and performance.
- `references/network-subprograms.md`: shared network subprogram list, invocation format, and versioning.
