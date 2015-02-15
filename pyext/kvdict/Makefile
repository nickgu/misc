
VERSION = 1.1.0
CPPFLAGS =  -D__VERSION_ID__="\"$(VERSION)\"" -g -Wall -O0 -fPIC  -pipe -D_REENTRANT -DLINUX -Wall

ULLIB=./lib/ullib
DICT=./lib/dict

TARGET=c_kvdict.so
INCLUDES = -I$(ULLIB)/include \
		   -I$(DICT)/include \
		  
LIBS = -L$(DICT)/lib -luldict \
	   -L$(ULLIB)/lib -lullib \
	   -lcrypto \
	   -lpthread

all: clean $(TARGET)
	@echo 'MAKE: ALL'
	mkdir output
	cp *.py $(TARGET) output

c_kvdict.so: c_kvdict.cpp
	@echo 'MAKE: KVDICT'
	g++ -shared -fpic $^ -o $@ $(LIBS) $(CPPFLAGS) $(INCLUDES) 

clean:
	rm -rf *.o *~ $(TARGET)
	rm -rf output





