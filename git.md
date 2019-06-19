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

## 添加远程仓库

> `git clone repo_url [local_name]`

## 提交修改

```shell
# 查看当前工作目录状态
git status
# 将修改添加至暂存区
git add [file_name or dir]
# 提交修改至本地仓库
git commit -m"comment"
# 提交修改至远程仓库
git push origin master
```

## 分支 (branch)

```shell
git checkout file_name
# 切换至branch_name 分支
git checkout  branch_name
# 切换至 tag_name 版本
git checkout tag_name
git checkout -b branch_name
git branch branch_name
git checkout branch_name
# 列出当前所有分支
git branch
# 列出分支并显示最后一次提交对象的信息
git branch -v
# 将当前分支与branch_name分支合并
git merge branch_name
# 删除分支 branch_name, -F 强制删除
git branch -d branch_name
###### 分支整合------分支整合有两种方式  merge 和rebase(变基)
1.  变基 git rebase  branch_name 将当前分支上的修改添加至branch_name分支
2.  使得当前分支成为branch_name分支的下游
```
