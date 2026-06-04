# 通信动作（动作管理）

通过 QuickerStarter.exe 调用通信动作，实现动作的创建、更新、查询、调试。

## 通信动作信息

- **动作 ID：** `3c7892bf-ef2f-41af-b63f-7cd5f4fda288`
- **动作名称：** 通信动作（kkj.quicker.action）

## 数据交换目录

```
{MyDocuments}\Quicker\kkj.quicker.action\
└── exports\          ← info 命令导出的 JSON 存放于此
```

- `{MyDocuments}` = `Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)`
- 通信动作自动管理此目录（不存在会自动创建）
- `info:` 命令导出动作到 `exports/动作名_ID.json`
- `create:` / `update:` 从指定路径读取 JSON（不限于此目录）

## 命令格式

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

## 返回值（通过 -c 获取 stdout）

| 命令 | 返回值 |
|------|--------|
| `create` | `已安装，动作Id：xxx` |
| `update` | `更新成功` |
| `info` | JSON文件路径 或 `未找到动作` |
| `debug` | `调试完成，未报错` 或 `调试报错：xxx` |

## 使用场景

| 场景 | 命令 | 说明 |
|------|------|------|
| 生成新动作后导入 | `create:文件路径` | 自动分配位置 |
| 修改已有动作后更新 | `update:文件路径` | 按 JSON 中的 ID 匹配 |
| 分析/查看已有动作 | `info:动作名或ID` | 导出 JSON 到 exports 目录 |
| 测试动作是否正常 | `debug:动作名或ID` | 运行动作并检查报错 |

## 判断动作来源

通过查询返回的 `ActionItem.Data` 字段可以判断动作来源：

| `ActionItem.Data` | 来源 | 说明 |
|--------------------|------|------|
| 非 null | 本地创建的动作 | Data 包含动作的完整 JSON，可正常 `update` |
| `null` | 动作库安装的动作 | 来自 Quicker 动作库（在线安装），Data 为空 |

**用途：** 当需要修改某个动作时，先查询判断来源。如果是动作库安装的（Data 为 null），应提示用户该动作为动作库安装，直接更新可能被动作库覆盖，建议复制为新动作后再修改。

## 注意事项

- PowerShell 中使用 `-c` 参数获取 stdout（`-Command` 的缩写）
- 路径含空格时需要用引号包裹
- `info` 命令支持按名称模糊匹配
- 导出的 JSON 文件名格式：`动作名_ID.json`

## 外部文档

https://getquicker.net/kc/manual/doc/quicker-starter
