import Pyro5.api
import json
import sqlite3
import logging
import sys


@Pyro5.api.expose
class RockAlbumServer(object):
    def __init__(self):
        CFG = json.load(open('config.json'))
        self.DATABASE = sqlite3.connect(CFG['SQLITE_FILE'])

    def __del__(self):
        self.DATABASE.close()

    def __exist_email_registered(self, EMAIL: str) -> int:
        DB_CUR = self.DATABASE.cursor()
        return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM users WHERE email="{EMAIL}"'))[0][0] == 1 else 0

    def __exist_giftcard(self, GIFTCARD_KEY: str) -> int:
        DB_CUR = self.DATABASE.cursor()
        return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM giftcards WHERE key="{GIFTCARD_KEY}"'))[0][0] == 1 else 0

    def __exist_sticker(self, STICKER_ID: int) -> int:
        DB_CUR = self.DATABASE.cursor()
        return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{STICKER_ID}"'))[0][0] == 1 else 0

    def __is_this_sticker_model_pasted(self, EMAIL: str, STICKER_ID: int) -> int:
        DB_CUR = self.DATABASE.cursor()
        STICKER_NAME = list(DB_CUR.execute(f'SELECT name FROM stickers WHERE id={STICKER_ID}'))[0][0]
        return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE name="{STICKER_NAME}" AND owner_email="{EMAIL}" AND is_pasted=1'))[0][0] == 1 else 0

    def __is_this_sticker_owned_by_the_user(self, EMAIL: str, STICKER_ID: int) -> int:
        DB_CUR = self.DATABASE.cursor()
        return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{STICKER_ID}" AND owner_email="{EMAIL}"'))[0][0] == 1 else 0

    def __is_this_sticker_waiting_for_sale(self, STICKER_ID: int) -> int:
        DB_CUR = self.DATABASE.cursor()
        return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{STICKER_ID}" AND is_for_sale=1'))[0][0] == 1 else 0

    def __get_coins(self, EMAIL: str) -> int:
        DB_CUR = self.DATABASE.cursor()
        return int(list(DB_CUR.execute(f'SELECT coins FROM users WHERE email="{EMAIL}"'))[0][0])

    def admin__create_giftcard(self, GIFTCARD_KEY: str):
        if self.__exist_giftcard(GIFTCARD_KEY) == 1:
            return {'error': 1, 'error_message': 'Falha na criação do Giftcard! Já existe um Giftcard com essa chave.'}

        DB_CUR = self.DATABASE.cursor()
        DB_CUR.execute(f'INSERT INTO giftcards VALUES ("{GIFTCARD_KEY}")')
        self.DATABASE.commit()
        return {'error': 0}

    def admin__create_stickers(self, STICKER_NAME: str, STICKER_NUMBER: int):
        DB_CUR = self.DATABASE.cursor()
        for _ in range(STICKER_NUMBER):
            DB_CUR.execute(f'INSERT INTO stickers (name, owner_email, is_pasted, is_for_sale, price) VALUES ("{STICKER_NAME}", "", 0, 0, 0)')
        self.DATABASE.commit()
        return {'error': 0}

    def admin__draw_lucky_prize(self):
        DB_CUR = self.DATABASE.cursor()
        DB_CUR.execute('UPDATE users SET coins=coins+50 WHERE email=(SELECT email FROM users ORDER BY RANDOM() LIMIT 1)')
        self.DATABASE.commit()
        return {'error': 0}

    def admin__op(self, TARGET_EMAIL: str):
        if self.__exist_email_registered(TARGET_EMAIL) == 0:
            return {'error': 1, 'error_message': 'Não é possível tornar esse usuário um administrador! Email não encontrado.'}

        DB_CUR = self.DATABASE.cursor()
        DB_CUR.execute(f'UPDATE users SET is_admin = 1 WHERE email="{TARGET_EMAIL}"')
        self.DATABASE.commit()
        return {'error': 0}

    def admin__unop(self, TARGET_EMAIL: str):
        if self.__exist_email_registered(TARGET_EMAIL) == 0:
            return {'error': 1, 'error_message': 'Não é possível tornar esse usuário um administrador! Email não encontrado.'}

        DB_CUR = self.DATABASE.cursor()
        DB_CUR.execute(f'UPDATE users SET is_admin = 0 WHERE email="{TARGET_EMAIL}"')
        self.DATABASE.commit()
        return {'error': 0}

    def album__get_album(self, EMAIL: str):
        DB_CUR = self.DATABASE.cursor()
        return {'error': 0, 'stickers': [x[0] for x in list(DB_CUR.execute(f'SELECT name FROM stickers WHERE owner_email="{EMAIL}" AND is_pasted=1'))]}

    def album__get_free_stickers(self, EMAIL: str):
        DB_CUR = self.DATABASE.cursor()
        return {'error': 0, 'stickers': [{'id': x[0], 'sticker_name': x[1]} for x in list(DB_CUR.execute(f'SELECT id, name FROM stickers WHERE owner_email="{EMAIL}" AND is_pasted=0 AND is_for_sale=0'))]}

    def album__paste_sticker(self, EMAIL: str, STICKER_ID: int):
        if self.__exist_sticker(STICKER_ID) == 0:
            return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! A figurinha não existe.'}

        if self.__is_this_sticker_model_pasted(EMAIL, STICKER_ID) == 1:
            return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! O modelo de figurinha já está colado.'}

        if self.__is_this_sticker_waiting_for_sale(STICKER_ID) == 1:
            return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! Ela está na fila para a venda.'}

        if self.__is_this_sticker_owned_by_the_user(EMAIL, STICKER_ID) == 0:
            return {'error': 1, 'error_message': 'Erro ao colar figurinha! O usuário não é dono desta figurinha.'}

        DB_CUR = self.DATABASE.cursor()
        DB_CUR.execute(f'UPDATE stickers SET is_pasted=1 WHERE id="{STICKER_ID}"')
        self.DATABASE.commit()
        return {'error': 0}

    def community_market__buy_sticker(self, EMAIL: str, STICKER_NAME: str):
        DB_CUR = self.DATABASE.cursor()
        QUERRY_RESULT = list(DB_CUR.execute(f'SELECT id, price FROM stickers WHERE price=(SELECT MIN(price) FROM stickers WHERE name="{STICKER_NAME}" AND is_for_sale=1 AND owner_email!="{EMAIL}")'))

        if len(QUERRY_RESULT) == 0:
            return {'error': 0, 'error_message': 'Não foi possível retornar preço da figurinha! Não há nenhuma figurinha desse modelo a venda!'}

        DESIRED_CARD = QUERRY_RESULT[0]

        if self.__get_coins(self) < DESIRED_CARD[1]:
            return {'error': 1, 'error_message': 'Não foi possível comprar a figurinha! Usuário sem moedas o suficiente'}

        DB_CUR.execute(f'UPDATE users SET coins=coins-{DESIRED_CARD[1]} WHERE email="{EMAIL}"')
        DB_CUR.execute(f'UPDATE stickers SET owner_email="{EMAIL}", is_for_sale=0, price=0 WHERE id={DESIRED_CARD[0]}')
        self.DATABASE.commit()
        return {'error': 0}

    def community_market__get_sticker_price(self, EMAIL: str, STICKER_NAME: str):
        DB_CUR = self.DATABASE.cursor()
        QUERRY_RESULT = list(DB_CUR.execute(f'SELECT price FROM stickers WHERE price=(SELECT MIN(price) FROM stickers WHERE name="{STICKER_NAME}" AND is_for_sale=1 AND owner_email!="{EMAIL}")'))

        if len(QUERRY_RESULT) == 0:
            return {'error': 1, 'error_message': 'Não foi possível retornar preço da figurinha! Não há nenhuma figurinha desse modelo a venda!'}

        return {'error': 0, 'price': QUERRY_RESULT[0][0]}

    def community_market__get_stickers_waiting_for_sale(self, EMAIL: str):
        DB_CUR = self.DATABASE.cursor()
        return {'error': 0, 'stickers': [{'sticker_name': x[0], 'price':x[1]} for x in list(DB_CUR.execute(f'SELECT name, price FROM stickers WHERE owner_email="{EMAIL}" AND is_for_sale=1'))]}

    def community_market__put_sticker_to_sell(self, EMAIL: str, STICKER_ID: int, PRICE: int):
        if self.__exist_sticker(self, STICKER_ID) == 0:
            return {'error': 1, 'error_message': 'Não é possível vender esta figurinha! A figurinha não existe.'}

        if self.__is_this_sticker_owned_by_the_user(EMAIL, STICKER_ID) == 0:
            return {'error': 1, 'error_message': 'Erro ao colocar figurinha a venda! O usuário não é dono desta figurinha.'}

        DB_CUR = self.DATABASE.cursor()
        DB_CUR.execute(f'UPDATE stickers SET is_for_sale=1, price={PRICE} WHERE id="{STICKER_ID}"')
        self.DATABASE.commit()
        return {'error': 0}

    def user__get_coins(self, EMAIL: str):
        return {'error': 0, 'coins': self.__get_coins(EMAIL)}

    def user__is_admin(self, EMAIL: str):
        DB_CUR = self.DATABASE.cursor()
        QUERY_RESULT = DB_CUR.execute(f'SELECT is_admin FROM users WHERE email="{EMAIL}"')
        if next(QUERY_RESULT)[0] == 1:
            return {'error': 0}
        else:
            return {'error': 1, 'error_message': 'Usuário não é administrador!'}

    def user__login(self, EMAIL: str, PASSWORD: str):
        DB_CUR = self.DATABASE.cursor()
        if list(DB_CUR.execute(f'SELECT COUNT(*) FROM users WHERE email="{EMAIL}" AND password="{PASSWORD}"'))[0][0] == 1:
            return {'error': 0}
        else:
            return {'error': 1, 'error_message': 'Usuário não encontrado!'}

    def user__register(self, EMAIL: str, PASSWORD: str):
        if self.__exist_email_registered(EMAIL) == 1:
            return {'error': 1, 'error_message': 'Falha no cadastro! Email já está em uso.'}

        DB_CUR = self.DATABASE.cursor()
        DB_CUR.execute(f'INSERT INTO users VALUES ("{EMAIL}", "{PASSWORD}", 0, 0)')
        self.DATABASE.commit()
        return {'error': 0}

    def user__retrieve_giftcard(self, EMAIL: str, GIFTCARD_KEY: str):
        if self.__exist_giftcard(GIFTCARD_KEY) == 0:
            return {'error': 1, 'error_message': 'Falha no resgate do Giftcard! Não existe um Giftcard com essa chave.'}

        DB_CUR = self.DATABASE.cursor()
        DB_CUR.execute(f'UPDATE users SET coins=coins+100 WHERE email="{EMAIL}"')
        DB_CUR.execute(f'DELETE FROM giftcards WHERE key="{GIFTCARD_KEY}"')
        self.DATABASE.commit()
        return {'error': 0}

    def official_market__buy_sticker_pack(self, EMAIL: str):
        DB_CUR = self.DATABASE.cursor()

        if list(DB_CUR.execute('SELECT COUNT(*) FROM stickers WHERE owner_email=""'))[0][0] < 2:
            return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Não existe figurinhas impressas sem dono suficientes'}

        if self.__get_coins(EMAIL) < 10:
            return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Você não tem moedas o suficiente!'}

        DB_CUR.execute(f'UPDATE users SET coins=coins-10 WHERE email="{EMAIL}"')
        for _ in range(2):
            DB_CUR.execute(f'UPDATE stickers SET owner_email="{EMAIL}" WHERE id=(SELECT id FROM stickers WHERE owner_email="" ORDER BY RANDOM() LIMIT 1)')

        self.DATABASE.commit()

        return {'error': 0}


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s :: [%(levelname)s] %(message)s;')
    logging.getLogger("Pyro5").setLevel(logging.DEBUG)
    logging.getLogger("Pyro5.core").setLevel(logging.DEBUG)

    with Pyro5.server.Daemon() as DAEMON:
        NAME_SERVER = Pyro5.api.locate_ns()
        URI = DAEMON.register(RockAlbumServer)
        NAME_SERVER.register("rockalbum.server", URI)

        DAEMON.requestLoop()
