# class Db:
#     def __init__(self):


class Crud:
    def __init__(self):   
        import sqlite3
        self.db = sqlite3.connect('Discografia.db') # conectando ao banco de dados
        # self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor() # criando cursor 

        self.cursor.execute("""create table if not exists Album(
                id integer not null primary key autoincrement,
                nome_album text not null,
                nome_banda text not null,
                data_album text not null);""" )       

    def Menu(self):
        print()
        print('-=' * 20)
        print('''Menu de opções
1 - Ver discografia atual
2 - Inserir nova Discografia
3 - Atualizar Discografia
4 - Deletar Disco
5 - Sair''')
        print('-=' * 20)

    
    def Insert(self, albumName, bandName, albumDate):    
        sql = """INSERT INTO Album(nome_album, nome_banda, data_album)
            VALUES (?, ?, ?); """
        
        self.cursor.execute(sql, (albumName, bandName, albumDate))  
        self.db.commit()

    def Read(self):
        sql = 'SELECT * FROM Album'
        result = self.cursor.execute(sql)
        result = result.fetchall()        
        
        json = dict()
        for tuple in result:
            # print(f'Album {tuple[0]}')
            json = {
                'Id': tuple[0],
                'Nome do Album': tuple[1],
                'Nome da Banda': tuple[2],
                'Data do Album': tuple[3]
            }

            print('=-' * 15)
            for key, value in json.items():
                print(f'{key}: {value}')


    def Delete(self, id):
        sql = '''DELETE FROM ALBUM
                WHERE id = ?;'''
        self.cursor.execute(sql, id)
        self.db.commit()


    def Update(self, id, albumName, bandName, albumDate):
        sql = ''' UPDATE Album
                SET nome_album = ?,
                    nome_banda = ?,
                    data_album = ? 
                WHERE id = ?'''
        
        self.cursor.execute(sql, (albumName, bandName, albumDate, id))
        self.db.commit()    

    def getById(self, id):
        sql = ''' SELECT * FROM album
                  WHERE id = ? '''
        result = self.cursor.execute(sql, id)
        result = result.fetchall()        
        
        json = dict()
        for tuple in result:
            # print(f'Album {tuple[0]}')
            json = {
                'Id': tuple[0],
                'Nome do Album': tuple[1],
                'Nome da Banda': tuple[2],
                'Data do Album': tuple[3]
            }

            print('=-' * 15)
            for key, value in json.items():
                print(f'{key}: {value}')
        print('=-' * 15)
        
        # self.db.commit()  


    def dbClose(self):
        self.cursor.close()


# programa principal
print('\nBem-vindo(a) a Discografia UGB!!!')

crud = Crud()

while True:
    crud.Menu()
    option = int(input('\nSua opção: '))

    if (option == 1):
        crud.Read()
    elif (option == 2):
        print('-=' * 21)
        albumName = input('Nome do album: ')
        bandName = input('Nome da banda: ')
        albumDate = input('Data do album: ')  
        
        crud.Insert(albumName, bandName, albumDate)
    elif (option == 3):
        print('-=' * 21)
        id = input('Qual Album deseja alterar? [informe o id]: ')
        crud.getById(id)
        albumName = input('Qual é o novo nome do album?: ')
        bandName = input('Novo nome da banda: ')
        albumDate = input('Nova data do album: ')  

        crud.Update(id, albumName, bandName, albumDate)
    elif (option == 4):
        print('-=' * 21)
        id = input('Qual Album deseja deletar? [informe o id]: ')
        crud.Delete(id)

    elif (option == 5):
        print('\nVolte sempre!')
        crud.dbClose()
        break 

        







