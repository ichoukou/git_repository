#include "tools.h"
#include <iostream>
#include <stdio.h>
long string_o_types::stol(string str)
{
    long result;
    istringstream is(str);
    is >> result;
    return result;
}

string string_o_types::ltos(long l)
{
    ostringstream os;
    os<<l;
    string result;
    istringstream is(os.str());
    //is>>hex;
    is>>result;
    return result;

}

int string_o_types::stoi(string str)  
{  
    int result;  
    istringstream is(str);  
    is >> result;  
    return result;  
}  

float string_o_types::stof(string str)  
{  
    float result;  
    istringstream is(str);  
    is >> result;  
    return result;  
}  

double string_o_types::stod(string str)  
{  
    double result;  
    istringstream is(str);  
    is >> result;  
    return result;  
}  

string string_o_types::itos(int i)  
{  
    ostringstream os;  
    os<<i;  
    string result;  
    istringstream is(os.str());  
    is>>result;  
    return result;  
  
}  

string string_o_types::ftos(float f)  
{  
    ostringstream os;  
    os<<f;  
    string result;  
    istringstream is(os.str());  
    is>>result;  
    return result;  
  
}  

string string_o_types::dtos(double d)  
{  
    ostringstream os;  
    os<<d;  
    string result;  
    istringstream is(os.str());  
    is>>result;  
    return result;  
}  

unsigned int string_o_types::stoui(string str)
{
	unsigned int result(0);//最大可表示值为4294967296（=2‘32-1）
	//从字符串首位读取到末位（下标由0到str.size() - 1）
	for (int i = str.size()-1;i >= 0;i--)
	{
		unsigned int temp(0),k = str.size() - i - 1;
		//判断是否为数字
		if (isdigit(str[i]))
		{
			//求出数字与零相对位置
			temp = str[i] - '0';
			while (k--)
				temp *= 10;
			result += temp;
		}
		else
			//exit(-1);
			break;
	}
	return result;
}


/*
string *tos(* i)     //改一下函数名，改一下类型，搞定  
{  
    ostringstream os;  
    os<<i;  
    string result;  
    istringstream is(os.str());  
    is>>result;  
    return result;  
  
}  
*/

int string_o_types::stobptr(string str, byte* result) //改一下函数名，变量类型，搞定  
{  
    istringstream is(str);  
    is >> result;  
    return 0;
} 

int ltobptr(long l, byte* ret)
{
	
	
}


string string_o_types::ltohs(long num)  
{  
    string str;  
    long Temp = num / 16;  
    int left = num % 16;  
    if (Temp > 0)  
        str += ltohs(Temp);  
    if (left < 10)  
        str += (left + '0');  
    else  
        str += ('a' + left - 10);  
    return str;  
}  

void string_rlv::split(const string& s, const string& delim, vector< string >* ret)
{	
	size_t last = 0;
	size_t index=s.find_first_of(delim,last);
	while (index!=string::npos)
	{
		ret->push_back(s.substr(last,index-last));
		last=index+1;
		index=s.find_first_of(delim,last);
	}
	if (index-last>0)
	{
		ret->push_back(s.substr(last,index-last));
	}
}



/*
int main()
{
	string s = "sdfhsdfg";
	unsigned char a[30];
	stobptr(s,a);
	printf("ad:%x\n",*a);
}
*/
