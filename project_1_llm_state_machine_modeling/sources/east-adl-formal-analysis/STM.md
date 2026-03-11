# A methodology for formal analysis and verification of EAST-ADL models - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：BBW ABS 逻辑清晰，但正文把状态机更多留给 TA 模型/工具层。

## 条目 1: BBW ABS brake-release logic under TA execution
- 控制对象：Brake-by-Wire 系统中每个 wheel ECU 的 ABS 控制逻辑
- 整理后的英文描述：For each wheel ECU, the ABS controller evaluates the slip rate. If the slip rate is larger than 0.2, the brake actuator is released and no brake is applied; otherwise the requested brake torque is used. The paper then maps each function block to timed automata with read-execute-write semantics, so the controller can be organized as an implicit cycle `read -> execute -> write -> idle`.
- 要素 1：控制分支显式给出：`slip rate > 0.2` 时进入 release/no-brake 分支，否则进入 normal torque 分支。
- 要素 2：EAST-ADL FunctionPrototype 被映射为 TA，并服从 `read-execute-write` 语义。
- 要素 3：正文没有把 ABS 的完整状态集合逐一文字化列出，因此仅标为“可整理”。
- 定位 1：`paper_content.txt` 第 4 页，Section 3 “Running Example: Brake-By-Wire”，行 22。
- 定位 2：`paper_content.txt` 第 6 页，Section 4.2，关于 `read-execute-write semantics` 与组件映射到 TA 的描述，行 31。
- 证据 1：`if the slip rate of the wheel is larger than 0.2, then the brake actuator is released and no brake is applied. Otherwise, the requested brake torque ... is used.`
- 证据 2：`read-execute-write semantics`
