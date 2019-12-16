# pysm3
sm3 算法，调用C语言接口


# 编译 sm3
- linux
`gcc -fPIC -shared -o libsm3.so sm3.c`

- windows
`gcc -fPIC -shared -o libsm3.dll sm3.c`
使用 msys64 版本的 mingw64 的 gcc 编译