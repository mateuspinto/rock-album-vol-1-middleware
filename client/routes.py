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


def admin__create_giftcard(SERVER, _):
    GIFTCARD_KEY = input('Insira a chave do cartão presente: ')

    RESPONSE = SERVER.admin__create_giftcard(GIFTCARD_KEY)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def admin__create_stickers(SERVER, _):
    STICKER_NAME = input('Insira o nome da figurinha: ')
    STICKER_NUMBER = int(input('Insira a quantidade de figurinhas: '))

    RESPONSE = SERVER.admin__create_stickers(STICKER_NAME, STICKER_NUMBER)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def admin__draw_lucky_prize(SERVER, _):

    RESPONSE = SERVER.admin__draw_lucky_prize()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def admin__op(SERVER, _):
    TARGET_EMAIL = input('Insira o email a ser tornado administrador: ')

    RESPONSE = SERVER.admin__op(TARGET_EMAIL)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def admin__unop(SERVER, _):
    TARGET_EMAIL = input('Insira o email a ser removido de administrador: ')

    RESPONSE = SERVER.admin__unop(TARGET_EMAIL)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def album__get_album(SERVER, EMAIL):

    RESPONSE = SERVER.album__get_album(EMAIL)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Figurinhas:')
        for sticker in RESPONSE['stickers']:
            print(sticker)


def album__get_free_stickers(SERVER, EMAIL):

    RESPONSE = SERVER.album__get_free_stickers(EMAIL)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Id - Nome da figurinhas:')
        for sticker in RESPONSE['stickers']:
            print(f'{sticker["id"]} - {sticker["sticker_name"]}')


def album__paste_sticker(SERVER, EMAIL):
    STICKER_ID = input('Insira o ID da figurinha: ')

    RESPONSE = SERVER.album__paste_sticker(EMAIL, STICKER_ID)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def community_market__buy_sticker(SERVER, EMAIL):
    STICKER_NAME = input('Insira o nome da figurinha: ')

    RESPONSE = SERVER.community_market__buy_sticker(EMAIL, STICKER_NAME)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def community_market__get_sticker_price(SERVER, EMAIL):
    STICKER_NAME = input('Insira o nome da figurinha: ')

    RESPONSE = SERVER.community_market__get_sticker_price(EMAIL, STICKER_NAME)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print(f'A figurinha custa {RESPONSE["price"]}')


def community_market__get_stickers_waiting_for_sale(SERVER, EMAIL):

    RESPONSE = SERVER.community_market__get_stickers_waiting_for_sale(EMAIL)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Preço - Nome da figurinhas')
        for sticker in RESPONSE['stickers']:
            print(f'{sticker["price"]} - {sticker["sticker_name"]}')


def community_market__put_sticker_to_sell(SERVER, EMAIL):
    STICKER_ID = input('Insira o ID da figurinha: ')
    PRICE = int(input('Insira o preço (em número inteiro) desejado na figurinha: '))

    RESPONSE = SERVER.community_market__put_sticker_to_sell(EMAIL, STICKER_ID, PRICE)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def user__get_coins(SERVER, EMAIL):

    RESPONSE = SERVER.user__get_coins(EMAIL)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print(f'Você tem {RESPONSE["coins"]}')


def user__retrieve_giftcard(SERVER, EMAIL):
    GIFTCARD_KEY = input('Insira a chave do cartão presente: ')

    RESPONSE = SERVER.user__retrieve_giftcard(EMAIL, GIFTCARD_KEY)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def official_market__buy_sticker_pack(SERVER, EMAIL):

    RESPONSE = SERVER.official_market__buy_sticker_pack(EMAIL)

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')
