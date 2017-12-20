#连接月神模拟器
nox_adb connect 127.0.0.1:62001
Start-Sleep -s 10
adb connect 127.0.0.1:62001


$flag=0 #阅读总时长计时
while($flag -lt 10800000)
{
	$dx=Get-Random -minimum 621 -maximum 651
	$dy=Get-Random -minimum 913 -maximum 953
	adb shell input tap $dx $dy #点击右侧屏幕翻页
	$t = Get-Random -minimum 30000 -maximum 50000
	Start-Sleep -m $t #阅读30-50秒
	$flag=[Int]$flag+[Int]$t
	echo $flag
}
