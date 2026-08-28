# 最终报告文风与保真回读

## 使用方式

本次使用 `shuorenhua:shuorenhua`，场景为 `docs`，档位为 `minimal`，长文 scope 为 `bounded`，无源论断模式为 `audit-only`。目标文件为 `report/v60_current_vs_x1v2_baseline_cn.md`。

protected spans 包括全部数字、分子/分母、百分比、delta、版本、commit、run/artifact ID、路径、字段名、schema、表格单元格、issue 编号、引用、主体归属、否定、条件、完成态和比较方向。没有改写命令、JSON 字段、链接或表格数据。

## 动作与回读

报告是技术文档，术语、系统主语和限制条件应保留。本次只将一处“两个不同分母的指标”收束为“分母不同，不能互换”；`211/306`、`95/306`、`0/306`、`219/435` 及其指向的对象均保持不变。

第一遍保真回读确认：数值、路径、commit、字段、表格和限制逐项保留；没有新增事实、引用、机构、年份或因果关系。第二遍 residual audit 未发现需要在 `docs` 场景继续处理的开场套话、总结腔、narrator 腔或工程表演腔。所有来源性主张继续回指 archive JSON、manifest、protocol 或 source catalog；没有无源引文需要补写。保真回读通过。
