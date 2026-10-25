# 项目网站

`docs/` 目录是纯静态站点，**实际发布在 https://mybailu.cn/osk/**。
不依赖 GitHub/Gitee Pages，也不需要 CI，把 `docs/` 拷到任意 Web 服务器即可。

- 首页：`docs/index.html` —— 定位、三档尺寸交互对比、特性、安装、下载
- 技术页：`docs/tech.html` —— 十一条死路、工作原理图、中文输入三条通道、踩坑、兼容性
- 样式：`docs/assets/css/site.css`（深色底 + `#E95420`）
- 脚本：`docs/assets/js/site.js`（中英切换、尺寸切换、复制按钮、滚动淡入）
- 图片：`docs/assets/img/`（WebP，由 `docs/images/` 的原始截图压缩而来）
- 图标：`docs/favicon.svg`、`docs/assets/img/apple-touch-icon.png`、分享图 `og-cover.png`

站点不依赖任何外部 CDN（字体、图标、脚本全部本地），断网也能打开。

## 本地预览

直接用浏览器打开 `docs/index.html` 也能看；想更接近线上环境：

```bash
# 在仓库根目录
python3 -m http.server 8080 -d docs
# 打开 http://localhost:8080/
```

## 改内容

| 想改的东西 | 改哪里 |
|---|---|
| 文案 | 对应 `*.html`，中文写在标签里，英文写在同名元素的 `data-en` 属性里 |
| 带标记的段落 | 用 `data-en-html`（值里的双引号要写成 `&quot;`） |
| 版本号 / 文件大小 | 搜 `Demo` 与 `13.7`，首页与技术页各一处 |
| 配色 | `site.css` 顶部的 `:root` 变量（`--accent` 是 Ubuntu 橙） |
| 截图 | 换 `docs/images/` 的源图后，重新生成 `docs/assets/img/` 下的 WebP |

**双语机制**：页面默认是中文。JS 启动后把 `data-en` 的内容换上去（不是替换整个文档），
选择存在 `localStorage.osk-lang`。新增一段可翻译文案时，同时写中文和 `data-en` 即可。
即使 JS 不执行，中文也照常显示。

**滚动淡入**：`.reveal` 元素由 `site.js` 加 `is-hidden` 类后才隐藏，
所以禁用 JS 或脚本报错时内容不会消失（这一点别再改成 CSS 里直接 `opacity:0`）。

## 截图来源

`docs/assets/img/` 由 `docs/images/` 的六张实拍图压缩而来（1600px 宽，WebP q84）：

| 文件 | 用途 |
|---|---|
| `quick-settings*.webp` | 三档尺寸切换（全屏，看占屏比例） |
| `sizes*.webp` | 键盘裁切（看键位细节，压缩后的分享图也用它） |
| `og-cover.png` | 链接分享预览图，1200×630 |

首屏大图是 `assets/img/hero-keyboard.webp`（1378×517，25 KB），由 `docs/images/keyboard-sizes.png`
裁掉四周 11 px 浅色描边、四角做 16 px 透明圆角后转出。**全站已无外部依赖**，可以直接整目录丢 CDN。

## 发布前自查

- [ ] 首页下载按钮指向的 Gitee / GitHub Release 存在
- [ ] 版本号与 `packaging/pad-osk/DEBIAN/control` 一致
- [ ] 手机宽度（≈390–430px）下没有横向滚动
- [ ] 中英切换后没有残留中文（新加的文案漏了 `data-en`）

## 放到对象存储（阿里云 OSS 等）

`docs/` 是纯静态目录，整体上传即可，注意三点：

1. **默认首页**设成 `index.html`（OSS 的「静态页面」→ 默认首页），否则访问目录根会 404
2. **Content-Type** 要给对，否则 `.webp` 可能被当成 `application/octet-stream`：`.html`→`text/html`、`.css`→`text/css`、`.js`→`application/javascript`、`.webp`→`image/webp`、`.svg`→`image/svg+xml`
3. **缓存**：带 hash 的没有，所以 HTML 设短缓存（如 60s），CSS/JS/图片可以设长一点；改文案后记得刷新 CDN 缓存

页内链接全是相对路径，放在子目录（如 `/osk/`）下也能正常工作。
