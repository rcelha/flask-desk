#!/bin/env python


def main():
    print("Flask desk runner")
    from app import app
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
