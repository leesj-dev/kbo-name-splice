"""Combine template.html + data/payload.json + assets/pretendard-subset.woff2
into the final, self-contained index.html (no external requests at all --
the font is embedded as a base64 data URI, the match data is embedded as
inline JSON).
"""
import base64

TEMPLATE_PATH = "template.html"
PAYLOAD_PATH = "data/payload.json"
FONT_PATH = "assets/pretendard-subset.woff2"
OUT_PATH = "index.html"


def main():
    template = open(TEMPLATE_PATH, encoding="utf-8").read()
    payload = open(PAYLOAD_PATH, encoding="utf-8").read()
    font_b64 = base64.b64encode(open(FONT_PATH, "rb").read()).decode("ascii")

    out = template.replace("__PAYLOAD__", payload).replace("__FONT_B64__", font_b64)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {OUT_PATH} ({len(out) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
