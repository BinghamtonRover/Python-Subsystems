import lib.services as services

service = services.CanService(test=True)

service.register_handler(1, handler=lambda x: print(x.data))
service.mock_send(1, b"Hola")

print("Done")
