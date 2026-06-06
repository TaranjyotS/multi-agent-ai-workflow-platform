from collections import Counter
from threading import Lock


class MetricsRegistry:
    def __init__(self) -> None:
        self._counter: Counter[str] = Counter()
        self._lock = Lock()

    def inc(self, name: str) -> None:
        with self._lock:
            self._counter[name] += 1

    def render_prometheus(self) -> str:
        with self._lock:
            lines = ["# TYPE app_counter counter"]
            for key, value in sorted(self._counter.items()):
                lines.append(f'app_counter{{name="{key}"}} {value}')
            return "\n".join(lines) + "\n"


metrics = MetricsRegistry()
