# PlantUML→SysML v2 实验图表资源

本目录存放 issue #190（【实验记录】PlantUML→SysML v2：54 对 STM 转换与现有 SysMLv2 检查器诊断能力实测）中引用的 6 张 matplotlib 图表，供 issue 内嵌渲染使用。

- fig1_code_dist.png：诊断按 code 分布
- fig2_per_pair.png：逐对诊断总数（54 对）
- fig3_size_corr.png：诊断总数 vs 模型规模（Pearson r = 0.9561）
- fig4_liftfix_effect.png：302 处源端点修复前后的诊断总数对比（6696 → 6697）
- fig5_null_msgs.png：无 code 的 1343 条诊断细分
- fig6_liftfix_rounds.png：三轮「源端点提升」修复工作量（40/155、31/125、8/22，合计 302 处 / 48 文件）

完整资产（54 份 SysML v2 代码、PlantUML 源、全部审计数据、脚本）见 issue #190 中列出的 4 个公开 gist。

图表生成脚本：python3 /tmp/gen_charts.py（依赖 matplotlib + Noto Sans CJK SC），数据源为实验目录 audit/_final_recheck.json、audit/_baseline_recheck.json、audit/fidelity_audit_report.json。
