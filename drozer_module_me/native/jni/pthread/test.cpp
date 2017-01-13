#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>

void *thread_function(void *arg);

char message[] = "Hello Word";
int thread_finished = 0;

int main() 
{
	int res;
	pthread_t a_thread;
	
	pthread_attr_t thread_attr;
	
	res = pthread_attr_init(&thread_attr);
	res = pthread_attr_setdetachstate(&thread_attr, PTHREAD_CREATE_DETACHED);
	res = pthread_create(&a_thread, &thread_attr, thread_function, (void*)message);
	(void)pthread_attr_destroy(&thread_attr);
	printf("sgsg\n");
	while(!thread_finished)
	{
		printf("sh\n");
		sleep(1);
	}
	exit(EXIT_SUCCESS);
}

void *thread_function(void *arg)
{
	printf("l\n");
	thread_finished = 1;
	pthread_exit(NULL);
}
