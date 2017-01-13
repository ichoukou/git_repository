#ifndef __MSG_HANDLE_H__
#define __MSG_HANDLE_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <unistd.h>
#include <vector>
#include <iostream>
#include "tools.h"
#include "pidtools.h"
#include "memopt.h"
#include "memopt_b.h"
using namespace std;
#define BUFFERSIZE 500
#define BUFFER_MAPS_ITEM 500

struct maps_struct{
	long startAddr;
	long endAddr;
	char rwx[5];
	long offsetRefile;
	char dev[6];
	void clear(){
		this->startAddr = 0;
		this->endAddr = 0;
		this->offsetRefile = 0;
	}
};

class msg_handle
{
	int pid;
	void *search_content;
	int search_types;
	vector<maps_struct> maps_s;
	
	bool get_maps_structs();
	void set_search_struct(void *search_content, int search_types);
	bool search_mem();
	
	bool maps();
	public:
		string pid_ret;
		string maps_ret;
		vector<long> ret_addr;
		
		msg_handle();
		void set_pid(int pid);		
		bool msg_hangle_(vector<string> &command);
};




#endif
