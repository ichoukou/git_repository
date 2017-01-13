native: native.cpp msg_handle.cpp pidtools.cpp memopt.cpp memopt_b.cpp tools.cpp   ./socket/jni/ServerSocket.cpp ./socket/jni/Socket.cpp
	g++ native.cpp msg_handle.cpp pidtools.cpp memopt.cpp memopt_b.cpp tools.cpp  ./socket/jni/ServerSocket.cpp ./socket/jni/Socket.cpp -o native
