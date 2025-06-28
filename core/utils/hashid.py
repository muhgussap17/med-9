from hashids import Hashids

hashids = Hashids(min_length=10, salt="rme-clinic-salt")

def encode_id(id):
    return hashids.encode(id)

def decode_hash(hash_id):
    decoded = hashids.decode(hash_id)
    return decoded[0] if decoded else None
