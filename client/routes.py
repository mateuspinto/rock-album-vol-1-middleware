def is_admin(SERVER, EMAIL):
    RESPONSE = SERVER.user__is_admin(EMAIL)
    return not RESPONSE['error']


def login(SERVER):
    while True:
        EMAIL = input('Digite o seu email: ')
        PASSWORD = input('Digite a sua senha: ')

        RESPONSE = SERVER.user__login(EMAIL, PASSWORD)

        if RESPONSE['error'] == 1:
            print(f'Erro! {RESPONSE["error_message"]} Tente novamente...\n')
        else:
            return EMAIL


def register(SERVER):
    while True:
        EMAIL = input('Digite o seu email: ')
        PASSWORD = input('Digite a sua senha: ')

        RESPONSE = SERVER.user__register(EMAIL, PASSWORD)

        if RESPONSE['error'] == 1:
            print(f'Erro! {RESPONSE["error_message"]} Tente novamente...\n')
        else:
            return EMAIL


# def admin__create_giftcard(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'admin/create_giftcard',
#         'email': EMAIL,
#         'giftcard_key': input('Insira a chave do cartão presente: ')
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def admin__create_stickers(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'admin/create_stickers',
#         'email': EMAIL,
#         'sticker_name': input('Insira o nome da figurinha: ')
#         'sticker_number': int(input('Insira a quantidade de figurinhas: '))
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def admin__draw_lucky_prize(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'admin/draw_lucky_prize',
#         'email': EMAIL,
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def admin__op(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'admin/op',
#         'email': EMAIL,
#         'target_email': input('Insira o email a ser tornado administrador: ')
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def admin__unop(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'admin/unop',
#         'email': EMAIL,
#         'target_email': input('Insira o email a ser removido de administrador: ')
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def album__get_album(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'album/get_album',
#         'email': EMAIL,
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Figurinhas:')
#         for sticker in RESPONSE['stickers']:
#             print(sticker)


# def album__get_free_stickers(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'album/get_free_stickers',
#         'email': EMAIL,
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Id - Nome da figurinhas:')
#         for sticker in RESPONSE['stickers']:
#             print(f'{sticker["id"]} - {sticker["sticker_name"]}')


# def album__paste_sticker(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'album/paste_sticker',
#         'email': EMAIL,
#         'sticker_id': input('Insira o ID da figurinha: ')
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def community_market__buy_sticker(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'community_market/buy_sticker',
#         'email': EMAIL,
#         'sticker_name': input('Insira o nome da figurinha: ')
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def community_market__get_sticker_price(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'community_market/get_sticker_price',
#         'email': EMAIL,
#         'sticker_name': input('Insira o nome da figurinha: ')
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print(f'A figurinha custa {RESPONSE["price"]}')


# def community_market__get_stickers_waiting_for_sale(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'community_market/get_stickers_waiting_for_sale',
#         'email': EMAIL,
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Preço - Nome da figurinhas')
#         for sticker in RESPONSE['stickers']:
#             print(f'{sticker["price"]} - {sticker["sticker_name"]}')


# def community_market__put_sticker_to_sell(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'community_market/put_sticker_to_sell',
#         'email': EMAIL,
#         'sticker_id': input('Insira o ID da figurinha: ')
#         'price': int(input('Insira o preço (em número inteiro) desejado na figurinha: '))
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def user__get_coins(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'user/get_coins',
#         'email': EMAIL,
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print(f'Você tem {RESPONSE["coins"]}')


# def user__retrieve_giftcard(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'user/retrieve_giftcard',
#         'email': EMAIL,
#         'giftcard_key': input('Insira a chave do cartão presente: ')
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')


# def official_market__buy_sticker_pack(SERVER, EMAIL):
#     REQUEST = {
#         'method': 'official_market/buy_sticker_pack',
#         'email': EMAIL,
#     }

#     RESPONSE = SERVER.method(REQUEST)

#     if RESPONSE['error'] == 1:
#         print(f'Erro! {RESPONSE["error_message"]}')
#     else:
#         print('Feito!')
