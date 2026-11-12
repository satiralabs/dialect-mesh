"""
DialectMesh CLI: Direct terminal interface for offline semantic routing.
"""

import argparse
import json
import sys
from .router import IntentRouter
from .normalizer import normalize_text


def cmd_route(args):
    router = IntentRouter()
    res = router.route(args.query, lang=args.lang, threshold=args.threshold)
    print(json.dumps(res, indent=2, ensure_ascii=False))


def cmd_normalize(args):
    res = normalize_text(args.query, lang=args.lang)
    print(f"Original:   {args.query}")
    print(f"Normalized: {res}")


def main():
    parser = argparse.ArgumentParser(
        prog="dialect-mesh",
        description="DialectMesh: Edge Semantic Router for Low-Resource Languages",
    )
    subparsers = parser.add_subparsers(dest="command")

    p_route = subparsers.add_parser("route", help="Route a query to an intent and API tool")
    p_route.add_argument("query", help="Raw vernacular text (Amharic, Oromo, Swahili)")
    p_route.add_argument("--lang", default="auto", choices=["auto", "am", "om", "sw"])
    p_route.add_argument("--threshold", type=float, default=0.35)
    p_route.set_defaults(func=cmd_route)

    p_norm = subparsers.add_parser("normalize", help="Normalize vernacular text")
    p_norm.add_argument("query", help="Text to normalize")
    p_norm.add_argument("--lang", default="auto", choices=["auto", "am", "om", "sw"])
    p_norm.set_defaults(func=cmd_normalize)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
