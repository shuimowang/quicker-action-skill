# 网络共享子程序

来自 Quicker 网站子程序库，可直接拖放到步骤中使用。

## 调用格式

```
@@{id}@{version}@{name}
```

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 子程序 GUID | `3d7a8957-8ae3-4cd7-5327-08ddb0c7f7f4` |
| `version` | 版本号（会更新） | `7` |
| `name` | 子程序名称 | `自定义窗口检测` |

子程序网址：`https://getquicker.net/subprogram?id={id}&version={version}`

## 常用子程序

### 自定义窗口检测

多实例处理，确保自定义窗口单实例运行。

- 网址：https://getquicker.net/subprogram?id=3d7a8957-8ae3-4cd7-5327-08ddb0c7f7f4&version=7
- 调用：`@@3d7a8957-8ae3-4cd7-5327-08ddb0c7f7f4@7@自定义窗口检测`

```json
{
  "StepRunnerKey": "sys:subprogram",
  "InputParams": {
    "subProgram": {"VarKey": null, "Value": "@@3d7a8957-8ae3-4cd7-5327-08ddb0c7f7f4@7@自定义窗口检测"},
    "var:窗口标识": {"VarKey": null, "Value": "$=_context.ActionId"},
    "var:窗口操作": {"VarKey": null, "Value": "关闭窗口"},
    "stopIfFail": {"VarKey": null, "Value": "1"},
    "skipDebugOutput": {"VarKey": null, "Value": "1"}
  },
  "OutputParams": {"isSuccess": null, "errMessage": null}
}
```
