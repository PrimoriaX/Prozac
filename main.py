import os
from colorama import Fore, Back, Style
from prozac import Prozac

def run():
    startup()
    prints()
    Prozac().listen()

def startup():
    os.system("color")
    os.system(f"title Prozac")

def prints():
    ascii_art = """
                                           @@@@@@
                                       @@@@@@@@@@@@
                                     @@@@@@@@@@@@@@@@
                                    @@@@@@@@@@@@@@@@@@
                                   @@@@@@@@@@@@@@@@@@@@@
                                    @@@@@@@@@@@@@@@@@@@@@@@
                                     @@@@@@@@@@@@@@@@@@@######
                                     @@@@@@@@@@@@@@@@##########
                                       @@@@@@@@@@@@##############
                                         @@@@@@@@@#################
                                           @@@@@@####################
                                             @@@#######################
                                                 ########################
                                                  ######################
                                                    ###################
                                                      ###############
                                                        ###########
                                                          #######
                                         ▄▄▄·▄▄▄        ·▄▄▄▄• ▄▄▄·  ▄▄·
                                        ▐█ ▄█▀▄ █·     ▪▀·.█▌▐█ ▀█ ▐█ ▌▪
                                         ██▀·▐▀▀▄  ▄█▀▄ ▄█▀▀▀•▄█▀▀█ ██ ▄▄
                                        ▐█▪·•▐█•█▌▐█▌.▐▌█▌▪▄█▀▐█ ▪▐▌▐███▌
                                        .▀   .▀  ▀ ▀█▄▀▪·▀▀▀ • ▀  ▀ ·▀▀▀
    """

    ascii_art = ascii_art.replace("@", f"{Fore.GREEN}@{Style.RESET_ALL}").replace(".", f"{Fore.WHITE}.{Style.RESET_ALL}")

    support_discord = f"{Fore.LIGHTBLACK_EX}\t\t\t  [{Fore.GREEN}x{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} Join our support discord server: {Fore.GREEN}discord.gg/bsNKqvxvE2   {Style.RESET_ALL}"
    
    print(ascii_art)
    print(support_discord)
    
run()
