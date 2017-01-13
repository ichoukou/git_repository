#ifndef __MEMOPT_H__
#define __MEMOPT_H__

#include <stdio.h>
#include <stdlib.h>
#include "memopt_b.h"
class memopt
{
	private:
		
		
	public:
		static int findString(byte *bt, long btLen, void *a, int len, vector<long> &addr);
		static int findT(byte *bt, long btLen, void *a, int types, vector<long> &addr);
		static int memWT(pid_t pid, long addr, void *a, int types);
		static int memWString(pid_t pid, long addr, void *a, int len);
		static int memfind(pid_t pid, vector<long> &addr,  vector<long> &retaddr, void *a, int types);
	
};



#endif
