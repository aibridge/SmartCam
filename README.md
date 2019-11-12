# Smart Camera
## Main Section
1. Run the following after cd to this dir: pip install -r requirements.txt
2. Run init.sh and change folder names accoarding to comments on init.sh file
3. Copy and replace contents of REPLACE folder into this folder
4. Put your image with the name 'test.jpg' in the input folder
5. Download vgg weights from:
   https://mega.nz/#!YU1FWJrA!O1ywiCS2IiOlUCtCpI6HTJOMrneN-Qdv3ywQP5poecM
   and copy it in ./colorize/vgg
6. Download:
   https://github.com/Armour/Automatic-Image-Colorization/releases/download/2.0/pre_trained.zip
   and extract in ./colorize 
7. Download:
   https://drive.google.com/drive/folders/1FPELQupnGR750EoUWTY_0owkEnlAGVYH
   and extract into ./enhance/checkpoints
8. Download 'RRDV_ESRGAN_x4.pth':
   https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY
   and extract into ./super/models
9. To generate the image run the 'main.py' file. Use '-h' to get help.

Note: Remember that the code can be run under linux os and 'git bash' or with MINGW in windows os.

## Not Integerated Yet
### Face Swapping
1. Download "shape_predictor_68_face_landmarks.dat" from "https://github.com/AKSHAYUBHAT/TensorFace/tree/master/openface/models/dlib"
2. Run "pip install -r Requirements.txt" from current directory.
3. Run "photos_face_swapping.py"
### PGAN
1. In "PGAN/parsing_network" run "pip install -r requirements.txt"
2. Get model from [link](https://jbox.sjtu.edu.cn/l/hJjgjw) and extract in "PGAN/parsing_network"
3. Put the image in "PGAN/parsing_network" folder with name "1.jpg"
4. Run "PGAN/parsing_network/inference.py"