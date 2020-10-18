FROM python:3
COPY ./ app/
RUN apt update && apt install -y tesseract-ocr && pip install pytesseract && pip3 install opencv-python
ENTRYPOINT ["python3", "/app/imageToNumber.py"]
