import pylast


lastfmApiKey = '8b7f5ccf0c14f75ea8e1b1a5bdd1fd5c'
API_SECRET = '5e6413b0a8abb30309d2eef5b9d882ca'
lastfm_username = 'bumi_'
lastfm_password_hash = pylast.md5("Ilsfhs4eae!")

lastfm_network = pylast.LastFMNetwork(
    api_key = lastfmApiKey,
    api_secret=API_SECRET,
    username=lastfm_username,
    password_hash=lastfm_password_hash,
)

databaseLocation = "/Users/joshuareid/Documents/GitHub/SmartBotDatabase/SmartBot.db"
groupyToken = "j0uo0ElyoFkVWdKAwXEuBsS8JLvvr925BOZCqik0"
groupy_id = 57087652
bot_id = "199b4198cf92f44506557e07f2"