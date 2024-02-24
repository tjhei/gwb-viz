P=$PWD
cd $P/WorldBuilder; git pull
cd $P/ModelCollection; git pull
cd $P

export PATH=$P/WorldBuilder/build/bin:${PATH}

python makeall.py
