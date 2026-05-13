# WebAR 图像锚点 Demo

基于 **MindAR.js** + **A-Frame** 的 WebAR 图像追踪应用，在浏览器中实现 ARKit 级别的图像锚点功能。

## ✨ 功能

- 📷 **图像追踪** — 扫描识别图，3D 模型锚定在图像位置
- 🌐 **无需 App** — Safari / Chrome 直接打开，零安装
- 🎯 **精准锚定** — 基于 MindAR.js 计算机视觉引擎
- 🔧 **可定制** — 替换识别图和 3D 模型即可创建自己的 AR 体验

## 🚀 快速开始

1. 打开 [GitHub Pages 链接](https://e476663603.github.io/arkit-demo/)
2. 下载并打印识别图（或在另一屏幕显示）
3. 点击「启动 AR」→ 允许摄像头 → 对准识别图
4. 3D 模型出现在识别图位置！

## 📁 项目结构

```
├── index.html        # 主页面（WebAR 入口）
├── compiler.html     # 识别图编译器（生成 .mind 文件）
├── assets/
│   ├── card.mind     # MindAR 编译的追踪特征文件
│   ├── card.png      # 识别图
│   └── model.glb     # 3D 模型（GLTF 格式）
└── README.md
```

## 🔧 自定义识别图

1. 打开 `compiler.html`
2. 上传你的识别图（建议高对比度、纹理丰富的图片）
3. 编译生成 `.mind` 文件
4. 将 `.mind` 文件和对应的图片放到 `assets/` 目录
5. 修改 `index.html` 中的 `imageTargetSrc` 和图片引用

## 🔧 自定义 3D 模型

1. 准备 GLB/GLTF 格式的 3D 模型
2. 放到 `assets/` 目录
3. 修改 `index.html` 中的模型路径和 scale/rotation 参数

## 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 图像追踪 | [MindAR.js](https://github.com/hiukim/mind-ar-js) | 开源 WebAR 引擎，GPU 加速 |
| 3D 渲染 | [A-Frame](https://aframe.io/) | Mozilla WebXR 框架 |
| 模型格式 | GLTF/GLB | Web 标准 3D 格式 |
| 部署 | GitHub Pages | 静态托管，全球 CDN |

## 兼容性

- ✅ iOS Safari 15+ (iPhone/iPad)
- ✅ Android Chrome 90+
- ✅ Desktop Chrome/Safari (需要摄像头)

## 与 AR Quick Look 的区别

| 特性 | AR Quick Look | WebAR (本项目) |
|------|--------------|----------------|
| 图像锚点 | ❌ 不支持 | ✅ 支持 |
| 平面检测 | ✅ | ❌ |
| 自定义 UI | ❌ | ✅ |
| 需要 App | ❌ | ❌ |
| 模型格式 | USDZ | GLTF/GLB |

## License

MIT
