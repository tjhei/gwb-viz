git clone https://github.com/GeodynamicWorldBuilder/WorldBuilder
git clone https://github.com/GeodynamicWorldBuilder/ModelCollection


cd WorldBuilder
rm -rf build
mkdir build
cd build
cmake -G Ninja ..
ninja
