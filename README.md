# MyTools
[TOC]
### AutoRead    //微信读书自动阅读
* 功能：微信读书想看的书太贵，又不想看一些不想看的书攒书币，自动阅读脚本攒书币，
* 环境：
    - WindowsPowershell
    - adb
    - 夜神模拟器 
* 使用：
    - 夜神模拟器bin文件夹加入环境变量Path
    - 模拟器屏幕应保证是1280*720
    - 在模拟器中打开要自动阅读的书
    - 执行脚本

### Mp3Play    //使用奇葩播放模式的命令行MP3播放器
* 功能：使用混合单曲循环和随机播放的模式播放MP3
* 环境：
    - windows
    - python3
* 使用：
    - python3 play.py [path] [min] [max]
    - path是MP3所在文件夹，min为最小循环次数，max为最大循环次数
    - 可以省略所有参数，或者只有文件夹路径，或者包括所有参数

### WordToAss    //word转换到ass文件(未完成)
* 功能：字幕组打轴前期准备工作
* 环境：
    - Python3模块：python-docx, lxml