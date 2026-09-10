# 切配 Qiepei

中文社科／人文论文写作的备料 skill。**AI 切，人炒。**

## 为什么叫切配

把一篇论文的写作看成一场烹饪。烹饪本身——对材料的解读、论证的安排与力度、行文——只能由人来做。AI 自己"理解"材料的时候错误太多，写出来的原稿作者自己都不能看，看了再改要花两倍多的时间。所以 AI 不做厨师，做切配：把厨师点名要的材料从文献里切出来，洗净、分堆、贴标签、摆到案板上，等厨师下锅。

## 工作流

```
厨师：新想法 ──► （可选）和 AI 聊几句思路 ──► 写思路单 ──► 找文献、下载
                                                                  │
切配：                                    文献清单 ◄──────────────┘
                                             │
                                        引用汇编（每条引文＋完整出处＋模块归属＋便签）
                                             │
                                        材料骨架（按思路单顺序排成带脚注的正文，引文之间只有连接句）
                                             │
厨师：                                  在引文之间填入解读与论证 ──► 初稿
```

## 三条铁律

1. **不凭记忆下料。** 每条引文都能在用户给的文件里翻到，文件名＋印刷页码。
2. **不炒。** 不解读、不评价、不推论。便签只指不论，连接句只准四类。
3. **不改字。** 原文照录，删节只在同页同段内，转引必标，页码定不下来写待核不猜。

## 安装

Claude Code：

```bash
git clone https://github.com/yanouyuan-bit/Qiepei.git ~/.claude/skills/qiepei
```

或者放进项目里的 `.claude/skills/qiepei/`。Claude 桌面端／网页端：把整个仓库打包成 zip 上传为自定义 skill。

## 使用

1. 把 [assets/templates/_模板-思路单.md](assets/templates/_模板-思路单.md) 填好。
2. 把参考文献放进一个文件夹。
3. 对 Claude 说：「切配：思路单在 X，文献在 Y，先出文献清单。」
4. 确认清单后：「出引用汇编。」
5. 汇编改定后：「出第一节的材料骨架。」
6. 交付前：`python scripts/check_footnotes.py 骨架.md 汇编.md`

## 目录

```
SKILL.md                         skill 主文件：分工、铁律、四阶段工作流、便签与连接句规则
references/
  reading-guide.md               读料：PDF／扫描／OCR、页码取法、繁简、转引
  huibian-spec.md                引用汇编的结构与规则
  gujia-spec.md                  材料骨架的结构、连接句四类、禁用词表
  citation-style.md              脚注与参考文献著录格式
assets/
  templates/                     思路单、引用汇编、材料骨架三个模板
  examples/                      汇编与骨架的节选示例
scripts/
  check_footnotes.py             阶段 4 自检脚本
```

## License

MIT
