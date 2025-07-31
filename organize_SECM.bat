@echo off
REM === 创建目录 ===
mkdir docs
mkdir diagrams
mkdir source
mkdir tex

REM === 移动文件 ===
move SECM_Model_Equations.tex docs\
move SECM_Model_Equations.pdf docs\
move SECM_VariableDictionary.tex docs\
move SECM_VariableDictionary.pdf docs\

move SECM_Flowchart.png diagrams\
move SECM_CausalDiagram.png diagrams\
move SECM_Flowchart.mermaid diagrams\
move SECM_CausalDiagram.mermaid diagrams\

move SECM_V0.4_Final.tex tex\
move SECM V0.4 Alpha.pdf tex\

REM === 提示 ===
echo Done. Files have been organized.
pause
