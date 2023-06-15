
def start_preview():
    picam2.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1))
    picam2.start()

def stop_preview():
    picam2.stop_preview()
    picam2.stop()
