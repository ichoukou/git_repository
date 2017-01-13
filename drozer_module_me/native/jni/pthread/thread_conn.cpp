#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>


void *thread_function(void *arg);
char message[] = "Hello word!";

int  main()
{
	int res;
	pthread_t a_thread;
	void *thread_result;
	
	res = pthread_create(&a_thread, NULL, thread_function, (void*)message);
	if (res != 0)
	{
		perror("thread create failed!");
		exit(EXIT_SUCCESS);
	}
	printf("waiting for thread to finish...\n");
	res = pthread_join(a_thread, &thread_result);
	printf("hahaha~~~");
	if (res != 0)
	{
		perror("thread join failed");
		exit(EXIT_SUCCESS);
	}
	printf("over\n");
	exit(EXIT_SUCCESS);
}

void *thread_function(void *arg)
{
	int a;
	printf("rgsrettsrhsth");
	scanf("%d",&a);
}
