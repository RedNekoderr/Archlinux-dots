import signal

heights = []


def handler(signum, frame) -> None:
    raise Exception()
    return


def loop_forever() -> None:
    global heights
    while True:
        heights.append(int(input()))
    return


signal.signal(signal.SIGALRM, handler)
signal.alarm(1)
try:
    loop_forever()
except Exception:
    if len(heights) > 0:
        print(sum(heights) / len(heights))
    else:
        print(-1)
