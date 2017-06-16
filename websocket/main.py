import websocket
import thread
import time

def on_message(ws, message):
    print "Message:" + message.decode("utf-8")

def on_error(ws, error):
    print "Error:" + error.decode("utf-8")

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("http://s46-101-206-115.splix.io:8001/splix",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    #ws.on_open = on_open
    ws.run_forever()