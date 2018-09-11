# A simple, yet usable makefile
CLASS_NAME = DivideBigInt

all: $(CLASS_NAME).class

run: $(CLASS_NAME).class
	java $(CLASS_NAME)

$(CLASS_NAME).class: $(CLASS_NAME).java
	javac $(CLASS_NAME).java

clean:
	rm -f $(CLASS_NAME).class