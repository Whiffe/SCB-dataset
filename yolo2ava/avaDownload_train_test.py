# python avaDownload_train_test.py
f1 = open("ava_file_names_test_v2.1.txt")   
str1='https://s3.amazonaws.com/ava-dataset/test/'
str2=''

#清空str.txt
f2 = open("str.txt", 'w').close()
i=0
#按行读取f1
for line in f1:
	i=i+1
	#在将str2和str1拼接
	str2=str1+line
	# 在str.txt中追加str2
	with open('str.txt',"a") as f2:
		f2.write(str2+"\n")
print(i)	
f1.close()
f2.close()