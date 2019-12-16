# pysm3
sm3 算法，调用C语言接口



## 编译 sm3
- linux
`gcc -fPIC -shared -o libsm3.so sm3.c`

- windows
`gcc -fPIC -shared -o libsm3.dll sm3.c`
使用 msys64 版本的 mingw64 的 gcc 编译

## 注意

当前已编译的 libsm3.dll libsm3.so 适用于 64 位 python 平台