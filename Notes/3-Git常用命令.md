本笔记参考自[廖雪峰老师git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
1. `git init`
初始化一个本地仓库
2. `git add ./.`
添加文件到本地暂存区
3. `git commit -m "Update"`
提交文件到当前分支并写注释
`git commit -F "File Path"`
提交文件到当前分支并写入文件里面的注释
4. `git push`
推送文件到github远程仓库默认分支
`git push -u oringi master`
推送文件到github远程仓库主分支
第一次加上参数-u推送master分支的所有内容：关联本地的master分支和远程的master分支关联起来
`git push -u oringi master`
后续直接使用此命令
`git push origin dev`
推送指定分支
`#　git push -b dev`
推送文件到github远程仓库指定分支
5. `git remote add origin "github url"`
`git remote add origin git@github.com:GithubName/RespName.git`
添加远程仓库到本地记录
`git remote`
`git remote -v`
仓库远程分支信息
`git remote rm origin`
删除远程库链接
6. `git stash`
修改记录暂存本地
7. `git status`
获得本地仓库的状态，是否有文件被修改过，是否有文件需要提交。
8. `git diff`
查看修改内容（按q退出）
9. `git log`
显示从最近到最远的提交日志
`git log --pretty=oneline`
单行（简洁）显示
`git log --graph`
分支合并记录
`git log --graph --pretty=oneline --abbrev-commit`
commit线路图
10. `git reset --head HEAD^`
回到上个版本
`git reset HEAD readme.txt`
丢弃暂存区修改，结合git checkout -- FileName丢弃某个文件工作区修改
```
HEAD       当前版本
HEAD^^     一个^代表一个版本
HEAD~100   前一百个版本
```
`git reset --hard commit_id`
`git reset --hard 14c1e24f46779156c5b3386ccd704393ebf982fd`
回到指定版本
11. `git reflog`
显示执行过的所有命令
`git last`
显示最近一次的提交
12. `git checkout -- FileName`
丢弃某个文件工作区修改/撤销某个文件的删除操作
13. `git rm FileName - git commit`
确认删除
14. `ssh-keygen -t rsa -C "youremail@example.com"`
创建ssh key - id_rsa.pub
15. `git clone "github url"`
克隆仓库
16. `git checkout -b dev`
创建并且切换分支
`git branch dev`
创建分支
`git checkout dev`
切换分支
`git branch`
查看分支
`git branch -d dev`
删除分支
`git branch -D dev`
强行删除分支
`git pull <remote> <branch>`
`git branch --set-upstream dev origin/<branch>`
设定本地分支与远程分支的连接
17. `git merge BranchName`
`git merge dev`
合并指定分支到当前分支
merge 出现冲突时，解决冲突，重新add和commit、
`git merge --no-ff -m "merge with no-ff" dev`
普通模式合并，合并后的历史有分支。
18. `git stash`
隐藏现在的工作内容，进行其他工作
`git stash pop`
回到隐藏的工作内容
`git stash list = apply + drop`
列出隐藏的工作内容
`git stash apply`
应用某个工作内容
`git stash drop`
删除某个工作内容
19. 临时切换到其他任务的做法
```
git stash
git checkout master
git checkout -b issue-101
git checkout master
git merge --no-ff -m "merged bug fix 101" issue-101
git branch -d issue-101
git checkout dev
git stash list
```
20. `git pull`
拉下当前远程分支的内容，有冲突则会提示
21. 多人协作流程
```
git push origin branch-name
if fail:     git pull
if conflict: fix conflict
if no tracking information:  git branch --set-upstream branch-name origin/branch-name
git push origin branch-name
```
22. `git tag v1.0`
创建标签
`git tag`
查看标签
`git tag v0.9 6224937`
` git tag tagName commitID`
给指定commit打上标签
`git show v0.9`
查看标签信息
`git tag -a v0.1 -m "version 0.1 released" 3628164`
创建一个带说明的标签
`git tag -s v0.2 -m "signed version 0.2 released" fec145a`
给签名一个私钥
`git tag -d v0.1`
删除本地标签
`git push origin <tagname>`
推送标签到远程
`git push origin --tags`
推送所有未提交标签到远程
`git tag -d v0.9　　git push origin :refs/tags/v0.9`
删除远程标签：两步
23. 同时同步到github和码云
```
git remote add github git@github.com:michaelliao/learngit.git
git remote add gitee git@gitee.com:liaoxuefeng/learngit.git
git push github master
git push gitee master
```
24. 自定义命令名称
```
$ git config --global alias.co checkout
$ git config --global alias.ci commit
$ git config --global alias.br branch
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```
配置文件位置　.git/config
自定义别名就在[alias]后面
当前用户的Git配置文件放在用户主目录下的一个隐藏文件.gitconfig中
```
配置修改默认仓库级别
--global　用户级别
--system　系统级别
```
25. 忽略特殊文件
编写.gitignore
例如windows python:
```
# Windows:
Thumbs.db
ehthumbs.db
Desktop.ini
# Python:
*.py[cod]
*.so
*.egg
*.egg-info
dist
build
# My configurations:
db.ini
deploy_key_rsa
```
`git add -f filename`
 对忽略的文件强制添加


