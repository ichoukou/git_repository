#ifndef _TOOLS_H_
#define _TOOLS_H_

#include <sstream>
#include <string>
#include <vector>
#include <ctype.h>
#include "def.h"
using namespace std;

class string_o_types
{
	public:
		static long stol(string str);
		static string ltos(long l);
		static int stoi(string str);
		static unsigned int stoui(string str);
		static float stof(string str);
		static double stod(string str);
		static string itos(int i);
		static string ftos(float f);
		static string dtos(double d);
		static string ltohs(long num); 
		static int stobptr(string str, byte* result);
};

class string_rlv
{
	public:
		static void split(const string& s, const string& delim, vector< string >* ret);//注意：当字符串为空时，也会返回一个空字符串
};


#endif
