import os
import random
import shutil
import time
import traceback
import pyperclip
import ua_generator
from utils.logger import logger
from playwright.sync_api import sync_playwright


class PWModel:

    def __init__(self, number, auth_token, ct0, private=None, proxy=None, inviteLink=None):
        self.playwright = sync_playwright().start()

        self.inviteLink = inviteLink
        # print(self.inviteLink)

        self.auth_token, self.ct0 = auth_token, ct0
        self.number = number
        self.proxy = proxy
        self.privateKey = private

        # print(self.privateKey)

        EX_path = "MetaMask"

        user_data_dir = f"{os.getcwd()}\\dataDir"

        self.context = self.playwright.chromium.launch_persistent_context(user_data_dir,
                                                                          user_agent=ua_generator.generate(
                                                                              device="desktop", browser="chrome").text,
                                                                          proxy={
                                                                              "server": f"{proxy.split(':')[0]}:{proxy.split(':')[1]}",
                                                                              "username": f"{proxy.split(':')[2]}",
                                                                              "password": f"{proxy.split(':')[3]}",
                                                                          } if proxy != None else None, headless=False,
                                                                          devtools=False, args=[
                f'--load-extension={os.getcwd()}\\{EX_path}',
                f'--disable-extensions-except={os.getcwd()}\\{EX_path}'
                ])

        self.context.add_cookies([
            {"name": "auth_token",
             "value": self.auth_token,
             "domain":".twitter.com",
             "path":"/"},

            {"name": "ct0",
             "value": self.ct0,
             "domain":".twitter.com",
             "path":"/"}
        ])

        self.page = self.context.new_page()

        self.page.set_default_timeout(60000)

    def CreateNewWallet(self):
        # Открытие страницы Twitter
        # self.page.goto('https://yandex.ru')
        self.page.wait_for_timeout(5000)

        # print(self.context.pages)

        self.MMPage = self.context.pages[-1]
        self.MMPage.bring_to_front()
        self.MMPage.reload()
        self.MMPage.wait_for_selector('input[id="onboarding__terms-checkbox"]').click()
        self.MMPage.wait_for_selector('button[data-testid="onboarding-create-wallet"]').click()
        self.MMPage.wait_for_selector('button[data-testid="metametrics-i-agree"]').click()
        self.MMPage.wait_for_selector('input[data-testid="create-password-new"]').fill('Passwordsdjeruf039fnreo')
        self.MMPage.wait_for_selector('input[data-testid="create-password-confirm"]').fill('Passwordsdjeruf039fnreo')
        self.MMPage.wait_for_selector('input[data-testid="create-password-terms"]').click()
        self.MMPage.wait_for_selector('button[data-testid="create-password-wallet"]').click()
        self.MMPage.wait_for_selector('button[data-testid="secure-wallet-later"]').click()
        self.MMPage.wait_for_selector('input[data-testid="skip-srp-backup-popover-checkbox"]').click()
        self.MMPage.wait_for_selector('button[data-testid="skip-srp-backup"]').click()
        self.MMPage.wait_for_selector('button[data-testid="onboarding-complete-done"]').click()
        self.MMPage.wait_for_selector('button[data-testid="pin-extension-next"]').click()
        self.MMPage.wait_for_timeout(1000)
        self.MMPage.wait_for_selector('button[data-testid="pin-extension-done"]').click()
        self.MMPage.wait_for_timeout(4000)
        self.MMPage.wait_for_selector('button[data-testid="popover-close"]').click()
        # self.MMPage.wait_for_timeout(1000)
        # self.MMPage.wait_for_selector('button[data-testid="popover-close"]').click()

        if self.privateKey == None:
            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/div/div/div/button').click()
            self.MMPage.wait_for_timeout(3000)
            self.address = pyperclip.paste()

            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/span/button/span').click()
            self.MMPage.wait_for_selector('xpath=//*[@id="popover-content"]/div[2]/button[2]').click()

            self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/button[3]').click()
            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[5]/div/input').fill(
                'Passwordsdjeruf039fnreo')
            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[7]/button[2]').click()

            holdButton = self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[3]/button/span')
            holdButton.hover()
            self.MMPage.mouse.down()
            self.MMPage.wait_for_timeout(3000)
            self.MMPage.mouse.up()

            self.privateKey = '0x' + self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[5]/div').text_content()
            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[7]/button').click()


        else:

            self.MMPage.wait_for_timeout(1000)
            self.MMPage.wait_for_selector('button[data-testid="account-menu-icon"]').click()
            self.MMPage.wait_for_selector('div.account-menu > button.account-menu__item.account-menu__item--clickable')
            self.MMPage.query_selector_all(
                'div.account-menu > button.account-menu__item.account-menu__item--clickable')[1].click()
            self.MMPage.wait_for_selector('input[id="private-key-box"]').fill(self.privateKey)
            self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]').click()
            self.MMPage.wait_for_selector('button[data-testid="eth-overview-send"]')

            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/div/div/div/button').click()
            self.address = pyperclip.paste()




    def TwitterCheck(self):

        self.page.goto("https://twitter.com")

        try:
            self.page.wait_for_selector('a[href="/i/verified-choose"]', timeout=30000)
            return True
        except:
            return False

    def ZetaChain(self):

        self.page.bring_to_front()
        self.page.goto("https://labs.zetachain.com/leaderboard" if self.inviteLink == None else self.inviteLink)

        self.page.wait_for_timeout(random.randint(1000, 4000))
        self.page.wait_for_selector('xpath=/html/body/div[2]/div[3]/div')
        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(random.randint(1000, 4000))
        self.page.wait_for_selector('xpath=//div[text()="Verify with Twitter"]').click()
        self.page.wait_for_selector('div[data-testid="OAuth_Consent_Button"]', timeout=20000).click()

        # try:
        #     self.page.wait_for_selector('xpath=//div[text()="Connect Wallet"]',state="visible" , timeout=10000).click()
        # except:
        self.page.wait_for_selector('xpath=/html/body/div[2]/div[3]/div')
        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(random.randint(1000, 4000))
        self.page.wait_for_selector('xpath=//div[text()="Connect Wallet"]').click()

        self.ConnectWallet('xpath=/html/body/div[2]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/button/div/div/div[1]/div[1]')

        self.page.wait_for_timeout(random.randint(1000, 4000))

        try:
            self.page.wait_for_selector('xpath=//*[@id="__next"]/div/div/main/div/div[1]/button[2]', timeout=10000).click()
        except:
            pass

        self.page.wait_for_timeout(random.randint(5000, 12000))

        # self.page.wait_for_timeout(100000000)

    def ConfirmWallet(self):

        self.page.goto("https://labs.zetachain.com/leaderboard")

        self.page.wait_for_selector('xpath=/html/body/div[2]/div[3]/div')
        self.page.keyboard.press('Escape')

        self.ConfirmTransaction('xpath=//*[@id="__next"]/div/div/main/div/div[1]/div/button')
        self.page.wait_for_timeout(random.randint(1000, 4000))

    def RequireTokens(self):

        self.page.goto("https://labs.zetachain.com/get-zeta")
        self.page.wait_for_timeout(random.randint(4000, 8000))

        self.page.wait_for_selector('xpath=/html/body/div[2]/div[3]/div')
        self.page.keyboard.press('Escape')

        self.page.wait_for_selector('xpath=//*[@id="__next"]/div/div/main/div/div[1]/button[2]').click()
        self.page.wait_for_timeout(random.randint(1000, 4000))


        self.inviteLink = pyperclip.paste()

    #     https://labs.zetachain.com/leaderboard?code=K6gXx9NhBXS3shV_EksZL
    def GetInviteLink(self):

        self.page.goto("https://labs.zetachain.com/leaderboard")
        self.page.wait_for_timeout(random.randint(4000, 8000))

        self.page.wait_for_selector('xpath=/html/body/div[2]/div[3]/div')
        self.page.keyboard.press('Escape')

        self.page.wait_for_selector('xpath=//*[@id="__next"]/div/div/main/div/div[2]/div/div[2]/div[2]/button/div').click()
        self.page.wait_for_timeout(random.randint(1000, 4000))
        self.page.wait_for_selector('xpath=/html/body/div[2]/div[3]/div/div[3]/button').click()
        self.page.wait_for_timeout(random.randint(1000, 4000))

        self.inviteLink = pyperclip.paste()

    #     https://labs.zetachain.com/leaderboard?code=K6gXx9NhBXS3shV_EksZL

    def GhostChain(self):

        self.page.goto("https://airdrop.ghostchain.io/")

        self.page.wait_for_selector('xpath=//*[@id="root"]/div/div[1]/div[2]/button').click()
        self.page.wait_for_timeout(random.randint(1000, 4000))

        self.ConnectWallet('xpath=/html/body/div[2]/div[3]/button[1]')

        self.page.wait_for_selector('div[aria-labelledby="select-network-label select-network"]').click()
        self.page.wait_for_timeout(random.randint(1000, 4000))
        self.page.wait_for_selector('xpath=//*[@id="menu-"]/div[3]/ul/li[24]').click()
        self.page.wait_for_timeout(random.randint(1000, 4000))

        self.ConfirmTransaction('xpath=//*[@id="root"]/div/div[2]/div/div/div/div[2]/div[2]/button')
        self.page.wait_for_timeout(random.randint(1000, 4000))



    def DotZeta(self):

        self.page.goto("https://dotzeta.me/")
        self.page.wait_for_timeout(random.randint(3000, 8000))

        self.page.wait_for_selector('xpath=//*[@id="__next"]/div/main/div/div[1]/div/div[3]/div/button').click()
        self.page.wait_for_timeout(random.randint(1000, 4000))
        self.SpecialConnect('xpath=/html/body/div[2]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/button')

        self.page.wait_for_selector('xpath=//*[@id="__next"]/div/main/div/div[2]/div[1]/div[2]/div/div[1]/div/input').fill(self.randomTitle)
        self.page.wait_for_timeout(random.randint(1000, 4000))

        if self.page.wait_for_selector('xpath=//*[@id="__next"]/div/main/div/div[2]/div[1]/div[2]/div/ul/div/div/div[4]').text_content() == "Available":
            self.page.wait_for_selector(
                'xpath=//*[@id="__next"]/div/main/div/div[2]/div[1]/div[2]/div/ul/div/div/div[4]').click()

        else:
            self.page.wait_for_selector(
                'xpath=//*[@id="__next"]/div/main/div/div[2]/div[1]/div[2]/div/div[1]/div/input').fill(self.randomTitle)
            self.page.wait_for_timeout(random.randint(1000, 4000))

            if self.page.wait_for_selector(
                    'xpath=//*[@id="__next"]/div/main/div/div[2]/div[1]/div[2]/div/ul/div/div/div[4]').text_content() == "Available":
                self.page.wait_for_selector(
                    'xpath=//*[@id="__next"]/div/main/div/div[2]/div[1]/div[2]/div/ul/div/div/div[4]').click()


        self.page.wait_for_selector('xpath=//*[@id="__next"]/div/div/div[1]/div[2]/div[1]/div[5]/button').click()
        self.page.wait_for_timeout(random.randint(1000, 4000))
        self.ConfirmTransaction('xpath=//*[@id="modal__register_domain"]/form/div/button')
        self.page.wait_for_selector('xpath=//*[@id="modal__register_domain"]/form/div/div[2]/button[2]').click()

        self.page.wait_for_timeout(random.randint(5000, 12000))

    def AceSwap(self):

        self.page.goto("https://test.aceswap.io/ru/swap?inputCurrency=ETH&outputCurrency=0x1320f70ab72E867d3e54840929659fF75cA88210")

        self.page.wait_for_selector('div.flex.flex-col.gap-3 > button[id="connect-wallet"]').hover()
        self.page.wait_for_timeout(6000)

        self.page.mouse.click(0,0)
        self.page.wait_for_selector('div.flex.flex-col.gap-3 > button[id="connect-wallet"]').click()
        self.ConnectWallet('img[src="https://res.cloudinary.com/sushi-cdn/image/fetch/f_auto,c_limit,w_64,q_auto/https://app.sushi.com/images/wallets/metamask.png"]')

        self.page.wait_for_timeout(random.randint(3000, 10000))


        for i in range(random.randint(1,4)):
            inputs = self.page.query_selector_all('input[title="Token Amount"]')
            inputs[0].fill(str(3*(random.randint(3,15)/100)))

            try:
                self.page.wait_for_selector('button[id="swap-button"]').click()
                self.page.wait_for_timeout(random.randint(1000, 4000))
                self.ConfirmTransaction('button[id="confirm-swap-or-send"]')
            except:
                self.page.wait_for_selector('div.bg-dark-900.border.border-dark-800 svg.text-high-emphesis').click()
                self.page.wait_for_timeout(random.randint(1000, 4000))
                self.page.wait_for_selector('button[id="swap-button"]').click()
                self.page.wait_for_timeout(random.randint(1000, 4000))
                self.ConfirmTransaction('button[id="confirm-swap-or-send"]')

            self.page.wait_for_timeout(random.randint(1000, 4000))
            self.page.wait_for_selector('div.bg-dark-900.border.border-dark-800 svg.text-high-emphesis').click()
            self.page.wait_for_timeout(random.randint(1000, 4000))
            self.page.wait_for_selector('xpath=//*[@id="swap-page"]/div/div[2]/div/div[2]/div[2]/div').click()
            self.page.wait_for_timeout(random.randint(1000, 4000))

            while float(self.page.query_selector_all('div[class="text-sm leading-5 font-medium cursor-pointer select-none flex text-secondary whitespace-nowrap"]')[0].text_content().split(' ')[-1]) == 0:
                self.page.wait_for_timeout(1000)

            balance = float(self.page.query_selector_all('div[class="text-sm leading-5 font-medium cursor-pointer select-none flex text-secondary whitespace-nowrap"]')[0].text_content().split(' ')[-1])
            inputs = self.page.query_selector_all('input[title="Token Amount"]')
            inputs[0].fill(str(balance*(random.randint(10,50)/100)))

            try:

                if i == 0:
                    self.ConfirmToken('//*[@id="swap-page"]/div/div[2]/div/div[2]/div[5]/button')
                else:
                    try:
                        self.ConfirmToken('//*[@id="swap-page"]/div/div[2]/div/div[2]/div[5]/button')
                    except:
                        pass

                self.page.wait_for_timeout(random.randint(1000, 4000))
                self.page.wait_for_selector('button[id="swap-button"]').click()
                self.page.wait_for_timeout(random.randint(1000, 4000))
                self.ConfirmTransaction('button[id="confirm-swap-or-send"]')
            except:
                self.page.wait_for_selector('div.bg-dark-900.border.border-dark-800 svg.text-high-emphesis').click()
                self.page.wait_for_timeout(random.randint(1000, 4000))
                self.page.wait_for_selector('button[id="swap-button"]').click()
                self.page.wait_for_timeout(random.randint(1000, 4000))
                self.ConfirmTransaction('button[id="confirm-swap-or-send"]')

            self.page.wait_for_timeout(random.randint(1000, 4000))
            self.page.wait_for_selector('div.bg-dark-900.border.border-dark-800 svg.text-high-emphesis').click()
            self.page.wait_for_timeout(random.randint(1000, 4000))
            self.page.wait_for_selector('xpath=//*[@id="swap-page"]/div/div[2]/div/div[2]/div[2]/div').click()
            self.page.wait_for_timeout(random.randint(1000, 4000))

        # self.page.goto("https://test.aceswap.io/ru/legacy/add/ETH?chainId=7001")
        # self.page.wait_for_timeout(random.randint(1000, 4000))
        #
        # self.page.wait_for_selector('xpath=//*[@id="add-page"]/div/div[2]/div[1]/div[4]/div[1]/div/button').click()
        # self.page.wait_for_timeout(random.randint(1000, 4000))
        # self.page.wait_for_selector('xpath=//div[text()="AceSwap"]').click()
        # self.page.wait_for_timeout(random.randint(1000, 4000))
        #
        # inputs = self.page.query_selector_all('input[title="Token Amount"]')
        # balance = float(self.page.query_selector_all(
        #     'div[class="text-sm leading-5 font-medium cursor-pointer select-none flex text-secondary whitespace-nowrap"]')[1].text_content().split(
        #     ' ')[-1])
        # inputs[1].fill(str(balance * (random.randint(40, 70) / 100)))
        # self.page.wait_for_timeout(random.randint(1000, 4000))
        #
        # try:
        #     self.ConfirmToken('xpath=//*[@id="add-page"]/div/div[2]/div[1]/div[6]/button')
        # except:
        #     pass
        # self.page.wait_for_timeout(random.randint(5000, 12000))
        # self.page.wait_for_selector('xpath=//*[@id="add-page"]/div/div[2]/div[1]/div[6]/button').click()
        # self.page.wait_for_timeout(random.randint(20000, 30000))
        # self.ConfirmTransaction('xpath=//button[text()="Добавить ликвидность"]')
        # self.page.wait_for_timeout(random.randint(5000, 12000))
        # self.page.wait_for_selector('div.bg-dark-900.border.border-dark-800 svg.text-high-emphesis').click()
        # self.page.wait_for_timeout(random.randint(5000, 12000))

    def ConfirmToken(self, element):

        pages = len(self.context.pages)
        self.page.wait_for_selector(element, timeout=10000).click()

        _ = 0
        while pages == len(self.context.pages) and _ < 30:
            self.page.wait_for_timeout(1000)
            _ += 1

        if _ >= 30:
            raise Exception("Превышено время ожидания открытия страницы Метамаск")

        else:

            self.MMConfirmer = self.context.pages[-1]
            self.MMConfirmer.wait_for_selector('div.custom-spending-cap__max > button.mm-button-link--size-auto.mm-text--body-md').click()
            self.MMConfirmer.wait_for_timeout(3000)
            self.MMConfirmer.wait_for_selector('button[data-testid="page-container-footer-next"]').click()
            self.MMConfirmer.wait_for_timeout(3000)
            self.MMConfirmer.wait_for_selector('button[data-testid="page-container-footer-next"]').click()
            self.MMConfirmer.wait_for_timeout(3000)


    def ConnectWallet(self, element):

        pages = len(self.context.pages)
        self.page.wait_for_selector(element).click()

        _ = 0
        while pages == len(self.context.pages) and _ < 60:
            self.page.wait_for_timeout(1000)
            _ += 1

        if _ >= 60:
            raise Exception("Превышено время ожидания открытия страницы Метамаск")

        else:

            self.MMConfirmer = self.context.pages[-1]
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            try:
                self.MMConfirmer.wait_for_selector('button.btn-primary.button', timeout=5000).click()
            except:
                pass

    def ConfirmTransaction(self, element):

        pages = len(self.context.pages)
        self.page.wait_for_selector(element).click()

        _ = 0
        while pages == len(self.context.pages) and _ < 30:
            self.page.wait_for_timeout(1000)
            _ += 1

        if _ >= 30:
            raise Exception("Превышено время ожидания открытия страницы Метамаск")

        else:

            self.MMConfirmer = self.context.pages[-1]
            self.MMConfirmer.wait_for_selector('button[data-testid="page-container-footer-next"]').click()
            self.MMConfirmer.wait_for_timeout(3000)

    def SpecialConnect(self, element):

        pages = len(self.context.pages)
        self.page.wait_for_selector(element).click()

        _ = 0
        while pages == len(self.context.pages) and _ < 60:
            self.page.wait_for_timeout(1000)
            _ += 1

        if _ >= 60:
            raise Exception("Превышено время ожидания открытия страницы Метамаск")

        else:

            self.MMConfirmer = self.context.pages[-1]
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            try:
                self.MMConfirmer.wait_for_selector('button.btn-primary.button', timeout=5000).click()
            except:
                pass


    @property
    def randomTitle(self) -> str:
        adjectives = [
            "Red", "Blue", "Majestic", "Lonely", "Vibrant", "Mysterious", "Serene",
            "Ethereal", "Dynamic", "Gloomy", "Harmonious", "Infinite", "Radiant",
            "Surreal", "Ancient", "Charming", "Elegant", "Graceful", "Quaint",
            "Rustic", "Stunning", "Sublime", "Whimsical", "Dazzling", "Exquisite",
            "Magnificent", "Opulent", "Picturesque", "Timeless", "Captivating",
            "Enchanting", "Peaceful", "Breathtaking", "Luminous", "Translucent",
            "Mesmerizing", "Spellbinding", "Delightful", "Divine", "Idyllic",
            "Lavish", "Luxurious", "Poetic", "Splendid", "Striking", "Grandiose"
        ]
        nouns = [
            "Sunset", "Ocean", "Mountain", "Forest", "Sky", "River", "Moon",
            "Desert", "Prairie", "Lake", "Star", "Planet", "Galaxy", "Comet",
            "Meadow", "Island", "Beach", "Waterfall", "Cliff", "Volcano",
            "Canyon", "Fjord", "Cave", "Valley", "Gorge", "Summit",
            "Horizon", "Glacier", "Grove", "Plateau", "Lagoon", "Marsh",
            "Swamp", "Estuary", "Reef", "Jungle", "Archipelago", "Bay",
            "Dune", "Oasis", "Tundra", "Savannah", "Rainforest", "Woodland",
            "Hill", "Field", "Pond", "Brook", "Stream", "Fountain"
        ]
        return f"{random.choice(adjectives)}{random.choice(adjectives)}{random.choice(nouns)}"

    def close(self):
        self.playwright.stop()

def TaskDestibutor():
    elements = ['GhostChain', 'AceSwap']

    # Сначала выбираем первый элемент ('DotZeta' или 'AceSwap')
    first_element = 'DotZeta'

    # Определяем, сколько еще элементов нужно добавить (0, 1 или 2)
    additional_elements_count = random.randint(0, 2)

    # Извлекаем дополнительные уникальные элементы
    additional_elements = random.sample(elements, additional_elements_count)

    # Создаем и возвращаем результирующую последовательность
    return [first_element] + additional_elements





if __name__ == '__main__':

    print(' ___________________________________________________________________\n'
          '|                       Rescue Alpha Soft                           |\n'
          '|                   Telegram - @rescue_alpha                        |\n'
          '|                   Discord - discord.gg/438gwCx5hw                 |\n'
          '|___________________________________________________________________|\n\n\n')

    try:
        shutil.rmtree(f"{os.getcwd()}/dataDir")
    except:
        pass

    delay = (15, 30)
    delayTasks = (10, 20)
    refCount = (3, 9)
    globalRefCode = None

    try:
        with open('config', 'r', encoding='utf-8') as file:
            for i in file:

                if 'refCount=' in i.rstrip():
                    refCount = (int(i.rstrip().split('refCount=')[-1].split('-')[0]), int(i.rstrip().split('refCount=')[-1].split('-')[1]))
                if 'refLink=' in i.rstrip():
                    globalRefCode = str(i.rstrip().split('refLink=')[-1])
                    if globalRefCode == "":
                        globalRefCode = None
                if 'delayTasks=' in i.rstrip():
                    delayTasks = (int(i.rstrip().split('delayTasks=')[-1].split('-')[0]),
                                int(i.rstrip().split('delayTasks=')[-1].split('-')[1]))
                if 'delay=' in i.rstrip():
                    delay = (int(i.rstrip().split('delayAccs=')[-1].split('-')[0]),
                                int(i.rstrip().split('delayAccs=')[-1].split('-')[1]))

    except:
        # traceback.print_exc()
        print('Вы неправильно настроили конфигуратор, повторите попытку')
        input()
        exit(0)

    proxies = []
    with open('InputData/Proxies.txt', 'r') as file:
        for i in file:
            proxies.append(i.rstrip())

    privates = []
    with open('InputData/Privates.txt', 'r') as file:
        for i in file:
            privates.append(i.rstrip())

    twitterData = []
    with open('InputData/TwitterData.txt', 'r') as file:
        for i in file:
            twitterData.append([i.rstrip().split("auth_token=")[-1].split(';')[0], i.rstrip().split("ct0=")[-1].split(';')[0]])



    localRefCode = None
    startRefCount = 0
    randomRefCount = None

    for i in range(len(proxies)):

        try:
            shutil.rmtree(f"{os.getcwd()}/dataDir")
        except:
            pass

        if localRefCode == None or startRefCount == randomRefCount:
            randomRefCount = random.randint(refCount[0], refCount[1])
            startRefCount = 0

        try:
            # print(localRefCode)
            # print(globalRefCode)
            model = PWModel(i + 1,
                            twitterData[i][0],
                            twitterData[i][1],
                            privates[i] if len(privates) != 0 and privates[0] != "" else None,
                            proxies[i],
                            localRefCode if localRefCode != None else globalRefCode if globalRefCode != None else None)
            status = model.TwitterCheck()

            if status:
                logger.info(f"{i + 1} | Аккаунт Twitter рабочий")

                model.CreateNewWallet()
                logger.info(f"{i + 1} | Аккаунт MetaMask активирован")

                model.ZetaChain()
                logger.info(f"{i + 1} | Аккаунт ZetaChain активирован")
                try:
                    model.ConfirmWallet()
                    logger.info(f"{i+1} | Кошелек успешно подключен")
                except:
                    logger.info(f"{i+1} | К данному аккаунту кошелек уже был подключен ранее")

                try:
                    model.RequireTokens()
                    logger.info(f"{i + 1} | Тестовые токены успешно получены")
                except:
                    logger.info(f"{i + 1} | Тестовые токены получить не удалось")

                model.GetInviteLink()
                invite = model.inviteLink

                for project in TaskDestibutor():

                    if project == 'GhostChain':
                        try:
                            model.GhostChain()
                            logger.info(f"{i + 1} | GhostChain успешно выполнен")
                        except Exception as e:
                            logger.info(f"{i + 1} | GhostChain не удалось сделать, ошибка ({str(e)})")

                    elif project == 'DotZeta':
                        model.DotZeta()
                        logger.info(f"{i + 1} | DotZeta успешно выполнен")

                    elif project == 'AceSwap':
                        model.AceSwap()
                        logger.info(f"{i + 1} | AceSwap успешно выполнен")

                    time.sleep(random.randint(delayTasks[0], delayTasks[1]))

                logger.info(f"{i + 1} | Действия на аккаунте успешно выполнены")

                if localRefCode == None:
                    localRefCode = invite
                    logger.success(f'{i + 1} | Зарегистрирован рефовод. Код - {localRefCode}')
                else:

                    startRefCount += 1
                    logger.success(f'{i + 1} | Реферал {startRefCount}/{randomRefCount} зарегистрирован')

            else:
                logger.error(f"{i+1} | Проблемы с аккаунтом твиттера")

        except Exception as e:
            traceback.print_exc()
            logger.error(f"{i + 1} | Произошла ошибка ({str(e)})")

        try:
            model.close()
        except:
            pass

        try:
            with open("result.txt", "a+") as file:
                file.write(model.privateKey + '|' + proxies[i] + '|' + twitterData[i][0] + '|' + twitterData[i][1] + '\n')
        except:
            pass

        time.sleep(random.randint(delay[0], delay[1]))
        print('')

    logger.warning("Скрипт успешно завершил свою работу")
    input()

