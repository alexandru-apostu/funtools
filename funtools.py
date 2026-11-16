import os
import threading
import time

from forktex.api import create_app

counter = 0
app = create_app()


@app.get("/")
async def root():
    global counter
    counter += 1
    response = {
        "pid": os.getpid(),
        "count": counter,
        "native": threading.get_native_id(),
        "active_count": threading.active_count(),
    }
    return response


@app.get("/sync")
def sync():
    time.sleep(0.5)
    global counter
    counter += 1
    return {
        "pid": os.getpid(),
        "count": counter,
        "native": threading.get_native_id(),
        "active_count": threading.active_count(),
    }
