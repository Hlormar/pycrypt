from pycrypt_lib import *
import argparse
parser = argparse.ArgumentParser()
init(1)

#Argparse
parser = argparse.ArgumentParser()
#Variables
parser.add_argument("-key_type",
type=str,
help="Type of generating keys (default is RSA)",
action="store"
)
parser.add_argument("-key_lenght",
type=int,
help="Lenght of generating keys (default is 1024)",
action="store"
)
parser.add_argument("-name_real",
type=str,
help='Name using to create keys (default is "Autogenerated Key")',
action="store"
)
parser.add_argument("-name_comment",
type=str,
help='Comment using to create keys (default is "Generated by gnupg.py")',
action="store"
)
parser.add_argument("-name_email",
type=str,
help="Email adress using to create keys (default is <username>@<hostname>)",
action="store"
)
parser.add_argument("-passphrase",
type=str,
help="Phrase using to create keys and decrypt files. You should create it DEFENITELY",
action="store"
)
parser.add_argument("-file_raw",
type=str,
help="Path to file to be crypted",
action="store"
)
parser.add_argument("-file_crypted",
type=str,
help="Path to file to be encrypted",
action="store"
)


#Actions
parser.add_argument(
"--key_gen",
help="Generate a key pair",
action="store_true"
)
parser.add_argument(
"--encrypt",
help="Encrypt a file. Uses file_raw and name_real",
action="store_true"
)
parser.add_argument(
"--decrypt",
help="Decrypt a file. Uses file_crypted, name_real and passphrase",
action="store_true"
)


arg=parser.parse_args()
if arg.key_type==None:
    arg.key_type="RSA"
if arg.key_lenght==None:
    arg.key_lenght="1024"
if arg.name_real==None:
    arg.name_real="Autogenerated Key"
if arg.name_comment==None:
    arg.name_comment="Generated by gnupg.py"
if arg.name_email==None:
    arg.name_email="<username>@<hostname>"


if arg.key_gen:
	if arg.passphrase==None:
		print(Fore.YELLOW+"WARNING! Your passphrase is empy. You will be unalbe to decrypt files using pycrypt")
	key_gen(var_key_type=arg.key_type, var_key_length=arg.key_lenght, var_name_real=arg.name_real, var_name_comment=arg.name_comment, var_name_email=arg.name_email, var_passphrase=arg.passphrase)
if arg.encrypt:
	encrypt (file_raw_path=arg.file_raw,var_name_real=arg.name_real)
if arg.decrypt:
	decrypt (file_crypted_path=arg.file_crypted,var_name_real=arg.name_real,var_passphrase=arg.passphrase)