# brew install FiloSottile/musl-cross/musl-cross
# brew install mingw-w64

echo "Building..."
echo "=========================="

echo "Building for Darwin (MacOS/amd64)..."
CGO_ENABLED=1 GOOS=darwin go build -o ./releases_latest/scheduller_darwin_amd64 ./*.go
CGO_ENABLED=1 GOOS=darwin go build -buildmode=c-shared -o ./releases_latest/_scheduller_darwin_amd64.so ./*.go
md5 ./releases_latest/scheduller_darwin_amd64
md5 ./releases_latest/_scheduller_darwin_amd64.so

echo "=========================="

echo "Building for Linux (Linux/amd64)..."
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC=x86_64-linux-musl-gcc  CXX=x86_64-linux-musl-g++ go build -o ./releases_latest/scheduller_linux_amd64 ./*.go
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC=x86_64-linux-musl-gcc  CXX=x86_64-linux-musl-g++ go build -buildmode=c-shared -o ./releases_latest/_scheduller_linux_amd64.so ./*.go
md5 ./releases_latest/scheduller_linux_amd64
md5 ./releases_latest/_scheduller_linux_amd64.so

echo "=========================="

echo "Building for Windows (Windows/amd64)..."
CGO_ENABLED=1 GOOS=windows GOARCH=386 CC=i686-w64-mingw32-gcc go build -o ./releases_latest/scheduller_windows_amd64.exe ./*.go
CGO_ENABLED=1 GOOS=windows GOARCH=386 CC=i686-w64-mingw32-gcc go build -buildmode=c-shared -o ./releases_latest/_scheduller_windows_amd64.dll ./*.go
md5 ./releases_latest/scheduller_windows_amd64.exe
md5 ./releases_latest/_scheduller_windows_amd64.dll

echo "=========================="
echo "Finished."
