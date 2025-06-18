import asyncio
from aiosmtpd.controller import Controller

class CustomHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message from:', envelope.mail_from)
        print('Message to:', envelope.rcpt_tos)
        print('Message data:\n', envelope.content.decode('utf8', errors='replace'))
        print('End of message\n')
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    handler = CustomHandler()
    controller = Controller(handler, hostname='127.0.0.1', port=8025)
    controller.start()
    print('SMTP server running at 127.0.0.1:8025')
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()