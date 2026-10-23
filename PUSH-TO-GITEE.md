# 上传到 Gitee —— 按你的仓库实际情况调整过的步骤

仓库：<https://gitee.com/HOSHINO6/opd2413-keyboard>
SSH 地址：`git@gitee.com:HOSHINO6/opd2413-keyboard.git`

---

## 你贴的教程里有三处要改

### 1. `mkdir opd2413-keyboard` 不要做

教程那是"从零开始"的情况。你已经**有现成的 `upload/` 目录**，
里面的文件都准备好了。再做一次 `mkdir` 只会建个空目录。

### 2. `touch README.md` 不要做

这句是为了让空仓库有个首提对象。你有真正的 README.md，
`touch` 只更新时间戳不改内容——无害但没必要，容易让人误以为要覆盖。

### 3. 分支名先按 `master` 推

Gitee 新建仓库默认分支通常是 `master`。推成功后如需改名：

```bash
git branch -m master main
git push -u origin main
```

---

## 推荐步骤

### 前置：安装 git

Windows 上装 <https://git-scm.com/download/win>（一路默认即可），
装完**重新打开**终端让 PATH 生效。验证：

```bash
git --version
```

### 第 1 步：进入准备好的目录

```bash
cd "D:/DSH/project/OP-PAD2P/upload"
```

> 这个目录已整理好，只含本项目 16 个文件（约 87 KB），
> 不含内核移植文档、`resize_probe`、`erhai-switch*.zip` 等无关内容。

### 第 2 步：全局身份（只需一次）

```bash
git config --global user.name "小鸟游星野"
git config --global user.email "3754914326@qq.com"
```

### 第 3 步：初始化并提交

```bash
git init
git add -A
git status --short          # 先看一眼，应该只有本项目文件
git commit -m "opd2413-keyboard 1.0: GNOME 50 Wayland on-screen keyboard"
```

### 第 4 步：关联远程并推送

```bash
git remote add origin git@gitee.com:HOSHINO6/opd2413-keyboard.git
git push -u origin master
```

---

## 关于 SSH 认证

你用的是 `git@gitee.com:...`（SSH），需要满足**其中一条**：

**A. 本机已有 SSH 密钥并已上传到 Gitee**

```bash
ls ~/.ssh/id_*.pub
```

有的话把公钥内容贴到 <https://gitee.com/profile/sshkeys>

**B. 没有密钥就生成**

```bash
ssh-keygen -t ed25519 -C "3754914326@qq.com"
cat ~/.ssh/id_ed25519.pub
```

把整行贴到上面那个 Gitee 页面。

**验证连通：**

```bash
ssh -T git@gitee.com
```

看到 `Welcome to Gitee.com, 小鸟游星野!` 即成功。

> ⚠️ 别用 `C:\Users\User\.ssh\erhai_vm` —— 那是连平板的，不是 Gitee 的。

---

## 嫌 SSH 麻烦就改用 HTTPS

```bash
git remote set-url origin https://gitee.com/HOSHINO6/opd2413-keyboard.git
git push -u origin master
```

登录框里 **用户名填 Gitee 昵称，密码填私人令牌**
（<https://gitee.com/profile/personal_access_tokens> 生成，勾 `projects`）。
Gitee 不接受账号原密码，必须用令牌。

---

## 完全不想碰命令行

打开 <https://gitee.com/HOSHINO6/opd2413-keyboard>，
点「上传文件」，把 `upload/` 里的内容拖进去。
但网页上传要一个个建目录才能保持结构，文件多时不如 git。

---

## 推送成功后应看到

```
README.md           ← 首页自动渲染
LICENSE
packaging/
scripts/
docs/
dist/opd2413-keyboard_1.0_arm64.deb
```

---

## 常见报错

| 报错 | 原因 | 办法 |
|---|---|---|
| `Permission denied (publickey)` | 公钥没传到 Gitee | 见「SSH 认证」 |
| `remote origin already exists` | 重复执行过 | 用 `git remote set-url origin <地址>` |
| `rejected` / `failed to push some refs` | 远程有本地没有的提交（建仓时勾了初始化） | `git pull --rebase origin master` 后再推 |
| `Authentication failed` | 用了账号密码而非令牌 | 换私人令牌 |
| `src refspec master does not match any` | 还没 commit | 先 `git add -A && git commit -m "..."` |
