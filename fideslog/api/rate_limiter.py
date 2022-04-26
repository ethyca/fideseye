from slowapi.extension import Limiter
from slowapi.util import get_remote_address

rate_limiter = Limiter(key_func=get_remote_address)