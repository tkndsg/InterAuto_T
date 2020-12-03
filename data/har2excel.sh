init(){
	echo "环境准备中...请稍候..."
	pip3 install xlwt

	echo -e "\n\n转换小提示："
	echo "--------------------------------------------------------"
	echo "- 直接回车，会找当前文件夹下的.har结尾的文件自动转换"
	echo "- 输入har文件名，会取相对路径，即当前路径的文件名进行转换"
	echo "- 输入绝对路径har文件名，可以找到对应文件进行转换"
	echo "--------------------------------------------------------"
	echo "注意，转换结果为当前目录下的case_raw.xls，多次操作将覆盖"
	echo -e "--------------------------------------------------------\n\n"
}

input_har_path(){
	read -p "输入har文件名:" har_path

	har_path_have_har=`echo $har_path | grep -oc ".*\.har"`  # 是否是har文件
	har_path_have_slash=`echo $har_path | tr -cd "/" | wc -c | grep -o "[0-9].*"`  # 有斜杠，以判断是相对还是绝对路径

	# 空输入和
	if [[ $har_path == "" ]];
    	then
			echo "您输入的路径为空，从`pwd`目录下安找har文件来转换case"
			default_har=`find . -name "*.har"`
			default_har_count=`find . -name "*.har" | grep -oc "har"`
			echo "当前路径下有 $default_har_count 个har文件"
			if [[ $default_har_count == 0 ]];
				then
				echo "当前面目录下的har文件数量不对，请重试："
				input_har_path
    		else
	    		# adb uninstall $packageName
	    		echo -e "开始转换$default_har\n"

	    		for line in $default_har; 
	    		do
	    			execute_py $line
	    		done
				 
			fi
	elif [[ $har_path_have_har == "0" ]]; 
		then
		echo "你输入的目录有问题，不是har结尾的，请重试："
		input_har_path
    else
    	if [[ $har_path_have_slash != "0" ]]; 
    		then
    		echo "从你输入的绝对路径下转"
    	else
    		echo "从相对路径下，找到你指定的文件，进行转换"
    	fi
		execute_py $har_path
	fi
}

execute_py(){
	python3 har2excel.py $1
	echo "转化完成"
}

do_transfer(){
	init
	input_har_path
}

do_transfer
