# High accuracy traffic light controller for increasing the given green time utilization - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：下一相位选择和绿灯持续时间计算流程明确，但更偏算法化相位决策。

## 条目 1: Dynamic next-phase selection for a traffic light controller
- 控制对象：动态相位决策交通灯控制器

### 0. 条目识别与判定

- 一句话说明：这是路口交通控制领域的 dynamic traffic light controller，用于在每次相位切换时根据实时车道数据计算下一相位的绿灯方向和时长。
- 判断：算，但属于相位调度控制样本。对象是实际交通灯控制器，原文给出了“到切换时刻后生成新 phase plan，再确定绿灯组合和绿灯时长”的明确链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，System overview，对 switch to a new phase 的触发描述，行 87-89
> which will make the decisions regarding the next traffic light phase plan then forward it to the TLD to be implemented 
> there. When the time comes to switch to a new phase, the TLC will be triggered to produce a new phase plan based on a 
> new set of data, and so on.  The intersection considered in this paper was a four leg intersection as that shown in Figure

#### 摘录 B
- 出处：第 6 页，Section 3.3，对 phase plan two main values 的说明，行 137-142
> When the time c ame to change the traffic light phase, the traffic light controller would receive the latest collected 
> data for the intersection approaches and start ed the process  of producing a new traffic light phase plan.  The traffic light 
> phase plan consist ed of two main values : the index of the next phase green lights, and the phase time.  
> Figure 6  shows the internal architecture of the TLC which mainly ha d 3 blocks. The first two blocks were  the lanes ’ 
> load Calculation b lock and Graph route decision making block, and they help ed in determining the first decision , the 
> next phase green lights. While , the last block was the  next phase time decision maker which perform ed its job based on

#### 摘录 C
- 出处：第 9 页，Figure 9-10 附近，对 next phase green lights/time algorithm 的描述，行 206-224
> As can be seen in Figure 9, the next phase , green light determination process , started with initializing the 
> neighbor lists of each node. Then assigning the calculated weightage of each lane in the previous block to the 
> responsive nodes on the SIG and accordingly calculating the relations ’ values.  The n ext step was listing down the 
> available full -Mesh element -to-element pairs between the neighbours’  list members of the  two currently green 
> adjacen t node lists.  This represent ed all of the probabilities of the next phase combinations. However, there were  
>
>
> --- Page 10 ---
> 10 
>  some undesired combinations ; those might be duplicated (e.g ., CH and HC) or intersected (AC and BH) or paired to 
> itself (AA or BB, etc.).  This is wh y those combinations  were not  considered among the next phase probabilities and 
> were  eliminated.  The f inal step was to choose the two nodes of the combination with the highest weightage to act as 
> the next phase green lights.  
>  
>  
> Figure 9: The Developed Next Phase Green Light Decision Making algorithm  
> 3.3.3. Next Phase time decision making Block  
> After determining the two green traffic lights for the next phase ( those indexes are x and y in Figure 6  and Figure 
> 10), it was the time to  calculate for how long they would  stay green. This was why, the indexes x and y were  inserted as

### 2. 基于原文整理后的自然语言描述

Whenever it is time to switch phases, the traffic light controller receives the latest collected data and produces a new phase plan for the intersection. The phase plan contains the index of the next green directions and the duration for which that phase should remain green. The controller first determines the next green-light combination from the candidate lane relations and then computes the green duration from the queue-length ratios of the selected directions.

### 3. 逐句溯源

1. 句子 1：Whenever it is time to switch phases, the traffic light controller receives the latest collected data and produces a new phase plan for the intersection.
   对应摘录：A
2. 句子 2：The phase plan contains the index of the next green directions and the duration for which that phase should remain green.
   对应摘录：B
3. 句子 3：The controller first determines the next green-light combination from the candidate lane relations and then computes the green duration from the queue-length ratios of the selected directions.
   对应摘录：C
