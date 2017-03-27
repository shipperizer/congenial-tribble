import logging
import os
import ssl

from hyper import HTTPConnection


def init_logging():
    logger = logging.getLogger('client')
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] - [%(asctime)s] - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def create_ssl_context(certfile, keyfile):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.options |= (
        ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION
    )
    ssl_context.set_ciphers("EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH")
    ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    ssl_context.set_alpn_protocols(["h2"])
    return ssl_context


if __name__ == '__main__':
    init_logging()
    for i in range(100):
        conn = HTTPConnection(
            'https://{}'.format(os.environ['SERVER_HOST']),
            ssl_context=create_ssl_context('/tmp/client/cert.pem', '/tmp/client/key.pem')
        )
        conn.request('GET', '/')
        resp = conn.get_response()

        logger(resp.read())
