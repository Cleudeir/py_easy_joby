import time

def time_format_string(start_time):
        response_time = (time.time() - start_time) * 1000
        elapsed_time = f"{response_time:.2f} ms"
        if(response_time > 1000):  
            elapsed_time = f"{elapsed_time // 60} min {(elapsed_time % 60):.2f} s"
        if(response_time > 60 *1000):
            elapsed_time = f"{elapsed_time // (60 * 60)} h {elapsed_time % (60 * 60) // 60} min {elapsed_time % (60 * 60) % 60} s"
        if(response_time > 60 * 60 * 1000):
            elapsed_time = f"{elapsed_time // (60 * 60 * 24)} d {elapsed_time % (60 * 60 * 24) // (60 * 60)} h {elapsed_time % (60 * 60) // 60} min {elapsed_time % (60 * 60) % 60} s"
        if(response_time > 60 * 60 * 24 * 1000):
            elapsed_time = f"{elapsed_time // (60 * 60 * 24 * 30)} m {elapsed_time % (60 * 60 * 24 * 30) // (60 * 60)} h {elapsed_time % (60 * 60) // 60} min {elapsed_time % (60 * 60) % 60} s"
        return elapsed_time