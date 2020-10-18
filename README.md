# IntelIDReg
- to run only Python file: `python imageToNumber.py -folder [folder_name] -filename [filename]`
- to build Docker:
* 1. Run `sudo docker build -t [Docker's name]` within this folder and wait until it finishes building.
* 2. Inference the docker: `docker run intel-idreg --folder /app/ --filename Test_0_20200602_045411_2_1.jpg`
 
