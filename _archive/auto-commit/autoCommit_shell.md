# AutoCommit.sh로 구성

# PROCESS
1. Parameter Setting
	- github_id
	- github_Token
	- github_Address
	- logFile
	- SourceDir
2. git add
3. git commit
4. git push
5. cross check(awk)
6. print result

```

#!/bin/bash
baseDir=~/Obsidian.md
today=`date "+%Y-%m-%d %H:%M:%S"`

echo "##### ${today} auto push start #####"

cd ${baseDir}

echo "${today} autoCommit" >> autoCommit.log

commitMsg="AutoCommit ${today}"

git add *
git commit -m "${commitMsg}"
git push

echo '##### auto push end #####'
```