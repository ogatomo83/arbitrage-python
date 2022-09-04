import repository

zaif = repository.zaif_ticker(repository.zaif_symbol)
huobi = repository.huobi_ticker(repository.huobi_symbol)
bitflyer = repository.bitflyer_ticker(repository.bitflyer_symbol)
bit_point = repository.bit_point_ticker(repository.bit_point_symbol)

print(bit_point['asks'][0]['price'])

