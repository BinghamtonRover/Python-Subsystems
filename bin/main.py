import lib.services as services

service = services.CanService(test=True)
# message_sender = services.MessageSender()
# message_receiver = services.MessageReceiver()

service.register_handler(1, handler=lambda x: print(x.data))
service.mock_send(1, b"Hola")

rover = services.Rover()
rover.drive.brake()

print("Done")
