
apr-skeleton: apr-skeleton.c 
	gcc apr-skeleton.c -o apr-skeleton -I/usr/local/apr/include/ -L/usr/local/apr/lib -lapr-1 `pkg-config apr-1 --cflags` /home/serhat/Desktop/OpenSSL_stable/openssl-1.0.1f/libssl.a /home/serhat/Desktop/OpenSSL_stable/openssl-1.0.1f/libcrypto.a -ldl 

ab: ab.c ap_release.h
	gcc ab.c ap_release.h -o ab -I/usr/local/apr/include/ -L/usr/local/apr/lib -lapr-1 `pkg-config apr-1 --cflags` -laprutil-1 -lm /home/serhat/Desktop/OpenSSL_stable/openssl-1.0.1f/libssl.a /home/serhat/Desktop/OpenSSL_stable/openssl-1.0.1f/libcrypto.a -ldl



clean:
	rm ab apr-skeleton

