import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack
from operator import *

def get_subsidy(nCap, nMaxSubsidy, bnTarget):
    bnLowerBound = 0.01
    bnUpperBound = bnSubsidyLimit = nMaxSubsidy
    bnTargetLimit = 0x00000fffff000000000000000000000000000000000000000000000000000000

    while bnLowerBound + 0.01 <= bnUpperBound:
        bnMidValue = (bnLowerBound + bnUpperBound) / 2
        if pow(bnMidValue, nCap) * bnTargetLimit > pow(bnSubsidyLimit, nCap) * bnTarget:
            bnUpperBound = bnMidValue
        else:
            bnLowerBound = bnMidValue

    nSubsidy = round(bnMidValue, 2)

    if nSubsidy > bnMidValue:
        nSubsidy = nSubsidy - 0.01

    return int(nSubsidy * 1000000)

def debug_block_info(dat1):
	print 'block header',  data.block_header_type.unpack(dat1)['timestamp']
	return 0

nets = dict(
    yacoin=math.Object(
        P2P_PREFIX='d9e6e7e5'.decode('hex'),
        P2P_PORT=7688,
        ADDRESS_VERSION=77,
        RPC_PORT=8344,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'yacoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda target: get_subsidy(6, 100, target),
        BLOCKHASH_FUNC=lambda header: pack.IntType(256).unpack(__import__('yac_scrypt').getPoWHash(header, data.block_header_type.unpack(header)['timestamp'])),
        POW_FUNC=lambda header: pack.IntType(256).unpack(__import__('yac_scrypt').getPoWHash(header, data.block_header_type.unpack(header)['timestamp'])),
        BLOCK_PERIOD=60, # s
        SYMBOL='YAC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'yacoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/yacoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.yacoin'), 'yacoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://yacexplorer.tk/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://yacexplorer.tk/address/',
        SANE_TARGET_RANGE=(2**256//2**20//1000 - 1, 2**256//2**20 - 1),
    ),

    yacoin_testnet=math.Object(
        P2P_PREFIX='cdf2c0ef'.decode('hex'),
        P2P_PORT=17777,
        ADDRESS_VERSION=111,
        RPC_PORT=8344,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'novacoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda target: get_subsidy(6, 100, target),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=600, # s
        SYMBOL='tNVC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'YaCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/YaCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.yacoin'), 'yacoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://nonexistent-yacoin-testnet-explorer/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://nonexistent-yacoin-testnet-explorer/address/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
