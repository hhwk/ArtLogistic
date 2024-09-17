from deta import Deta
deta = Deta("c0n8ymyprw2_CwMUwv7o9KNkeKG3tdFX4VNF7Zi3km1B")
Users = deta.Base("Users")
Curs = deta.Base("Curs")

db_content = Users.fetch().items
print(db_content[0]['key'])
#Users.put({'key':f'{message.chat.id}','role':'user','change_id':'','price_wait':0,'orders':[]})
for i in range(0,10):
    print(i)
