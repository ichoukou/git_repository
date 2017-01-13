#ifndef __PIDTOOLS_H__
#define __PIDTOOLS_H__
#include <sys/types.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/reg.h>
#include <unistd.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <iostream>
#include <string>
#include <string.h>

#define BUF_SIZE 1024
struct pid_tools{
	static std::string ret;
	static void getNameByPid(pid_t pid);
	static bool getpids();
	static void getPidByName(char *task_name);	
	static void getPidByName(std::string task_name);
};

#endif
