# GitHub 上传指南

## 前置检查

### 1. 检查当前状态
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench
git status
```

### 2. 查看将要提交的文件
```bash
# 查看已修改的文件
git status

# 查看具体修改内容
git diff
```

---

## 初次上传（如果还没有 git 仓库）

### 1. 初始化 Git 仓库
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench
git init
```

### 2. 添加所有文件
```bash
# 添加所有文件（.gitignore 会自动过滤）
git add .

# 或者分批添加（更安全）
git add README.md
git add scenarios/
git add ground_truth/
git add reports/
git add docs/
git add scripts/
git add templates/
git add *.md
```

### 3. 提交到本地仓库
```bash
git commit -m "Initial commit: AirSim-RuleBench v1.0

- 40 complete scenarios (Layer 1-2B)
- Ground truth annotations for all scenarios
- LLM validation reports (Gemini 2.5 Flash)
- Bilingual benchmark with English docs and Chinese regulation citations
- Dual validation framework (Rule Engine + LLM Engine)"
```

### 4. 创建 GitHub 远程仓库
在 GitHub 网站上创建新仓库（不要初始化 README）

### 5. 关联远程仓库
```bash
# 替换 YOUR_USERNAME 和 YOUR_REPO_NAME
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 或使用 SSH（推荐）
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

### 6. 推送到 GitHub
```bash
# 首次推送（创建 main 分支）
git branch -M main
git push -u origin main
```

---

## 后续更新（已有 git 仓库）

### 1. 查看修改状态
```bash
git status
```

### 2. 添加修改的文件
```bash
# 添加所有修改
git add .

# 或添加特定文件
git add docs/
git add reports/
git add README.md
```

### 3. 提交修改
```bash
git commit -m "Update: 描述你的修改内容"

# 示例：
git commit -m "Update: Standardize all report formats to English"
git commit -m "Add: Language note in README for bilingual project"
git commit -m "Fix: Correct TEST_GUIDE formatting for S021-S040"
```

### 4. 推送到 GitHub
```bash
git push origin main

# 如果遇到冲突，先拉取
git pull origin main
git push origin main
```

---

## .gitignore 说明

当前配置会 **忽略** 以下内容：
- ✅ Python 缓存文件 (`__pycache__/`, `*.pyc`)
- ✅ IDE 配置文件 (`.vscode/`, `.idea/`)
- ✅ 系统文件 (`.DS_Store`)
- ✅ 环境变量文件 (`.env`)
- ✅ 临时生成脚本 (`scripts/generate_*.py`)
- ✅ 备份文件 (`*.bak`, `*_old.*`)

当前配置会 **保留** 以下内容：
- ✅ 所有场景配置文件 (`scenarios/`)
- ✅ Ground truth 文件 (`ground_truth/`)
- ✅ 报告文件 (`reports/`)
- ✅ 测试指南 (`docs/`)
- ✅ 核心脚本 (`scripts/*.py`)
- ✅ 轨迹文件 (`test_logs/*.json`) - 可选

**如果想排除轨迹文件**（节省空间），取消注释 `.gitignore` 中的：
```gitignore
test_logs/*.json
```

---

## 推荐的上传流程

### 首次上传完整项目
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench

# 1. 检查 git 状态
git status

# 2. 如果还没初始化，执行初始化
git init

# 3. 添加所有文件
git add .

# 4. 查看将要提交的内容
git status

# 5. 提交
git commit -m "Initial commit: AirSim-RuleBench v1.0"

# 6. 关联远程仓库（替换你的用户名和仓库名）
git remote add origin https://github.com/YOUR_USERNAME/AirSim-RuleBench.git

# 7. 推送
git branch -M main
git push -u origin main
```

---

## 常用命令速查

```bash
# 查看状态
git status

# 查看修改
git diff

# 查看提交历史
git log --oneline

# 撤销未提交的修改
git checkout -- filename

# 撤销已添加但未提交的文件
git reset HEAD filename

# 修改最后一次提交信息
git commit --amend

# 查看远程仓库
git remote -v

# 拉取最新代码
git pull origin main
```

---

## 文件大小建议

如果项目过大（>100MB），考虑：
1. 排除大型轨迹文件
2. 使用 Git LFS 管理大文件
3. 压缩测试日志

当前项目估计大小：
- scenarios: ~500KB
- ground_truth: ~1.5MB
- reports: ~2MB
- docs: ~500KB
- scripts: ~300KB
- test_logs: 可能很大（取决于轨迹数量）

**总计**: 约 5-10MB（不含 test_logs）

---

## 推荐的 GitHub 仓库设置

创建仓库时：
- ✅ **Public** 或 **Private**（根据需要）
- ✅ **不要初始化 README**（本地已有）
- ✅ **不要添加 .gitignore**（本地已有）
- ✅ **不要添加 License**（可以后续添加）

推荐 License：
- MIT License（最宽松，推荐学术项目）
- Apache 2.0（包含专利保护）
- GPL-3.0（要求衍生作品开源）

---

## 注意事项

⚠️ **上传前检查**：
1. 确认没有敏感信息（API keys, passwords）
2. 检查 `.gitignore` 是否正确过滤
3. 确认所有文件都是英文路径（中文路径可能有问题）
4. 验证文件大小（单个文件 <100MB，总项目 <1GB）

⚠️ **不要提交的内容**：
- ❌ API keys（使用环境变量）
- ❌ 个人配置文件
- ❌ 大型二进制文件
- ❌ 临时测试文件
- ❌ 编译产物

✅ **应该提交的内容**：
- ✅ 源代码
- ✅ 配置文件示例
- ✅ 文档
- ✅ 测试数据
- ✅ README 和 LICENSE
