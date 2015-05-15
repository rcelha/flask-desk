#!/bin/env python


def main():
    from app import app
    import logging
    logging.info("Flask desk runner")
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
