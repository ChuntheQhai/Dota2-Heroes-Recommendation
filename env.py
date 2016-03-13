import os

def main():
	print "run env.."
	os.environ["DOTABOT_API_KEY"] = "6E83EFA8D7815C7747AADD786AA043E8"
	os.environ["DOTABOT_USERNAME"] = "username"
	os.environ["DOTABOT_PASSWORD"] = "password"
	os.environ["DOTABOT_HOSTNAME"] = "hostname"
	os.environ["DOTABOT_DB_SERVER"] = "server"
	os.environ["DOTABOT_DB_NAME"] = "name"

if __name__ == '__main__':
	main()

