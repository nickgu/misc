
VERSION = 1.1.0
CPPFLAGS =  -D__VERSION_ID__="\"$(VERSION)\"" -g -Wall -O3 -fPIC  -pipe -D_REENTRANT -DLINUX -Wall

TARGET=c_prod.so
INCLUDES=
		  
LIBS = -lcrypto \
	   -lpthread

all: clean $(TARGET)
	@echo 'MAKE: ALL'
	mkdir output
	cp *.py $(TARGET) output

c_prod.so: c_prod.cc
	@echo 'MAKE: PROD'
	g++ -shared -fpic $^ -o $@ $(LIBS) $(CPPFLAGS) $(INCLUDES) 

clean:
	rm -rf core* *.o *.so *~ $(TARGET)
	rm -rf output

test: clean
	make c_prod.so
	python test_prod.py < item.txt





