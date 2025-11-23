# sintax-tools

**将 SILVA 138.2（DADA2 格式）转换为标准 SINTAX 格式的终极工具**  
专为 vsearch / usearch 打造，混库也能做到几乎零警告！

**作者**：lwzhao  
**发布时间**：2025-11-23  
**当前版本**：1.0  
**Python 版本**：≥ 3.8  

### 注意  
**SILVA 138.2 原始数据库文件过大（> 2 GB），无法直接上传至 GitHub**  

如需使用 SILVA 138.2（DADA2 或原始格式）进行测试或建库，请联系我获取：  

**邮箱**：lw718zhao@foxmail.com  
（邮件标题建议写：`Request SILVA 138.2 database`）

---

### 功能亮点

- 仅当分类名严格为 `UCG-001` 时 → 自动替换为 “上一级有效名 UCG-001”（带空格）  
- **不处理** UCG-002、UCG-003 等其他编号  
- 彻底清除 `Incertae_Sedis`、`unidentified`、`uncultured`、`endosymbionts` 等脏词  
- 缺失层级自动填充为 `上一级_X`  
- 种名缺失自动补全为 `属_sp`，有种名则为 `属_种名`  
- 混用多个数据库也能实现 **几乎 0 WARNING**（即使不加 `--notreeok`）

> **警告**  
> 运行 usearch 时仍可能出现极少数 WARNING（如某些序列的物种注释冲突），这属于 SILVA 数据库本身注释不一致的问题，**完全不影响 SINTAX 分类准确率和结果**
> ```bash
> #警告示例
> WARNING: g:Eubacterium has parents f:Eubacteriaceae (kept) and f:Lachnospiraceae (discarded)
> 
> 
> WARNING: g:Bacillus has parents f:Bacillaceae (kept) and f:Lactobacillaceae (discarded)
> 
> 
> WARNING: g:Enterobacter has parents f:Enterobacteriaceae (kept) and f:Morganellaceae (discarded)
> 
> 
> WARNING: g:Kamptonema has parents f:Cyanobacteriia_X (kept) and f:Paraspirulinaceae (discarded)
> 
---

### 使用方法

```bash
# 查看帮助
python silva-tdu.py -h

# 基本用法（推荐）
python silva-tdu.py input.fasta output.fasta

# 快速用法（自动使用默认输出名）
python silva-tdu.py silva138_dada2.fasta
