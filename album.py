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
    def Update(self, id):
        sql = ''' UPDATE Album
                SET nome_album = ?,
                    nome_banda = ?,
                    data_album = ? 
                WHERE id = ? '''
        
        id = self.IdValidation(id)        
        self.GetById(id)

        option = input("Tem certeza da alteração? [S/N]: ").upper()[0]
        while (option not in 'SN'):
            print("Entre com S ou N")
            option = input("Tem certeza da alteração? [S/N]: ").upper()[0]
        if (option in 'S'):

            albumName = input('Nome do album: ')
            bandName = input('Nome da banda: ')
            albumDate = input('Data do album: ')
            try:
                self.cursor.execute(sql, (albumName, bandName, albumDate, id))
            except Exception as e:
                Interface.WriteLow('[x] Falha na alteração do registro [x]')
                Interface.WriteLow(f'[x] Revertendo operação (rollback) [x]: {e}')
                self.db.rollback()
            else:
                self.db.commit()  
                Interface.WriteLow('[!] Registro alterado com sucesso [!]')  
        else:
            Interface.WriteLow('[!] Alteração cancelada [!]')
            self.db.rollback()


    # Delete
    def Delete(self, id):
        sql = f'''DELETE FROM ALBUM
                WHERE id = {id};'''

        id = self.IdValidation(id)
        self.GetById(id)
        Interface.Lines()

        option = input("Tem certeza da exclusão? [S/N]: ").upper()[0]
        while (option not in 'SN'):
            print("Entre com S ou N")
            option = input("Tem certeza da exclusão? [S/N]: ").upper()[0]
        if (option in 'S'):         
            try:
                self.cursor.execute(sql)
            except Exception as e:
                Interface.WriteLow('[x] Falha ao remover registro [x]')
                Interface.WriteLow(f'[x] Revertendo operação (rollback) [x]: {e}')
                self.db.rollback()
            else:
                self.db.commit()
                Interface.WriteLow('[!] Registro removido com sucesso [!]')
        else:
            Interface.WriteLow('[!] Exclusão cancelada [!]')
            self.db.rollback()

    def GetById(self, id):
        sql = f''' SELECT * FROM album
                  WHERE id = {id} '''
        result = self.cursor.execute(sql)
        result = result.fetchall()        
        Interface.Dictionary(result)
    
    def GetAllId(self):
        sql = "SELECT * FROM album"
                  
        result = self.cursor.execute(sql)
        result = result.fetchall()        
        
        listId = list()
        for row in result:
            listId.append(row[0])
        return listId

    def dbClose(self):
        self.cursor.close()

    # Validações
    def IdValidation(self, id): # validação de Ids    
        from time import sleep    
        while True:
            try:
                allIds = self.GetAllId() # pegando lista com todos os Id's
                if (allIds.count(int(id)) == 1):
                    break            
                else:
                    Interface.WriteLow(f"O Album com o id {id} não existe!")
                    print(f'\nALBUNS DISPONÍVEIS: ')
                    self.Read()
                    sleep(2)
                    Interface.Lines()
                    id = input("\nSelecione um Album existente: ")
            except Exception as e:
                Interface.WriteLow(f'Entre apenas com números no ID! Erro: {e}')
                id = input("Id Correto: ")
        return id


# main program
if __name__ == '__main__':
    crud = Crud()
    if (crud.fatalError):
        Interface.WriteLow('ERRO FATAL! NÃO PODEMOS DAR PROSSEGUIMENTO A APLICAÇÃO')
        exit()

    Interface.Lines()
    print(f'{"Bem-vindo(a) a Discografia UGB!!!":^30}')
    
    while True:
        Interface.Menu()
        option = int()
        try:
            option = int(input('\nSua opção: '))
        except Exception as e:
            Interface.WriteLow(f'Entre apenas com números! Erro: {e}')
            continue        

        if (option == 1): # Ler dados
            crud.Read()

        elif (option == 2): # Inserir dados
            Interface.Lines()
            albumName = input('Nome do album: ')
            bandName = input('Nome da banda: ')
            albumDate = input('Data do album: ')            
            crud.Insert(albumName, bandName, albumDate)

        elif (option == 3): # Atualizar dados
            Interface.LinesMenu()
            id = input('Qual Album deseja alterar? [informe o id]: ')
            crud.Update(id)

        elif (option == 4): # Deletar dados
            Interface.LinesMenu()
            id = input('Qual Album deseja deletar? [informe o id]: ')
            crud.Delete(id)

        elif (option == 5):
            Interface.Lines()
            print(f'{"VOLTE SEMPRE!":^40}')
            Interface.Lines()
            crud.dbClose()
            break
        
        else:
            Interface.WriteLow("OPÇÃO INVÁLIDA")