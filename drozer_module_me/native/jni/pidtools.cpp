#include "pidtools.h"
std::string pid_tools::ret = "";
void pid_tools::getPidByName(char *task_name)
{
	DIR *dir;
    struct dirent *ptr;
    FILE *fp;
    char filepath[50];//大小随意，能装下cmdline文件的路径即可
    char cur_task_name[50];//大小随意，能装下要识别的命令行文本即可
    char buf[BUF_SIZE];
    dir = opendir("/proc"); //打开路径
    if (NULL != dir)
    {
        while ((ptr = readdir(dir)) != NULL) //循环读取路径下的每一个文件/文件夹
        {
            //如果读取到的是"."或者".."则跳过，读取到的不是文件夹名字也跳过
            if ((strcmp(ptr->d_name, ".") == 0) || (strcmp(ptr->d_name, "..") == 0))
				continue;
            if (DT_DIR != ptr->d_type)
				continue;
            sprintf(filepath, "/proc/%s/status", ptr->d_name);//生成要读取的文件的路径

			//printf("filepath:%s\n",filepath);

            fp = fopen(filepath, "r");//打开文件
            if (NULL != fp)
            {
				//printf("esrgwser2\n");

                if( fgets(buf, BUF_SIZE-1, fp) != NULL ){
					fclose(fp);
					sscanf(buf, "%*s %s", cur_task_name);
					if (!strcmp(task_name, cur_task_name)){
						printf("cur_task_name:%s  PID:  %s\n", cur_task_name, ptr->d_name);
					}
				}else{
					printf("%s\n",ptr->d_name);
					fclose(fp);
				}
			}
        }
        closedir(dir);//关闭路径
    }
}

void pid_tools::getNameByPid(pid_t pid) 
{
	char *task_name;
    char proc_pid_path[BUF_SIZE];
    char buf[BUF_SIZE];
    task_name = (char*)malloc(sizeof(char)*50);
    sprintf(proc_pid_path, "/proc/%d/status", pid);
    FILE* fp = fopen(proc_pid_path, "r");
    if(NULL != fp){
        if( fgets(buf, BUF_SIZE-1, fp)== NULL){
            fclose(fp);
        }
        fclose(fp);
        sscanf(buf, "%*s %s", task_name);
    }
    std::string ret = task_name;
    pid_tools::ret = ret;
    free(task_name);
}

bool pid_tools::getpids()
{
	std::string ret = "";
	char *rett = (char *)malloc(sizeof(char)*300);
	DIR *dir;
    struct dirent *ptr;
    FILE *fp;
    char filepath[50];//大小随意，能装下cmdline文件的路径即可
    char cur_task_name[50];//大小随意，能装下要识别的命令行文本即可
    char buf[BUF_SIZE];
    dir = opendir("/proc"); //打开路径
    if (NULL != dir)
    {
        while ((ptr = readdir(dir)) != NULL) //循环读取路径下的每一个文件/文件夹
        {
            //如果读取到的是"."或者".."则跳过，读取到的不是文件夹名字也跳过
            if ((strcmp(ptr->d_name, ".") == 0) || (strcmp(ptr->d_name, "..") == 0))
				continue;
            if (DT_DIR != ptr->d_type)
				continue;
            sprintf(filepath, "/proc/%s/status", ptr->d_name);//生成要读取的文件的路径

			//printf("filepath:%s\n",filepath);

            fp = fopen(filepath, "r");//打开文件
            if (NULL != fp)
            {
				//printf("esrgwser2\n");

                if( fgets(buf, BUF_SIZE-1, fp) != NULL ){
					fclose(fp);
					sscanf(buf, "%*s %s", cur_task_name);
					sprintf(rett, "process_name:%-20s  pid:%-25s\n", cur_task_name, ptr->d_name);
					ret += rett;
				}else{
					//printf("%s\n",ptr->d_name);
					fclose(fp);
				}
			}
        }
        closedir(dir);//关闭路径
    }
    free(rett);
    //printf("ret:%s",ret);
    if(ret == "")
		return false;
    pid_tools::ret = ret ;
    return true;
}
void pid_tools::getPidByName(std::string task_name)
{
	char *data;
	int len = task_name.length();
	data = (char *)malloc((len+1)*sizeof(char));
	task_name.copy(data,len,0);
	pid_tools::getPidByName(data);
	free(data);
}

/*
int main(int argc, char** argv)
{
    pid_t pid = getpid();
    printf("pid of this process:%d\n", pid);
    //pid_tools::getpids();
    std::cout<<pid_tools::ret;
    std::string s = "bash";
    pid_tools::getPidByName(s);
    std::cout<<pid_tools::ret;

    pid_tools::getNameByPid(1);
    std::cout<<pid_tools::ret;
	return 0;
}
*/

