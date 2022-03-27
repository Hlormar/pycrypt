from colorama import init,Fore
import gnupg
import argparse
import os


init(1)
bin_path=os.getcwd()+r"\\GNUPG\\gpg.exe"






def key_gen(var_passphrase,var_key_type, var_key_length, var_name_real, var_name_comment, var_name_email):
	#Generating key path
	print(Fore.BLUE+"GENERATING KEYS")
	try:
		print("Trying to setup keys folder...")
		base_dir=os.getcwd()
		key_path_temp=os.getcwd()+"/Keys/"+var_name_real
		if not os.path.exists(key_path_temp):
			print("Key folder doesn't exist. Creating key folder...")
			os.makedirs(key_path_temp)
			os.chdir(key_path_temp)
		else:
			print("Key folder already exists")
			os.chdir(key_path_temp)
		print("Current Key directory is ",os.getcwd())
		gpg = gnupg.GPG(gnupghome=os.getcwd(),gpgbinary=bin_path)
		gpg.encoding = 'utf-8'
	except OSError:
		print(Fore.RED+"OOPS! OSError caused while setting up key folder\nProbably the GNUPG folder next to pycrypt does not exist")
		quit()
	except:
		print(Fore.RED+"OOPS! something went wrong while setting up key folder\n")
		quit()

	#Generating key
	try:
		print("Trying to generate keys...")
		input_data=gpg.gen_key_input(
		key_type=var_key_type,
		key_length=var_key_length,
		name_real=var_name_real,
		name_comment=var_name_comment,
		name_email=var_name_email,
		passphrase=var_passphrase
		)
		key = gpg.gen_key(input_data)
		print(Fore.GREEN+"The keys was succesfully created")
	except:
		print(Fore.RED+"OOPS! Something went wrong while trying to generate keys\n")
		quit()

	#Exporting Keys
	try:
		print("Trying to exporting keys...")
		public_keys = gpg.export_keys(var_name_real)
		private_keys = gpg.export_keys(var_name_real,True, passphrase=var_passphrase)
		with open(var_name_real+"_public.asc","w") as f:
			f.write(public_keys)
			f.close()
		print(Fore.GREEN+"Public key succesfully exported as ",var_name_real+"_public.asc")
		with open(var_name_real+"_secret.asc","w") as f:
			f.write(private_keys)
			f.close()
		print(Fore.GREEN+"Private key succesfully exported as ",var_name_real+"_secret.asc")
		os.chdir(base_dir)
		print("Current Key directory is ",os.getcwd(),"\n")
	except ValueError:
		print(Fore.RED+"OOPS! ValueError caused while trying generate keys.\nYou should have a passphrase to succesfully export keys.\nProbably, you do not have one.\nYou can easly add it by using -passphrase\n")
		quit()
	except:
		print(Fore.RED+"OOPS! Something went wrong while trying to export keys\n")
		quit()






def encrypt(file_raw_path,var_name_real):
	#Setting up key folder
	print(Fore.BLUE+"ENCRYPTING A FILE")
	try:
		print("Trying to setup path to public key...")
		public_key_path=os.getcwd()+r"\Keys\\"+(var_name_real)  #pycrypt/keys/test
		gpg = gnupg.GPG(gnupghome=public_key_path,gpgbinary=bin_path)
		gpg.encoding = 'utf-8'
	except ValueError:
		print(Fore.RED+'OOPS! ValueError caused while setting up path to public key\nProbably, the key',str(var_name_real)+"_public.asc"+' does not exist\n')
		quit()
	except:
		print(Fore.RED+"OOPS! Unknown error caused while setting up path to public key\n")
		quit()

	#Importing key
	try:
		print("Trying to import public key",var_name_real+"...")
		key_data=open(public_key_path+r"\\"+var_name_real+"_public.asc","r").read()
		import_result=gpg.import_keys(key_data)
	except:
		print(Fore.RED+"OOPS! something went wrong while importing the key\n")
		quit()
	
	#Trusting key
	try:
		print("Trying to trust public key",var_name_real+"...")
		gpg.trust_keys(import_result.fingerprints,'TRUST_ULTIMATE')

	except ValueError:
		print(Fore.RED+"OOPS! ValueError caused while trusting the key\nProbably, your key has been generated not by pycrypt")
		quit()
	except:
		print(Fore.RED+"OOPS! something went wrong while trusting the key\n")
		quit()
	
	#Encrypting file
	try:	
		print("Trying to encrypt file",file_raw_path+"...")
		file_encrypted= gpg.encrypt_file(open(file_raw_path,"rb"),recipients=var_name_real,output=file_raw_path+".gpg")
		if file_encrypted.ok==False:
			print('OK status:',Fore.RED+str(file_encrypted.ok))
		else:
			print('OK status:',Fore.GREEN+str(file_encrypted.ok))
		print(file_encrypted.stderr+'\n')
	except FileNotFoundError:
		print(Fore.RED+"OOPS! FileNotFoundError caused while encrypting the file\nProbably, your file_raw path wrong ")
		quit()
	except TypeError:
		print(Fore.RED+"OOPS! TypeError caused while encrypting the file\nProbably, you forgot to indicate file_raw ")
		quit()
	except:
		print(Fore.RED+"OOPS! something went wrong while encrypting the file\n")
		quit()






def decrypt(file_crypted_path,var_name_real="unnamed",var_passphrase=None):
		#Setting up key folder
		print(Fore.BLUE+"DECRYPTING A FILE")
		try:
			print("Trying to settup path to private key folder")
			base_dir=os.getcwd()
			key_path_temp=os.getcwd()+"/Keys/"+var_name_real
			os.chdir(key_path_temp)
			gpg = gnupg.GPG(gnupghome=os.getcwd(),gpgbinary=bin_path)
			gpg.encoding = 'utf-8'
		except ValueError:
			print(Fore.RED+'OOPS! ValueError caused while setting up path to private key\nProbably, the key',str(var_name_real)+"_secret.asc"+' does not exist\n')
			quit()
		except:
			print(Fore.RED+"OOPS! Unknown error caused while setting up path to private key\n")
			quit()

		#Deleting .gpg from name
		try:
			print("Trying to delete .gpg from the",file_crypted_path+"...")
			file_decrypted_name_list=file_crypted_path.split(".")
			file_decrypted_name_list.remove("gpg")
			file_decrypted_name=""
			counter=1
			for el in range(len(file_decrypted_name_list)):
				if counter!=len(file_decrypted_name_list):
					file_decrypted_name+=file_decrypted_name_list[el]+"."
					counter+=1
				else:
					file_decrypted_name+=file_decrypted_name_list[el]
		except ValueError:
			print(Fore.RED+"OOPS! Value error caused while deleting .gpg from the",str(file_crypted_path)+Fore.RED+'\nProbably, something wrong with',Fore.RED+str(file_crypted_path)+".\n")
			quit()
		except:
			print(Fore.RED+"OOPS! Something went wrong while deleting .gpg from the",str(file_crypted_path)+Fore.RED,'\n')
			quit()

		#decryption
		try:
			print("Trying to decrypt",file_crypted_path,"by the",var_name_real,"private key...")
			with open(file_crypted_path,"rb") as f:
				file_decrypted=gpg.decrypt_file(f,passphrase=var_passphrase,output=file_decrypted_name)
			if file_decrypted.ok==False:
				print('OK status:',Fore.RED+str(file_decrypted.ok))
			else:
				print('OK status:',Fore.GREEN+str(file_decrypted.ok))
			print(file_decrypted.stderr)
			if file_decrypted.ok==True:
				print("The decrypted file saved as",file_decrypted_name+"\n")
		except FileNotFoundError:
			print(Fore.RED+"OOPS! FileNotFoundError caused while decrypting",Fore.RED+str(file_crypted_path)+"\nProbably, your file_crypt path wrong"+Fore.RED)
			quit()
		except:
			print(Fore.RED+"OOPS! Something went wrong while decrypting",Fore.RED+str(file_crypted_path)+"\n")
			quit()
		try:
			os.chdir(base_dir)
		except:
			print(Fore.RED+"OOPS! Failed to change base directory from",Fore.RED+str(os.getcwd()),"to "+Fore.RED+str(base_dir)+"\n")
			quit()
