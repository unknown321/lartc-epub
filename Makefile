html.tar.gz:
	wget https://www.lartc.org/html.tar.gz

howto: html.tar.gz
	tar xf html.tar.gz

clean:
	rm -rf *.tar.gz howto/ *.epub

run: howto
	./run.py

.DEFAULT_GOAL:=run
