set GOOS=linux
go build -o ./releases_latest/scheduller_linux_amd64 ./*.go
go build -buildmode=c-shared -o ./releases_latest/_scheduller_linux_amd64.so ./*.go

set GOOS=windows
go build -o ./releases_latest/scheduller_windows_amd64.exe ./*.go
go build -buildmode=c-shared -o ./releases_latest/_scheduller_windows_amd64.dll ./*.go

set GOOS=darwin
go build -o ./releases_latest/scheduller_darwin_amd64 ./*.go
go build -buildmode=c-shared -o ./releases_latest/_scheduller_darwin_amd64.so ./*.go