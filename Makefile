KEPUBIFY_VERSION=v4.0.4
KEPUBIFY_SHA256=37d7628d26c5c906f607f24b36f781f306075e7073a6fe7820a751bb60431fc5

kepubify:
	wget https://github.com/pgaskin/kepubify/releases/download/$(KEPUBIFY_VERSION)/kepubify-linux-64bit
	echo -n "$(KEPUBIFY_SHA256) kepubify-linux-64bit" | sha256sum -c -
	chmod +x kepubify-linux-64bit

html.tar.gz:
	wget https://www.lartc.org/html.tar.gz

howto: html.tar.gz
	tar xf html.tar.gz

clean:
	rm -rf *.tar.gz howto/ *.epub

run: howto
	./run.py
	./kepubify-linux-64bit --no-add-dummy-titlepage -i *.epub

.DEFAULT_GOAL:=run
