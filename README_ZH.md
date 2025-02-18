# LiblibAI LoRA管理器

## 🚀 核心功能
- **智能中文解析**：自动转换`xiaoluoli_v3.safetensors` → 小萝莉版本3
- **多维度搜索**：支持名称/标签/拼音首字母（如`xll`→小萝莉）
- **可视化预览**：支持拖拽模型到工作流节点
- **强度调控**：0.1精度调节（0.0-2.0范围）

## 📥 安装步骤
1. 下载插件包：
```bash
git clone https://github.com/liblibai/LoRA-Manager.git ComfyUI/custom_nodes/LiblibAI_LoRA_Manager
```

2. 创建模型目录：
```bash
mkdir -p ComfyUI/lora_models/{风格,人物,场景}
```

3. 安装依赖：
```bash
pip install -r ComfyUI/custom_nodes/LiblibAI_LoRA_Manager/requirements.txt
```

## 🖥️ 界面操作
| 控件         | 功能描述                     | 快捷键   |
|--------------|----------------------------|----------|
| 搜索栏       | 支持"tag:古风"过滤          | Ctrl+F   |
| 强度滑块     | 实时预览模型效果            | 鼠标滚轮 |
| 模型卡片     | 拖拽到任何CLIP文本编码器    | 按住拖动 |
| 刷新按钮     | 手动重新扫描模型目录        | F5       |

## ⚙️ 配置文件
在`ComfyUI/custom_nodes/LiblibAI_LoRA_Manager/config.yaml`中配置：
```yaml
model_paths:
  - lora_models               # 主模型目录
  - my_custom_models          # 附加目录

cache:
  max_size: 512MB             # 缓存限制
  auto_clean: true            # 自动清理旧缓存
```

## 🔧 故障排查
**问题**：模型列表中缺少文件  
✅ 检查文件扩展名是否为`.safetensors`或`.pt`  
✅ 确认文件权限（Linux/Mac需`chmod 644`）  

**问题**：节点加载失败  
✅ 运行依赖检查命令：  
```bash
python -c "import safetensors; print(safetensors.__version__)"
# 应输出 >=0.4.1
```

## 📞 技术支持
联系开发者：  
📧 Email: support@liblibai.com  
🟢 QQ群: 12345678  
🔵 Discord: [加入频道](https://discord.gg/liblibai)  

---

📄 版本: 1.2.0 | 📅 更新日期: 2024-03-20 | [查看更新日志](https://www.liblibai.com/changelog)
