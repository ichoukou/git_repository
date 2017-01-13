#include "memopt_b.h"

bool memRW::getdata(pid_t child,  long addr, byte *str, int len)  
{ 
    byte *laddr;  
    int i, j;  
    union u {  
            long val;  
            byte chars[long_size];  
    }data;  
    data.val = 1000;
  
    i = 0;  
    j = len / long_size;  
    laddr = str; 
    
    errno = 0; //errno reset to valid ,to record the ptrace ret status.
    while(i < j) {
        data.val = ptrace(PTRACE_PEEKDATA, child, (void*)(addr + i * long_size), NULL); 
		if(errno){ 
			//printf("erron:%d\n",errno);
			//printf("%lx \n",data.val);
			perror("ptrace");
			return false;
		} 
        memcpy(laddr, data.chars, long_size);  
        ++i;  
        laddr += long_size;  
    }  
    j = len % long_size;  
    if(j != 0) {  
        data.val = ptrace(PTRACE_PEEKDATA, child, (void*)(addr + i * long_size), NULL); 
		if(errno){
			perror("ptrace");
			return false;
		}
		//printf("%lx \n",data.val);
        memcpy(laddr, data.chars, j);  
    }  
    str[len] = '\0';  
    return true;
}  
  
bool memRW::putdata(pid_t child, long addr, byte *str, int len)  
{     
    byte *laddr;  
    int i, j; 
	int ptrce_ret; 
    union u {  
            long val;  
            byte chars[long_size];  
    }data;  
  
    i = 0;  
    j = len / long_size;  
    laddr = str;  
    while(i < j) {  
        memcpy(data.chars, laddr, long_size);  
        ptrce_ret = ptrace(PTRACE_POKEDATA, child, (void*)(addr + i * long_size), (void*)data.val); 
		if(ptrce_ret == -1){ 
			perror("ptrace");
			return false;
		}
        ++i;  
        laddr += long_size;  
    }  
    j = len % long_size;  
    if(j != 0) {  
        memcpy(data.chars, laddr, j);  
        ptrce_ret = ptrace(PTRACE_POKEDATA, child,  (void*)(addr + i * long_size), (void*)data.val);  
		if(ptrce_ret == -1){ 
			perror("ptrace");
			return false;
		}
    }  
    return true;
}  

bool memRW::dataW(pid_t pid, long addr,byte *data,int len)
{
	int ptrace_ret; 
	int i;	
	ptrace_ret = ptrace(PTRACE_ATTACH, pid, NULL, NULL);  
	if (ptrace_ret == -1) {
		fprintf(stderr, "error: ptrace attach failed.\n");
		perror("ptrace");
		return false;
	}

	if (waitpid(pid, NULL, 0) == -1) {
		fprintf(stderr, "error: waitpid failed.\n");
		perror("waitpid");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		return false;
	}
	/*
	byte backup[16];
	getdata(pid, addr, backup, 16);
	for(i = 0; i<typemode; i++){
		backup[i] = data[i];
	} 
	*/
	
	if(!putdata(pid, addr, data, len))
	    return false; 
	ptrace(PTRACE_DETACH, pid, NULL, NULL); 
	return true;
}

bool memRW::dataR(pid_t pid, long addr,byte *data,int len){
	int ptrace_ret; 
	ptrace_ret = ptrace(PTRACE_ATTACH, pid, NULL, NULL);  
	if (ptrace_ret == -1) {
		fprintf(stderr, "error: ptrace attach failed.\n");
		perror("ptrace");
		return false;
	}

	if (waitpid(pid, NULL, 0) == -1) {
		fprintf(stderr, "error: waitpid failed.\n");
		perror("waitpid");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		return false;
	}
	if(!getdata(pid, addr, data, len))
		return false;
	ptrace(PTRACE_DETACH, pid, NULL, NULL);
	return true;
}


bool memRW::dumpMem(pid_t pid,unsigned long start_addr,unsigned long end_addr,std::string filename)
{
	unsigned long len = end_addr - start_addr;
	// printf("end:%ld\n",end_addr);
	// printf("start%ld\n",start_addr);
	// printf("len:%ld\n",len);
	int ptrace_ret;
	ptrace_ret = ptrace(PTRACE_ATTACH, pid, NULL, NULL);
	if (ptrace_ret == -1) {
		fprintf(stderr, "error: ptrace attach failed.\n");
		perror("ptrace");
		return false;
	}
	if (waitpid(pid, NULL, 0) == -1) {
		fprintf(stderr, "error: waitpid failed.\n");
		perror("waitpid");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		return false;
	}

	
	/*open /proc/<pid>/mem to attach the memory*/
	int fd;
	char path[256] = {0};
	sprintf(path, "/proc/%d/mem", pid);


	fd = open(path, O_RDONLY);
	if (fd == -1) {
		fprintf(stderr, "error:open file failed.\n");
		perror("open");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		return false;
	}
	

	off_t off;
	off = lseek(fd, start_addr, SEEK_SET);
	if (off == (off_t)-1) {
		fprintf(stderr, "error: lseek failed.\n");
		perror("lseek");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		close(fd);
		return false;
	}
	

	unsigned char *buf = (unsigned char *)malloc(len);
	if (buf == NULL) {
		fprintf(stderr, "error: malloc failed.\n");
		perror("malloc");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		close(fd);
		return false;
	}


	int rd_sz;
	rd_sz = read(fd, buf, len);
	if (rd_sz < len) {
		fprintf(stderr, "error: read failed.\n");
		perror("read");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		free(buf);
		close(fd);
		return false;
	}
	

	int i = 0;
	//printf("filename:%s\n",filename.c_str());
	FILE *fp = fopen(filename.c_str(), "wb+");
	if (fp == NULL) {
		fprintf(stderr, "fopen failed.\n");
		perror("fopen");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		free(buf);
		close(fd);
		return false;
	}
	fwrite(buf, 1, len, fp);
	fclose(fp);
	
	ptrace(PTRACE_DETACH, pid, NULL, NULL);
	free(buf);
	close(fd);
	return true;
}


int	memRW::findBt(byte *bt, long btLen, byte *search, int seaLen, vector<long> &addr){
	int i,j;
	int searchf = 0;	
	for(i = 0; i < btLen; i++)
	{
		//printf("%x ",bt[i]);
		for(j = 0; j < seaLen; j++)
		{
			//printf("%x ",search[j]);
			if(bt[i+j] == search[j])
				searchf += 1;
		}
		if(searchf == seaLen)
		{
			addr.push_back(i);
		}
		searchf = 0;
	}
	return 0;
}


/*	
int readfileBt(char *filename, byte *bt, long btLen){
	FILE *fp;  
	if((fp=fopen(filename,"r"))==NULL)
	{  
		printf("File cannot be opened/n");  
		exit(-1);
	}
	fread(bt,1,btLen,fp); 
	fclose(fp);
	return 0; 
}
*/

/*

int main()
{
	byte b[3] = {0x12,0x4C,0xF};
	byte *a = b;
	byte *aa = (byte*)malloc(sizeof(byte)*16);

	memRW::dataR(1,0x7f0548a08000,aa,16);
	memRW::dumpMem(1,0x7f0548a08000,0x7f0548a08016,"/home/andro/1.txt");
	for(int i = 0; i<16; i++)
		printf("%x ",*(aa+i));
	printf("\n");
	
	memRW::dataW(1,0x7f0548a08003,a,3);
	memRW::dataR(1,0x7f0548a08000,aa,16);
	memRW::dumpMem(1,0x7f0548a08000,0x7f0548a08016,"/home/andro/2.txt");
	for(int i = 0; i<16; i++)
		printf("%x ",*(aa+i));
	printf("\n");
}

*/
