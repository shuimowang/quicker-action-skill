# Quicker 动作分享页图文简介

为 Quicker 动作分享页生成适配 Summernote 0.8.20 的简短富文本正文。

## 输入来源

- 用户只提供粗糙介绍时，只提炼用户提供的内容。
- 用户提供动作名称或 ID 时，先通过 `info` 读取真实动作 JSON，再结合用户提供的介绍提炼。
- 动作实现与用户描述冲突时，以可验证的动作实现为准，但不要擅自补写用户未要求公开的内部细节。
- 原始材料没有提到的功能、限制、注意事项和更新说明，一律不要添加。

## 输出格式

- 只输出正文 HTML 片段。
- 不输出 `<html>`、`<head>`、`<body>`、`<style>` 或 `<script>`。
- 不输出 Markdown、代码围栏、前言、解释或结尾说明。
- 使用 Summernote 0.8.20 可直接编辑的普通 HTML。
- 优先使用 `div`、`p`、`strong`、`span`、`ul`、`ol`、`li` 和 `hr`。
- 可使用少量行内 `style` 制作浅色卡片、重点色和分隔线。
- 不使用 CSS class、复杂布局、表格、定位、动画、JavaScript 或外部样式依赖。
- 只有用户提供可用图片 URL 时才使用 `img`；不得虚构图片地址。
- 图片使用简洁响应式样式，例如 `max-width:100%;height:auto;border-radius:8px;`。

## 内容结构

优先采用以下核心区块，并根据原始内容增减：

1. 简短介绍：一小段，说明动作解决什么问题。
2. 主要特点：三至五条短句。
3. 使用方法：二至四步。

可在原文确有相关信息时增加适用场景、注意事项、配置说明或更新要点等区块。

约束：

- 每段最多两句话。
- 每个列表项尽量不超过二十个汉字。
- 不限制区块数量，但每个区块都应有明确用途，避免重复和冗长。
- 原始内容不足时可以省略区块，不要为了凑结构编造内容。
- 原始内容很多时压缩为用户一眼能看懂的短版。
- 不使用“全网最强”“神器”“颠覆性”“万能”“必装”等夸张营销词。
- 语气清楚、克制、精致，避免写成长篇说明书。

## 推荐样式

使用单列块级结构，示意如下。根据实际内容删减，不要照抄占位文字：

```html
<div style="padding:14px 16px;background:#f6f8fa;border-left:4px solid #4a90e2;border-radius:8px;">
  <p style="margin:0;line-height:1.7;">简短介绍</p>
</div>
<div style="margin-top:14px;">
  <p style="margin:0 0 8px;"><strong>主要特点</strong></p>
  <ul style="margin:0;padding-left:22px;line-height:1.8;">
    <li>特点一</li>
  </ul>
</div>
<div style="margin-top:14px;">
  <p style="margin:0 0 8px;"><strong>使用方法</strong></p>
  <ol style="margin:0;padding-left:22px;line-height:1.8;">
    <li>第一步</li>
  </ol>
</div>
```

## 输出前检查

- [ ] 只包含 HTML 正文片段
- [ ] 区块数量与原始内容相称，没有重复或凑数内容
- [ ] 功能均有输入材料或动作实现依据
- [ ] 没有夸张词、Markdown、脚本或完整网页标签
- [ ] 列表简短，段落不超过两句话
- [ ] HTML 标签闭合，行内样式简单
