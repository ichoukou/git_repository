#include "memopt.h"
int memopt::memWT(pid_t pid, long addr, void *a, int types)
{  
	switch(types)
	{
        case INT: 
			return memRW::dataW(pid,addr,(byte *)a,int_size);
			//break;
        case U_INT: 
			return memRW::dataW(pid,addr,(byte *)a,int_size); 
			//break;
        case LONG:
			return memRW::dataW(pid,addr,(byte *)a,long_size);
			//break;
        case U_LONG: 
			return memRW::dataW(pid,addr,(byte *)a,long_size); 
			//break;
        case DOUBLE: 
			//printf("%8x",*(byte *)a);
			return memRW::dataW(pid,addr,(byte *)a,double_size);
			//break;
        case SHORT: 
			return memRW::dataW(pid,addr,(byte *)a,short_size); 
			//break;
		case BYTE: 
			return memRW::dataW(pid,addr,(byte *)a,1); 
			//break;
		case CHAR: 
			return memRW::dataW(pid,addr,(byte *)a,1); 
			//break;
        default: printf("wrong!"); return false;
    }
    return false;
}


int memopt::memWString(pid_t pid, long addr, void *a, int len)
{ 
	memRW::dataW(pid, addr, (byte*)a, len);
	return 0;
}


int memopt::findT(byte *bt, long btLen, void *a, int types, vector<long> &addr){ 
	switch(types){
        case INT: 	
			memRW::findBt(bt, btLen, (byte *)a, int_size, addr); 
			break;
        case U_INT: 
			memRW::findBt(bt, btLen, (byte *)a, int_size, addr); 
			break;
        case LONG:  
			memRW::findBt(bt, btLen, (byte *)a, long_size, addr); 
			break;
        case U_LONG: 
			memRW::findBt(bt, btLen, (byte *)a, long_size, addr); 
			break;
        case DOUBLE: 
			memRW::findBt(bt, btLen, (byte *)a, double_size, addr); 
			break;
        case SHORT: 
			memRW::findBt(bt, btLen, (byte *)a, short_size, addr); 
			break;
		case BYTE: 
			memRW::findBt(bt, btLen, (byte *)a, 1, addr); 
			break;
		case CHAR: 
			memRW::findBt(bt, btLen, (byte *)a, 1, addr); 
			break;
        default: 
			printf("find type wrong!"); return -1;
    }
    return 0;
}


int memopt::memfind(pid_t pid, vector<long> &addr,  vector<long> &retaddr, void *a, int types){ 
	/*
	byte *retbytes ;
	int i = 0;
	int fi = 0;
	vector<unsigned long>::size_type ix;
	retbytes = (byte*)malloc(128);
	for(ix = 0; ix != addr.size(); ix++)
	{
		i = 0;
		fi = 0;
		switch(types){
			case INT: 
			case U_INT: 
				dataR(pid, addr[ix],retbytes,int_size);
				for(i = 0; i<int_size; i++){
					if(retbytes[i] == ((byte*)a)[i])	
						fi += 1;	
				}
				if(fi == int_size)
					retaddr.push_back(addr[ix]);
				break;
			case LONG:  
			case U_LONG: 
				dataR(pid, addr[ix],retbytes,long_size);
				for(i = 0; i<long_size; i++){
					if(retbytes[i] == ((byte*)a)[i])	
					fi += 1;	
				}
				if(fi == long_size)
					retaddr.push_back(addr[ix]);
				break;
			case DOUBLE: 
				dataR(pid, addr[ix],retbytes,double_size);
				for(i = 0; i<double_size; i++){
					if(retbytes[i] == ((byte*)a)[i])	
					fi += 1;	
				}
				if(fi == double_size)
					retaddr.push_back(addr[ix]);
				break;
			case SHORT: 
				dataR(pid, addr[ix],retbytes,short_size);
				for(i = 0; i<short_size; i++){
					if(retbytes[i] == ((byte*)a)[i])	
					fi += 1;	
				}
				if(fi == short_size)
					retaddr.push_back(addr[ix]);
				break;
			case BYTE: 
			case CHAR:
				//printf("addr[ix]:%lx ",addr[ix]);
				dataR(pid, addr[ix],retbytes,1);
				//printf("%0x ",((byte*)a)[0]);
				if(retbytes[0] == ((byte*)a)[0])	
					fi += 1;	
				if(fi == 1)
					retaddr.push_back(addr[ix]);
				break;
			default: 
				printf("wrong!"); return -1;
		}
		free(retbytes);
		
	}
	*/
    return 0;
}


int memopt::findString(byte *bt, long btLen, void *a, int len, vector<long> &addr){
	memRW::findBt(bt, btLen, (byte*)a, len, addr);
}

/*
int main(int argc, char *argv[])  
{     
	byte a[4] = {0x12,0x4C,0xF,0x00};
	byte *aa = (byte*)malloc(sizeof(byte)*1024);
	vector<long> addr;
	
    memopt::memWT(1,0x7f0548a08005,a,INT);
    memRW::dataR(1,0x7f0548a08000, aa, 1024);
	memopt::findString(aa,1024,a,4,addr);   
	
	for(int i = 0; i<addr.size(); i++){
		printf("%2hx ",addr[i]);
	}
} 
*/




/*
int main()
{
	byte b[3] = {0x12,0x4C,0xF};
	byte *a = b;
	byte *aa = (byte*)malloc(sizeof(byte)*16);

	memopt::memWT(1,0x7f0548a08000,b,8);
	memRW::dataR(1,0x7f0548a08000,aa,1);
	//for(int i = 0; i<16; i++)
	printf("%x ",*aa);
	//printf("\n");
	return 0;
*/
