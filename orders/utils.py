import uuid


def generate_order_number():
    return str(uuid.uuid4()).replace('-', '').upper()[:12]
