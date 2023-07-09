from datetime import datetime

def greet():
    time = datetime.now()
    print(f"now, it's {time} o'clock!")
    msg = "Morning!"
    
    return msg
