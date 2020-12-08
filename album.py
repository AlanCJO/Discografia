class Interface:
    @staticmethod # criando um método estático pelo o objeto não ser diferente um do outro, então não precisaríamos instanciar 
    def Menu():
        Interface.Lines()
        print(f'{"MENU DE OPÇÕES":^40}\n')
        print(f'''{"1 - Ver discografia atual":30}{"|":>10.8}
{"2 - Inserir nova Discografia":30}{"|":>10.8}               
{"3 - Atualizar Discografia":30}{"|":>10.8}                   
{"4 - Deletar Disco":30}{"|":>10.8}                           
{"5 - Sair":30}{"|":>10.8}''')                                
        Interface.Lines()

    @staticmethod
    def Lines():
        print('-=' * 20)

    @staticmethod
    def LinesMenu():
        print('-=' * 25)
    
    @staticmethod
    def Dictionary(query):
        json = dict()
        for tuple in query:
            json = {
                'Id': tuple[0],
                'Nome do Album': tuple[1],
                'Nome da Banda': tuple[2],
                'Data do Album': tuple[3]
            }
            Interface.Lines()
            for key, value in json.items():
                print(f'{key}: {value}')

    @staticmethod
    def WriteLow(word):
        from time import sleep
        print()
        for l in word:
            print(l, flush=True, end='')
            sleep(0.02)
        print()


class Crud:
    def __init__(self):   
        import sqlite3
        self.db = sqlite3.connect('Discografia.db') # conectando ao banco de dados
        self.cursor = self.db.cursor() # criando cursor 
        self.fatalError = self.createTable()

    def createTable(self, name="Album"):
        try:
            self.cursor.execute(f"""create table if not exists {name}(
                id integer not null primary key autoincrement,
                nome_album text not null,
                nome_banda text not null,
                data_album text not null);""")    
        except Exception as e:
            Interface.WriteLow(f'[x] Falha ao criar tabela {name} [x]: {e}')
            return True
        else:
            Interface.WriteLow(f'[!] Tabela {name} criada com sucesso [!]')
            return False

    # Create
    def Insert(self, albumName, bandName, albumDate):    
        sql = """INSERT INTO Album(nome_album, nome_banda, data_album)
            VALUES (?, ?, ?); """
        
        try:
            self.cursor.execute(sql, (albumName, bandName, albumDate))  
        except Exception as e:
            Interface.WriteLow('[x] Falha ao inserir registro [x]')
            Interface.WriteLow(f'[x] Revertendo a operação(rollback) [x]: {e}')
            self.db.rollback()
        else:
            self.db.commit()
            Interface.WriteLow('[!] Registro inserido com sucesso [!]\n')

    # Retrieve
    def Read(self):
        sql = 'SELECT * FROM Album'
        result = self.cursor.execute(sql)
        result = result.fetchall()        
        
        Interface.Dictionary(result) # apresenta informações em forma de dicionário
        
    # Update
    def Update(self, id, albumName, bandName, albumDate):
        sql = ''' UPDATE Album
                SET nome_album = ?,
                    nome_banda = ?,
                    data_album = ? 
                WHERE id = ?'''
        
        try:
            self.cursor.execute(sql, (albumName, bandName, albumDate, id))
        except Exception as e:
            Interface.WriteLow('[x] Falha na alteração do registro [x]')
            Interface.WriteLow(f'[x] Revertendo operação (rollback) [x]: {e}')
            self.db.rollback()
        else:
            self.db.commit()  
            Interface.WriteLow('[!] Registro alterado com sucesso [!]')  

    # Delete
    def Delete(self, id):
        sql = '''DELETE FROM ALBUM
                WHERE id = ?;'''

        try:
            self.cursor.execute(sql, id)
        except Exception as e:
            Interface.WriteLow('[x] Falha ao remover registro [x]')
            Interface.WriteLow(f'[x] Revertendo operação (rollback) [x]: {e}')
            self.db.rollback()
        else:
            self.db.commit()
            Interface.WriteLow('[!] Registro removido com sucesso [!]')


    def getById(self, id):
        sql = ''' SELECT * FROM album
                  WHERE id = ? '''
        result = self.cursor.execute(sql, id)
        result = result.fetchall()        
        Interface.Dictionary(result)


    def dbClose(self):
        self.cursor.close()


# programa principal
if __name__ == '__main__':
    crud = Crud()
    if (crud.fatalError):
        Interface.WriteLow('ERRO FATAL! NÃO PODEMOS DAR PROSSEGUIMENTO A APLICAÇÃO')
        exit()

    print(f'\n{"Bem-vindo(a) a Discografia UGB!!!":^30}')

    while True:
        Interface.Menu()
        option = int(input('\nSua opção: '))

        if (option == 1):
            crud.Read()
        elif (option == 2):
            Interface.Lines()
            albumName = input('Nome do album: ')
            bandName = input('Nome da banda: ')
            albumDate = input('Data do album: ')  
            
            crud.Insert(albumName, bandName, albumDate)
        elif (option == 3):
            Interface.LinesMenu()
            id = input('Qual Album deseja alterar? [informe o id]: ')

            crud.getById(id)
            Interface.Lines()
            albumName = input('Nome do album: ')
            bandName = input('Nome da banda: ')
            albumDate = input('Data do album: ')  

            crud.Update(id, albumName, bandName, albumDate)
        elif (option == 4):
            Interface.LinesMenu()
            id = input('Qual Album deseja deletar? [informe o id]: ')

            crud.Delete(id)
        elif (option == 5):
            print('\nVolte sempre!')
            crud.dbClose()
            break
