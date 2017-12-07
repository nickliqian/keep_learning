ls -l
ls -l | tee a.txt

ls -l > b.txt 输出重定向
cat < b.txt  输入重定向，默认描述符指向定向的位置

fun()
{
	echo "hello"
	echo "hello"
	echo "hello"
}

echo "--start--"
fun
echo "--end--"


fun()
{
	echo "hello"
	echo $0  # 文件名称
	echo $1
	echo $2
	echo $3
	echo "hello"
}

echo "--start--"
fun aa bb 11
echo "--end--"