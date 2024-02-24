P=$pwd
cd $P/WorldBuilder; git pull
cd $P/ModelCollection; git pull

export PATH=WorldBuilder/build/bin;$PATH

python makeall.py
