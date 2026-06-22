---
name: quicker-action
description: Generate, inspect, import, debug, and modify Quicker action JSON files on Windows, and create Summernote-compatible rich-text descriptions for Quicker action sharing pages. Use when Codex needs to build or analyze Quicker actions, query or update actions through QuickerStarter, or prepare concise action-library introductions.
---

# Quicker Action

Create, analyze, and update Quicker combined-action JSON files. Prefer practical Quicker modules and valid JSON over clever code.

## Core Workflow

1. Run `ping` before doing any task with this skill and require the exact response `通信动作正常运行`. If it fails, stop and report that the communication action is unavailable.
2. Classify the request:
   - Existing action: query it first with `info:<action id or name>`, read the exported JSON, preserve its action ID, then use `update` after editing. Never use `create` for an existing action.
   - New action: design the step flow, variables, and UI, write a `.json` file, validate it, then automatically use `create` to import it into Quicker.
   - Import/update/debug: use the communication action through QuickerStarter.
   - Share-page description: read `references/share-description.md`; use the user's source text, and query the action first when a name or ID is supplied.
3. Load only the references needed for the requested feature. Always load `references/action-spec.md` before generating or changing action JSON.
4. Use built-in modules first, expressions second, C# only when the feature clearly requires it.
5. Create a disposable per-task directory under `%TEMP%\quicker-action\<task-id>\`. Store generated JSON, working copies, extracted code, analysis notes, screenshots, logs, and debug output there unless the user explicitly requests a persistent file.
6. Validate against the checklist in `references/action-spec.md#复查清单`, perform the required `create` or `update`, and verify the success response before reporting completion.

## Workspace Hygiene

- Keep the skill directory limited to reusable instructions, references, scripts, and assets.
- Never store exported action JSON, action-specific code, analysis notes, screenshots, logs, debug output, or unfinished action artifacts inside the skill directory.
- Use `%TEMP%\quicker-action\<task-id>\` as the disposable working directory for each task. Its contents must remain safe to delete after the task.
- For an existing action, treat the Quicker export as source material. Copy it into the task directory before editing or extracting code; preserve its action ID and update from the working copy.
- For a new action, generate and validate the JSON in the task directory, then import it with `create`.
- Keep files outside the temporary directory only when the user explicitly requests a deliverable file or supplies a destination.
- Treat `info` exports as disposable source snapshots. Keep them during the task, then remove them after a verified `create`, `update`, or completed analysis.
- Add action-specific knowledge to skill documentation only after verifying it as a reusable rule. Never preserve abandoned or half-finished action implementations as documentation.

## Quicker Communication

Use the installed communication action to query, create, update, or debug Quicker actions.

- Communication action ID: `3c7892bf-ef2f-41af-b63f-7cd5f4fda288`
- Export directory: `%TEMP%\quicker-action\exports\`
- Default QuickerStarter path: `C:\Program Files\Quicker\QuickerStarter.exe`

Prefer the bundled helper script because it handles stdout redirection and quoting:

The helper applies a 10-second timeout and automatically runs `ping` before
`info`, `create`, `update`, and `debug`. Override the timeout with
`--timeout <seconds>` or the `QUICKER_TIMEOUT` environment variable.

```powershell
python "<skill-dir>\scripts\quicker_comm.py" ping
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
| `ping` | `通信动作正常运行` |
| `info` | JSON file path, or `未找到动作` |
| `create` | `已安装，动作Id：xxx` |
| `update` | `更新成功` |
| `debug` | `调试完成，未报错`, or `调试报错：xxx` |

### Create vs. Update Decision

- A newly generated action is not complete when the JSON file is merely saved. After validation, run `create` automatically unless the user explicitly asks for file generation only.
- If an action with the intended name may already exist, run `info` first. Do not create a duplicate unless the user explicitly requests a separate copy.
- An existing action must follow `info → edit exported JSON → update`. Preserve the queried JSON's `Id`; never call `create`, because that installs a duplicate action.
- If a modification request returns `未找到动作`, do not silently create a replacement. Report that the target was not found and ask whether to create a new action.
- Treat success only as the expected communication response: `已安装，动作Id：...` for `create`, or `更新成功` for `update`.
- If Quicker or the communication action is unavailable, clearly report that the file was generated but not imported or updated.

## Share-Page Description

When the user asks for an action introduction, illustrated description, sharing-page copy, or Summernote HTML:

1. Read `references/share-description.md`.
2. Use only the user's source material unless an action name or ID is supplied.
3. If an action name or ID is supplied, query and inspect the real action before writing.
4. Return only the final Summernote 0.8.20 body HTML fragment, with no explanation or Markdown.

## Implementation Rules

Choose the lightest implementation that satisfies the requirement:

1. Quicker built-in modules such as `sys:assign`, `sys:simpleIf`, `sys:form`
2. Step parameter expressions with `$=`
3. Text interpolation with `$$`
4. Multiple coordinated steps
5. Step groups or subprograms
6. `sys:csscript` as a fallback

Use `sys:form` for configuration and ordinary parameter entry. Use `sys:customwindow` only for rich layouts, previews, drag/drop, complex events, or standalone windows. If using CustomWindow, keep related UI data handling in `cscode` instead of splitting simple callbacks into separate `sys:csscript` steps.

For CustomWindow display mode, use `Show` when the window step is terminal and no work follows its closure; this is easier to debug and update. Use `ShowAndWaitClose` only when later steps need to run after closure, consume close results, or keep the action alive for the window lifetime.

Do not use C# when an expression or built-in step is enough. Use C# when the implementation actually requires platform APIs, external DLLs, UI/STA access, or complex object construction and control flow.

## JSON Rules

- Keep `Data` as an escaped JSON string.
- Build variables before steps: every non-null `OutputParams` target, non-empty `VarKey`, expression/interpolation reference, and CustomWindow `dataMapping` variable must exist in the current `Variables` scope. When using CustomWindow `GetWindows`, declare `windowList` as Type 99 before adding the steps.
- Put default values in variable `DefaultValue`; do not add a separate initialization step unless the value is computed at runtime.
- For dictionary variables, write `DefaultValue` as direct serialized JSON such as `{"key":"value"}`; do not add a `json:` prefix.
- Access variables in C# with `context.GetVarValue()` and `context.SetVarValue()`.
- Set unused `OutputParams` to `null`.
- Do not write `WindowStartupLocation` in XAML; use the `winLocation` parameter.
- Set `cscode` to an empty string when no callback code is needed. If it contains C# code, it must define `OnWindowCreated`.
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
- `references/share-description.md`: Summernote-compatible action sharing-page introductions and HTML output rules.
