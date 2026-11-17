"""Start Ask Ashbourne locally:  python run.py [--port 8000] [--host 127.0.0.1]"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ashbourne import llm  # noqa: E402
from ashbourne.server import make_server  # noqa: E402


def main():
    p = argparse.ArgumentParser(description="Ask Ashbourne v1")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    a = p.parse_args()
    srv = make_server(a.host, a.port)
    mode = "LIVE (Anthropic API)" if llm.live_mode() else "OFFLINE (no ANTHROPIC_API_KEY)"
    print(f"Ask Ashbourne running at http://{a.host}:{a.port}/  mode: {mode}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
