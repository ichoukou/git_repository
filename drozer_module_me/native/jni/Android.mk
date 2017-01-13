LOCAL_PATH:= $(call my-dir)

include $(CLEAR_VARS)
LOCAL_SRC_FILES:= native.cpp msg_handle.cpp pidtools.cpp memopt.cpp memopt_b.cpp tools.cpp   ./socket/jni/ServerSocket.cpp ./socket/jni/Socket.cpp
LOCAL_MODULE:= native

LOCAL_FORCE_STATIC_EXECUTABLE := true
#LOCAL_STATIC_LIBRARIES := libc
#LOCAL_CFLAGS += -Iinclude/dir -DSOMEFLAGS

include $(BUILD_EXECUTABLE)
