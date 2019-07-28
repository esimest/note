# Git 笔记

## 基本配置

1. 本机生成 id_rsa.pub 添加至 GitHub --> Settings --> SSH and GPG keys
2. 验证配置 `ssh -T git@github.com`
3. 配置用户名、邮箱(/etc/giconfig(system) /home/user/.gitconfig(user)  .git/gitconfig(workspace))

   ```shell
   # 基本全局配置
   git config --global user.name user_name
   git config --global user.email user_email
   # 查看配置
   git config --list
   ```

## 远程仓库

```shell
# 克隆远程仓库
git clone repo_url [local_name] [-o repo_name]

# 添加远程仓库(前提：执行了 git init)
git remote add [repo_name] remote_url

# 查看所有 远程仓库
git remote

# 从远程仓库获取数据，但不合并。repo_name 默认为 origin
git fetch [repo_name]

# 从远程仓库获取数据，且合并。repo_name 默认为 origin
git pull [repo_name]

# 推送至远程仓库。repo_name 默认为 origin, branch_name 默认为 master
git push [repo_name] [branch_name]

# 推送标签至远程仓库（默认 push 的时候不会推送标签）
git push repo_name tag_name

# 显示远程仓库信息
git remote show repo_name

# 重命名远程仓库
git remote rename old_name new_name

# 删除远程仓库
git remote rm repo_name
```

## 文件操作

### 查看文件

```shell
# 查看尚未暂存的改动
git diff
# 查看以暂存的改动
git diff --staged
```

### 提交文件

```shell
# 查看当前工作目录状态
git status

# 添加内容至下一次提交中
## 跟踪未跟踪的文件
## 将修改的已跟踪文件添加至暂存区
## 合并时将冲突文件标记为已解决状态
git add [file, path]

# 取消暂存
git reset HEAD file

# 撤销对文件的改动(前提是已暂存)
git checkout -- file

# 提交以暂存的修改至本地仓库
git commit -m"comment"

# 提交已跟踪未暂存、以暂存的修改
git commit -a -m"comment"

```

### 删除文件(前提是已跟踪)

```shell
# 仅从工作目录中删除
rm -f file

# 从工作目录和暂存区中删除
git rm file

# 仅从工作区中删除
git rm --cache file
```

### 移动文件

`git mv file_from file_to`

## 查看提交历史

```shell
# 普通查看, 一页一页的列出所有提交记录的基本信息
git log

# 查看提交的详细信息
git log -p

# 查看最新的n条提交
git log -n

# 查看提交的总结信息
git log --stat

# 查看各分支所指的提交对象
git log --decorate

# 已指定格式显示提交记录
git log --pretty=[oneline, short, full, fuller,format:"自定义格式"]

# 通过添加特殊字符，来展示分支、合并的历史
git log --graph

# 显示指定时间之前的提交
git log --before/--until

# 显示指定时间之后的提交
git log --after/since

# 显示提交信息中包含' 关键字 '的提交
git log --grep='关键字'

# 显示添加或移除 '关键字' 的提交
git log S'关键字'
```

![git log 选项](./images/git_lot.png)

## 分支 (branch)

> 每次将文件添加至暂存区时，都会生成快照，正常情况下会永久存在于 .git/objects 目录下。
> .git/objects 保存着文件的快照，快照名为文件的 hash 值。
> 提交修改时，git 会生成一个树对象，保存着快照文件的指针。然后生成一个 提交对象，指向对应的树对象。
> 分支是指向提交对象的指针，HEAD 文件保存的是当前所在的分支。
> master 是默认创建的分支。
> HEAD 是当前分支的别名。
> 提交时，对应的分支会重新指向提交后的提交对象，其它分支不变。

```shell
# 列出当前所有分支
git branch

# 列出分支并显示最后一次提交对象的信息
git branch -v

# 新建分支
git branch branch_name

# 删除分支 branch_name, -F 强制删除
git branch -d branch_name

# 迁出仓库重中文件，覆盖工作目录中的文件，使其状态为未修改状态
git checkout file_name

***********切换分支前，需要确保当前分支上所做的修改都提交了*************

# 切换至branch_name 分支
git checkout  branch_name

# 新建分支 branch_name 并切换至该分支
git checkout -b branch_name

# 切换至 tag_name 版本
git checkout tag_name

###### 分支整合------分支整合有两种方式  merge 和 rebase(变基)
1.  变基 git rebase branch_name 将当前分支上的修改添加至branch_name分支
2.  使得当前分支成为branch_name分支的下游

# 将当前分支与branch_name分支合并
git merge branch_name

```

## 标签 (tag)

```shell
# 列出所有标签
git tag

# 添加普通标签
git tag tag_name

# 添加附注标签
git tag -a tag_name -m'comment'

# 给指定的提交追加标签
git tag -a tag_name -m'comment' commit_id

# 显示 tag 对应的提交的详细信息
gti show tag_name

# 推送标签至远程仓库（默认 push 的时候不会推送标签）
git push repo_name tag_name

# 推送所有未推送过的标签
git push repo_name --tags

# 本地删除标签
git tag -d tag_name

# 远程仓库删除标签
git push repo_name :refs/tags/tag_name

# 迁出标签对应的提交
git checkout tag_name
```

## 别名

```shell
# 给 git 命令设置别名
git config --global alias.new_name old_name

# 别名实例
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'rest HEAD --'
git config --global alias.last 'log -1 HEAD'
```

## 问题

```shell
# remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.
# git commit --amend -CHEAD 好像没用
git filter-branch -f --index-filter "git rm -rf --cached --ignore-unmatch ${file_name}" -- --all
```
