# 发布与推送说明

本仓库同时发布在两个平台，内容对等：

| 平台 | 地址 |
|---|---|
| GitHub | <https://github.com/HOSHINO61/opd2413-keyboard> |
| Gitee | <https://gitee.com/HOSHINO6/opd2413-keyboard> |

中国大陆用户建议用 Gitee，下载更快。两个仓库的 `master` 分支和 `v1.0` 发行版内容一致。

---

## 仓库结构说明

本目录是**独立的发布仓库**，只含屏幕键盘项目本身。开发时它嵌在一个更大的工作目录里
（同目录还有内核移植文档、镜像、探针程序等），那些内容不属于本项目，也没有提交进来。

因此本仓库**不需要**白名单式 `.gitignore`。把本目录挪到任何地方都能正常构建。

---

## 推送流程

```bash
git add -A
git status --short          # 提交前先看一眼
git commit -m "说明写什么"
git push github master
git push gitee  master
```

两个远程都推，保持对等。

初次克隆后需要手工添加远程（仓库里不记录远程地址）：

```bash
git remote add github git@github.com:HOSHINO61/opd2413-keyboard.git
git remote add gitee  git@gitee.com:HOSHINO6/opd2413-keyboard.git
```

---

## 认证

**GitHub** — SSH 公钥：<https://github.com/settings/keys>

**Gitee** — SSH 公钥：<https://gitee.com/profile/sshkeys>

验证：

```bash
ssh -T git@github.com
ssh -T git@gitee.com
```

> Gitee 有两点容易踩：
> 1. 如果账号开启了**邮箱隐私保护**，提交里的真实邮箱会被拒绝推送
>    （`Push will publish a hidden email`）。用 `<登录名>@users.noreply.gitee.com`
>    这个地址即可。
> 2. Gitee **不接受账号原密码**推送 HTTPS，必须用私人访问令牌
>    （<https://gitee.com/profile/personal_access_tokens>，勾 `projects`）。

---

## 发布新版本

改版本号 → 重新构建 → 打 tag → 建发行版并挂上 deb。

```bash
# 1. 改 packaging/opd2413-keyboard/DEBIAN/control 里的 Version
# 2. 重新构建
sh packaging/build-deb.sh

# 3. 提交并打 tag
git add -A
git commit -m "release 1.1"
git tag -a v1.1 -m "v1.1"
git push github master --tags
git push gitee  master --tags

# 4. 到网页上传 dist/ 里的 .deb 作为发行版附件
```

> **注意**：`dpkg` 的版本比较是分段的，`1.1` > `1.0`，但 `1.0` < `1.0.0`。
> 同一版本号不要中途改位数，否则会被当成降级。

---

## 换行符（重要）

`.gitattributes` 强制 `eol=lf`，这是刻意的：

- `scripts/*.sh`、`packaging/opd2413-keyboard/DEBIAN/*` 是 Linux 脚本，
  若被检出成 CRLF，运行时报 `bad interpreter: /bin/sh^M`
- `*.deb` 标为 `binary`，不做任何转换

**不要删除 `.gitattributes`**，也不要加白名单式 `.gitignore` 把它们排除掉。
