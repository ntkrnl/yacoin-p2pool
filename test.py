from p2pool.bitcoin import data, networks, sha256
from p2pool.util import pack


#"hash" : "000008d60d927a984d19b852348711f8d21c261b1247e61b44f307580f2ca6b6"
#"version" : 3,
#"merkleroot" : "916fb05aed6373d6e5c49626efc0dea5d103038135bffbc86014f5204df2ebe3",
#"mint" : 100.00000000,
#"time" : 1367995782,
#"nonce" : 58004,
#"bits" : "1e0fffff",


block_header = dict(
version=3,
previous_block=0xf260c39629d99355c5476d710d46ca0d35b3d962b44054b9ff943fe622,
merkle_root=0x916fb05aed6373d6e5c49626efc0dea5d103038135bffbc86014f5204df2ebe3,
timestamp=1367995782,
bits=data.FloatingInteger(0x1e0fffff),
nonce=58004,
)

DONATION_SCRIPT = '01210241b8aba0994f320a8b438c627dbf31fbdd7dc722dd8418d829d67a9c6e4fd69021036fbd9d0a34a569f10b0431c8aeecf74ad796b99838b7272ef35ded130a794f9b02ae'.decode('hex')
print DONATION_SCRIPT[2:35].encode('hex')
print data.pubkey_to_address(DONATION_SCRIPT[2:35], networks.nets['yacoin'])
print networks.nets['yacoin'].POW_FUNC(data.block_header_type.pack(block_header)) 

print data.pubkey_hash_to_script2(data.address_to_pubkey_hash('YJL3vTFn7m82zQRs7XAXcJXnBNNmZdb1Ty', networks.nets['yacoin'])).encode('hex')

donate = '4104ffd03de44a6e11b9917f3a29f9443283d9871c9d743ef30d5eddcd37094b64d1b3d8090496b53256786bf5c82932ec23c3b74d9f05a6f95a8b5529352656664bac'.decode('hex')
#print data.script2_to_address(donate, networks.nets['bitcoin'])
#print len("c8c6a3c0957d53698da14d7a2c176a133e92fc53".decode('hex'))
#print donate[1:-1].encode('hex')
#print data.pubkey_to_script2(donate[1:-1]).encode('hex')
#print donate[3:-2].encode('hex')
#print data.pubkey_hash_to_script2(donate[3:-2]).encode('hex')
#print len('0241b8aba0994f320a8b438c627dbf31fbdd7dc722dd8418d829d67a9c6e4fd690'.decode('hex'))
#print data.pubkey_to_script2('0241b8aba0994f320a8b438c627dbf31fbdd7dc722dd8418d829d67a9c6e4fd690'
#036fbd9d0a34a569f10b0431c8aeecf74ad796b99838b7272ef35ded130a794f9b
print data.base58_encode('cac8509b8f959d14253e934585c52d04bf4ae21d28e62414a0c71c9fb80a5713'.decode('hex'))
text = sha256.sha256('cac8509f4ae21d28e62414a0c71c9fb80a5713sdfsdfsdfsdfsfsdssssssssss')
print text.state
print text.buf
print text.length
print len(text.buf)
print len('cac8509b8f959d14253e934585c52d04bf4ae21d28e62414a0c71c9fb80a5713')
print len('21029df5832989ca91c766b0c2707eda848854b825efa650ec2d001138a5f8123650ac')
