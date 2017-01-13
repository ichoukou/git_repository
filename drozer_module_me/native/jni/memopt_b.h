#ifndef __MEMOPT_B_H__
#define __MEMOPT_B_H__

#include <sys/ptrace.h>  
#include <sys/types.h>  
#include <sys/wait.h>  
#include <unistd.h>  
#include <fcntl.h>
#include <sys/user.h>  
#include <string.h>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <vector>
#include "def.h"
using namespace std;

class memRW{	
	
	private:
		static bool getdata(pid_t child,  long addr, byte *str, int len);
		static bool putdata(pid_t child, long addr, byte *str, int len);
	public:
		static bool dataW(pid_t pid, long addr, byte *data, int len);
		static bool dataR(pid_t pid, long addr, byte *data, int len);
		static bool dumpMem(pid_t pid,unsigned long start_addr,unsigned long len,std::string filename);
		static int findBt(byte *bt, long btLen, byte *search, int seaLen, vector<long> &addr);
};

#endif 
