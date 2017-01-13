LOCAL_PATH:= $(call my-dir)

include $(CLEAR_VARS)
LOCAL_SRC_FILES:= Socket.cpp ClientSocket.cpp Client_main.cpp
LOCAL_MODULE:= client

LOCAL_FORCE_STATIC_EXECUTABLE := true
#LOCAL_STATIC_LIBRARIES := libc
#LOCAL_CFLAGS += -Iinclude/dir -DSOMEFLAGS

include $(BUILD_EXECUTABLE)
