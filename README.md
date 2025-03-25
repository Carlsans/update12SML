Every file is commented in english and french. I suggess your read each comment before trying to run it.
I run the code on arch-based linux cron job, but I guess it would also run fine on windows.
You must install playwright, include your wordpress website username and password in the /src/credentials.json file.
Depending on the number of source you have to update, you need to modify SOURCE_COUNT variable.
setting :   browser = p.firefox.launch(headless=True)
with headless=False
is nice to make tests, but will crash if added to a cron job.
Please modify /cron/updatemeetings.sh to fit your installation.

Push request appreciated, would be nice to make it work on windows too.

Chaque fichier est commenté en anglais et en français. Je vous suggère de lire chaque commentaire avant d'essayer de l'exécuter.
J'exécute le code sur un job cron linux basé sur arch, mais j'imagine qu'il fonctionnerait aussi bien sous windows.
Vous devez installer playwright, inclure le nom d'utilisateur et le mot de passe de votre site wordpress dans le fichier /src/credentials.json.
En fonction du nombre de sources à mettre à jour, vous devez modifier la variable SOURCE_COUNT.
setting : browser = p.firefox.launch(headless=True)
avec headless=False
est utile pour faire des tests, mais va planter si elle est ajoutée à un job cron.
Veuillez modifier /cron/updatemeetings.sh pour l'adapter à votre installation.

La demande de push est appréciée, ce serait bien que ça fonctionne aussi sous Windows.
