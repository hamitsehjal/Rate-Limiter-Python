from bucket import Bucket
from collections import defaultdict
import time
import threading

ip_to_bucket = defaultdict(
    lambda: Bucket()
)  # map each missing key to new instance of Bucket

lock = threading.Lock()

""" 
Why use Lock in the refill_buckets method??

Even though, the `Queue` data-structure is thread-safe, the sequence of operations involve:
- check if the bucket is empty
- adding token to the bucket 

Between these two operations, any other thread could potentially modify the bucket, specially if the `refill_buckets` is running concurrently with the request handler
"""


def refill_buckets():
    while True:
        with lock:
            for ip, bucket in ip_to_bucket.items():
                if not bucket.is_full():
                    bucket.add_token()
        time.sleep(1)


refill_thread = threading.Thread(target=refill_buckets, daemon=True)
