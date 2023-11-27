#include <iostream>
#include <fstream>
using namespace std;

int main() {
	
	int month = 10 , day = 1;
	
	ofstream outFile;	//定义ofstream对象outFile
	
	outFile.open("file_test.txt");	//打开文件
	
	outFile << "国庆节：" << month << "月" << day << "日" << endl; //写入操作 
	
	outFile.close();	//关闭文件
	
	return 0;
}
