GOOS=linux
go build -o ./releases_latest/scheduller_linux_amd64 ./*.go
go build -buildmode=c-shared -o ./releases_latest/_scheduller_linux_amd64.so ./*.go
echo "Build success - Linux"
md5 ./releases_latest/scheduller_linux_amd64

GOOS=windows
go build -o ./releases_latest/scheduller_windows_amd64.exe ./*.go
go build -buildmode=c-shared -o ./releases_latest/_scheduller_windows_amd64.dll ./*.go
echo "Build success - Windows"
md5 ./releases_latest/scheduller_windows_amd64.exe

GOOS=darwin
go build -o ./releases_latest/scheduller_darwin_amd64 ./*.go
go build -buildmode=c-shared -o ./releases_latest/_scheduller_darwin_amd64.so ./*.go
echo "Build success - Darwin"
md5 ./releases_latest/scheduller_darwin_amd64