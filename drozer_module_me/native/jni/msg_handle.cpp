#include "msg_handle.h"

msg_handle::msg_handle()
{
	this->pid = 0;
	this->search_content = NULL;
	this->search_types = 100;
	this->maps_ret = "";
	this->pid_ret = "";
}
void msg_handle::set_pid(int pid){
	this->pid = pid;
}

void msg_handle::set_search_struct(void *search_content, int search_types)
{
	this->search_content = search_content;
	this->search_types = search_types;
}


bool msg_handle::get_maps_structs()
{
	this->maps_s.clear();
	//得到该pid的maps文件名
	string filename = "/proc/";
	filename += string_o_types::itos(pid);
	filename += "/maps";
	
	//得到该pid的maps文件
	FILE *read_fp = fopen(filename.c_str(),"r");
	if (!read_fp) {
		return false;
	}
	
	maps_struct maps = {0};  //用于存储maps一条数据的结构
	char buffer[BUFFERSIZE];  //用于存储maps中的一条数据string
 
	while ( fgets(buffer, BUFFERSIZE, read_fp) ){
		maps.clear();
		if ( (sscanf(buffer, "%lx-%lx %s %lx %s", &maps.startAddr, &maps.endAddr, maps.rwx, &maps.offsetRefile, maps.dev)) == 5
		  //&& (!strcmp((const char *)maps.dev, "00:00") || !strcmp((const char *)maps.dev, "00:04"))
		  //&& !maps.offsetRefile
		  && strstr((const char *)maps.rwx, "rw-"))
		  
		{	
			this->maps_s.push_back(maps);
		}
	}
	fclose(read_fp);
	if(this->maps_s.size() == 0)
		return false;
	return true;
}

bool msg_handle::maps()
{
	maps_ret = ""; //先将maps_ret清空
	
	string filename = "/proc/";
	filename += string_o_types::itos(this->pid);
	filename += "/maps";
	//cout<<filename<<endl;

	//得到改pid的maps文件
	FILE *read_fp = fopen(filename.c_str(),"r");
	if (!read_fp) {
		return false;
	}
	
	char buffer[BUFFER_MAPS_ITEM];
	while ( fgets(buffer, BUFFERSIZE, read_fp) ){
		this->maps_ret += buffer;
	}
	fclose(read_fp);
	if(this->maps_ret.size() == 0)
		return false;
	return true;
}

bool msg_handle::search_mem()
{
	ret_addr.clear();
	vector <long> addr;
	for(vector<maps_struct>::size_type ix = 0; ix!=this->maps_s.size(); ix++) 
	{
		addr.clear();
		long length = maps_s[ix].endAddr - maps_s[ix].startAddr;
		byte* dumpString = (byte*)malloc(length * sizeof(byte));
		if(!memRW::dataR(pid, maps_s[ix].startAddr, dumpString, length))
			return false;
		
		if(search_types!=9)
		{
			memopt::findT(dumpString,length,search_content,search_types,addr);
			for(vector<long>::size_type ix2 = 0; ix2 != addr.size(); ix2++)
			{
				addr[ix2] += maps_s[ix].startAddr;
				ret_addr.push_back(addr[ix2]);
				//printf("%lx \n" ,addr[ix2]);
			}
		}
		else
		{
			memopt::findString(dumpString,length,search_content,search_types,addr);
			for(vector<long>::size_type ix2 = 0; ix2 != addr.size(); ix2++)
			{
				addr[ix2] += maps_s[ix].startAddr;
				ret_addr.push_back(addr[ix2]);
				//printf("%lx \n" ,addr[ix2]);
			}
		}
		free(dumpString);
	}
	if(ret_addr.size() == 0)
		return false;
	return true;
}

bool msg_handle::msg_hangle_(vector<string> &command)//int com_num,string *command)
{
	if (command[0] == "dump")
	{
		unsigned long cmd1 = strtoul (command[1].c_str(),NULL,0);//start address
		unsigned long cmd2 = strtoul (command[2].c_str(),NULL,0);//end address
		return memRW::dumpMem(this->pid,cmd1,cmd2,command[3]);//dump to file path
	}else if (command[0] == "pids") {
		if(pid_tools::getpids())
		{
			this->pid_ret = pid_tools::ret;
			return true;
		}
		return false;	
	}else if (command[0] == "sm") {
		int typee = string_o_types::stoi(command[1]);
		switch(typee)
		{
			case SHORT: 
			case INT: {
				int si = string_o_types::stoi(command[2]);
				void* sii = &si;
				if(!get_maps_structs())
					return false;
				set_search_struct(sii, INT);
				return search_mem();
				//break;
			}
			case U_INT: {
				int sui = string_o_types::stoui(command[2]);
				void* suii = &sui;
				if(!get_maps_structs())
					return false;
				set_search_struct(suii, U_INT);
				return search_mem();
				//break;
			}
			case LONG: {
				long sl = string_o_types::stol(command[2]);
				void *sli = &sl;
				if(!get_maps_structs())
					return false;
				set_search_struct(sli, LONG);
				return search_mem();
				//break;
			}
			case U_LONG: {
				unsigned long sul = strtoul(command[2].c_str(),NULL,0);
				void * suli = &sul;
				if(!get_maps_structs())
					return false;
				set_search_struct(suli, U_LONG);
				return search_mem();
				//break;
			}
			case DOUBLE: {
				double sd = string_o_types::stod(command[2]);
				void * sdi = &sd;
				if(!get_maps_structs())
					return false;
				set_search_struct(sdi, DOUBLE);
				return search_mem();
				//break;
			}
			case BYTE: 
				break;
			case CHAR: {
				void* cmdd = &command[2];
				if(!get_maps_structs())
					return false;
				set_search_struct(cmdd, CHAR);
				return search_mem();
				//break;
			}
			default: 
				//printf("wrong type"); 
				return false;
		}
	}else if (command[0] == "mm") {
		int typee = string_o_types::stoi(command[2]);
		unsigned long cmd1 = strtoul (command[1].c_str(),NULL,0);//start address
		switch(typee)
		{
			case SHORT: 
			case INT: {
				int si = string_o_types::stoi(command[3]);
				void* sii = &si;
				return memopt::memWT(pid, cmd1, sii, typee);
				//break;
			}
			case U_INT: {
				int sui = string_o_types::stoui(command[3]);
				void* suii = &sui;
				return memopt::memWT(pid, cmd1, suii, typee);
				//break;
			}
			case LONG: {
				long sl = string_o_types::stol(command[3]);
				void *sli = &sl;
				return memopt::memWT(pid, cmd1, sli, typee);
				//break;
			}
			case U_LONG: {
				unsigned long sul = strtoul(command[3].c_str(),NULL,0);
				void * suli = &sul;
				return memopt::memWT(pid, cmd1, suli, typee);
				//break;
			}
			case DOUBLE: {
				double sd = string_o_types::stod(command[3]);
				void * sdi = &sd;
				return memopt::memWT(pid, cmd1, sdi, typee);
				//break;
			}
			case BYTE: 
				break;
			case CHAR: {
				void* cmdd = &command[2];
				return memopt::memWT(pid, cmd1, cmdd, typee);
				//break;
			}
			default: 
				printf("wrong type"); 
				return false;
		}
	}else if (command[0] == "maps") {
		return maps();
	}else if (command[0] == "gitpidbyname")
	{
		return pid_tools::getPidByName(command[1]);
	}
	
	return false;
}




/*
int main()
{ 
	msg_handle m = msg_handle();
	m.set_pid(1);
	//string com = "maps";
	//string* c = &com; 
	//m.msg_hangle_(1,c);
	//cout<<m.maps_ret;
	
	//string com = "pids";
	//string* c = &com; 
	//m.msg_hangle_(1,c);
	//string cc[4] = {"dump","0x7f06e67c7000","0x7f06e67c8000","/home/andro/1.txt"};
	//m.msg_hangle_(4,cc);
	//cout<<m.pid_ret;
	
	string cc[4] = {"sm","5","12.9986"};
	string ca[4] = {"mm","0x7f06e67c8089","5","12.99898786"};
	m.msg_hangle_(4,ca);
	m.msg_hangle_(4,cc);
	for (vector<long>::iterator iter = m.ret_addr.begin(); iter!= m.ret_addr.end(); iter++)
	{
		printf("%lx  ",*iter);
	}
	return 0;
}

*/
