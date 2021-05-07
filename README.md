### 環境構築方法
rasbianの環境前提です。

まず本体をインストールします。
```
apt-get install opencv-python
git clone https://github.com/koty/too_close_checker.git
cd too_close_checker.git
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

次にkinectを操作するためのAPIをインストールします。本体のインストールとどちらを先に行っても良いですが、同じ仮想環境に入れたいので後に作業します。
```
cd ~
git clone https://github.com/OpenKinect/libfreenect.git
cd libfreenect
mkdir build
cd build
cmake -L ..
make
sudo make install
cd ~/libfreenect/wrappers/python
python3 setup.py install
```

起動方法
```
cd too_close_checker
export CHROMECAST_NAME=2階リビング
export DIRECTION_MP3_URL=http://example.com/angry.mp3
python3 main.py
```
