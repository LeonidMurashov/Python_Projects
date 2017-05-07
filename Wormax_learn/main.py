import cv2
import win32api, win32con
import numpy as np
from grabscreen import grab_screen
import time
from getkeys import key_check
from alexnet import alexnet
from CV_helpfile import bit_mask
from screen_consts import GRAB_REGION, WIDTH, HEIGHT, max_x, max_y, min_x, min_y, ROI_VERTICES, roi, cx, cy, kx, ky


def mouse_down(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)

def mouse_up(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

LR = 1e-3
EPOCHS = 20
MODEL_NAME = 'models/wormax-binary-worm8-0.005-alexnetv2-20-epochs-178K-data.model'

model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

print()
#with tf.device('/cpu:1'):
print("Tests prediction: ", model.predict(np.random.randint(100, size=[1, WIDTH, HEIGHT, 1])))
print("Tests prediction: ", model.predict(np.random.randint(100, size=[1, WIDTH, HEIGHT, 1])))
print("Tests prediction: ", model.predict(np.random.randint(100, size=[1, WIDTH, HEIGHT, 1])))


def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while (True):

        if not paused:
            # 800x600 windowed mode
            # screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
            img = grab_screen(region=GRAB_REGION)
            print('loop took {} seconds'.format(time.time() - last_time))
            last_time = time.time()
            img = bit_mask(roi(cv2.resize(img, (WIDTH, HEIGHT)), ROI_VERTICES))

            prediction = model.predict([img.reshape(WIDTH, HEIGHT, 1)])[0]
            print(prediction)
            #time.sleep(1)

            mx, my, press = prediction

            mx = int(mx*kx+cx)
            my = int(my*ky+cy)

            if mx > max_x:  mx = max_x
            if mx < min_x:  mx = min_x
            if my > max_y:  my = max_y
            if my < min_y:  my = min_y

            if press > 0:
                mouse_down(mx, my)
            else:
                mouse_up(mx, my)

            cv2.imshow('window', img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        keys = key_check()
        # p pauses game and can get annoying.
        if 'R' in keys:
            mouse_up(cx,cy)
            mouse_down(cx,cy)
            time.sleep(0.1)
            mouse_up(cx,cy)
            time.sleep(0.1)
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                mx = int(0 * kx + cx)
                my = int(0 * ky + cy)
                if mx > max_x:  mx = max_x
                if mx < min_x:  mx = min_x
                if my > max_y:  my = max_y
                if my < min_y:  my = min_y
                mouse_up(mx, my)

                paused = True
                time.sleep(1)


main()

'''def main():

    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    thread = Thread(target=detect_clicks)
    thread.start()
    vertices = np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT],[WIDTH-85, HEIGHT],[WIDTH-85, HEIGHT-15],[WIDTH-105, HEIGHT-15],[WIDTH-105, HEIGHT], [0, HEIGHT],
                         ], np.int32)
    paused = False
    while True:
        a = cv2.cvtColor(cv2.resize(grab_screen(region=(0, 125, 1000, 725)),(WIDTH,HEIGHT)), cv2.COLOR_RGB2GRAY)
        screen = roi(a,[vertices])
        #cv2.imshow("SCREEN", screen)
       # time.sleep(0.1)

        if not paused:
            last_time = time.time()
            screen = screen

            x, y = win32api.GetCursorPos()
            training_data.append([screen, [x, y, isPressed]])

            if len(training_data) % 1000 == 0:
                print(len(training_data))
                np.save(file_name, training_data)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)

        cv2.imshow('window', screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()'''

'''
def screen_record():
    last_time = time.time()
    while(True):
        image = cv2.cvtColor(cv2.resize(grab_screen(region=(0, 125, 1000, 725)),(160,90)), cv2.COLOR_BGR2GRAY)
        x,y = win32api.GetCursorPos()

        print('x: {},y: {}, mouse_down: {}'.format(x, y, isPressed))
        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window',image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break'''