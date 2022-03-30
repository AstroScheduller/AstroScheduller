# brew install FiloSottile/musl-cross/musl-cross
# brew install mingw-w64

GOOS=darwin go build -o ./releases_latest/scheduller_darwin_amd64 ./*.go
GOOS=darwin go build -buildmode=c-shared -o ./releases_latest/_scheduller_darwin_amd64.so ./*.go
echo "Build success - Darwin"
md5 ./releases_latest/scheduller_darwin_amd64

CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC=x86_64-linux-musl-gcc  CXX=x86_64-linux-musl-g++ go build -o ./releases_latest/scheduller_linux_amd64 ./*.go
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC=x86_64-linux-musl-gcc  CXX=x86_64-linux-musl-g++ go build -buildmode=c-shared -o ./releases_latest/_scheduller_linux_amd64.so ./*.go
echo "Build success - Linux"
md5 ./releases_latest/scheduller_linux_amd64

CGO_ENABLED=1 GOOS=windows GOARCH=386 CC=i686-w64-mingw32-gcc go build -o ./releases_latest/scheduller_windows_amd64.exe ./*.go
CGO_ENABLED=1 GOOS=windows GOARCH=386 CC=i686-w64-mingw32-gcc go build -buildmode=c-shared -o ./releases_latest/_scheduller_windows_amd64.dll ./*.go
echo "Build success - Windows"
md5 ./releases_latest/scheduller_windows_amd64.exe
