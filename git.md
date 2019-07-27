# git笔记

## git 配置 github

1. 本机生成id_rsa.pub添加至github settings中 `ssh-keygen`
2. 验证配置 `ssh -T git@github.com`
3. 配置用户名、邮箱(/etc/giconfig(system) /home/user/.gitconfig(user)  .git/gitconfig(workspace))
   - `git config --global user.name user_name`
   - `git config --global user.email user_email`
   - `git config --list` 查看配置

## 添加远程仓库

1. 本地 `git init` 初始化 git
2. `git remote add origin git_url`

## 提交修改

> `git status` 查看当前工作目录状态
> `git add [file_name or dir]` 确认修改操作(如删除，新建)
> `git commit -m"comment"` 提交修改
> `git push origin master` 提交至origin仓库master分支

## 分支

> `git checkout file_name`
> `git checkout  branch_name` 切换至branch_name 分支
> `git checkout tag_name`   切换至tag_name 版本
> `git checkout -b branch_name`
> `git branch branch_name`
> `git checkout branch_name`
> `git branch` 列出当前所有分支
> `git branch -v` 列出分支并显示最后一次提交对象的信息
> `git merge branch_name` 将当前分支与branch_name分支合并
> `git branch -d branch_name` 删除分支branch_name   -F 强制删除

## 分支整合------分支整合有两种方式  merge 和rebase(变基)

1. 变基 `git rebase  branch_nam`e 将当前分支上的修改添加至branch_name分支
2. 使得当前分支成为branch_name分支的下游
