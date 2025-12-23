# YinYang 东方玄学人生大数据平台

YinYang 融合传统八字命理与现代数据可视化技术，通过精准的真太阳时校正和专业的命理算法，为您呈现独一无二的人生K线图。

## 项目结构

```
yinyang/
├── backend/          # FastAPI 后端服务
│   ├── main.py       # 主应用入口
│   ├── core/         # 核心算法模块
│   └── data/         # 数据文件
└── frontend/         # React 前端应用
    ├── src/          # 源代码
    └── dist/         # 构建产物
```

## 技术栈

- **后端**: Python, FastAPI, lunar-python, OpenAI
- **前端**: React, TypeScript, Vite, TailwindCSS, ECharts

## 部署

### Railway 部署

1. Fork 此仓库到您的 GitHub
2. 在 Railway 创建新项目
3. 分别部署 backend 和 frontend 目录
4. 配置环境变量

### 环境变量

**后端 (backend)**:
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥

**前端 (frontend)**:
- `VITE_API_URL`: 后端 API 地址

## 许可证

MIT License
