# ViTAL: A Verification Tool for EAST-ADL Models Using UPPAAL PORT - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：有 BBW 功能约束和 fp 执行周期，但显式状态较少。

## 条目 1: EAST-ADL function block execution with BBW ABS guard
- 控制对象：ViTAL 中的 EAST-ADL 功能块执行语义与 BBW ABS 控制约束
- 整理后的英文描述：The paper models each FunctionPrototype with an interface-augmented timed automaton that reads inputs, executes internal behavior, and writes outputs. For the Brake-by-Wire system, one functional requirement is explicit: when the slip rate exceeds 0.2, the brake actuator is released and no brake is applied. This can be reorganized as an implicit controller cycle `read -> execute -> write`, with a guard selecting the no-brake branch.
- 要素 1：fp 的执行顺序是 read input ports -> execute -> write outputs。
- 要素 2：第 8 页给出 BBW 的 guard：`s > 0.2 => brake = 0`。
- 要素 3：显式状态名主要在自动机/图中，没有完整文字化，因此标为“可整理”。
- 定位 1：`paper_content.txt` 第 5 页，关于 fp 接口与 `run-to-completion` / read-write 行为，行 303-343。
- 定位 2：`paper_content.txt` 第 8 页，Figure 8 Brake by Wire control system，行 557-564。
- 证据 1：`the internal computation of an fp starts with reading all input flow ports`
- 证据 2：`before writing the variables to the output flow ports`
- 证据 3：`if the slip rate variable exceeds 0.2, the brake actuator is released and no brake is applied`
