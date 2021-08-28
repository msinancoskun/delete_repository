import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import shutil


class RepoDeleter:

    def __init__(self, username, password):
        """ Initializing the RepoDeleter class"""
        self.username = username
        self.password = password
        self.final_repo = list()
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.repo_to_delete = None

    def login(self):
        """ This method creates the login process to github.com"""
        self.browser.get('https://github.com/login')
        # This line finds the username login part of the authorization page and enters
        # the username
        login_info = self.browser.find_element_by_xpath('//*[@id="login_field"]')
        login_info.send_keys(self.username)
        
        # This line finds the username login part of the authorization page and enters
        # the username
        login_info = self.browser.find_element_by_xpath('//*[@id="password"]')
        login_info.send_keys(self.password)

        # Clicks the login button on the authorization page after entering username, password.
        login_info = self.browser.find_element_by_xpath('//*[@id="login"]/div[4]/form/div/input[12]')
        login_info.click()

        # Check username and password.
        # if self.username != RepoDeleter.USERNAME or self.password != RepoDeleter.PASSWORD:
        #     print("Wrong password or username, try again!")
        # else:
        self.browser.get('https://github.com/{}?tab=repositories'.format(self.username))

    def create_repo_list(self):
        """ This method is used to create a repository list using
            the existing repositories from github.com"""
        text_repository = []
        base_url = 'https://github.com/{}?tab=repositories'.format(self.username)
        source = requests.get(base_url).text
        soup = BeautifulSoup(source, 'html.parser')
        repositories = soup.find_all('h3', class_='wb-break-all')
        for i in range(len(repositories)):
            text_repository.append(repositories[i].text)
        for repo in text_repository:
            new_repo = repo.split('        ')
            self.final_repo.append(new_repo[1].split('\n')[0])

        print(self.final_repo)

    def repo_delete(self, repo_name):
        """ This method is used to delete the repository by repo_name and removes it from the list."""
        self.repo_to_delete = repo_name
        
        x_path = ['//*[@id="user-repositories-list"]/ul/li[1]/div[1]/div[1]/h3/a',
                  '//*[@id="user-repositories-list"]/ul/li[2]/div[1]/div[1]/h3/a',
                  '//*[@id="user-repositories-list"]/ul/li[3]/div[1]/div[1]/h3/a',
                  '//*[@id="user-repositories-list"]/ul/li[4]/div[1]/div[1]/h3/a',
                  '//*[@id="user-repositories-list"]/ul/li[5]/div[1]/div[1]/h3/a',
                  '//*[@id="user-repositories-list"]/ul/li[6]/div[1]/div[1]/h3/a']

        index = 0
        for repo in self.final_repo:
            if repo_name == repo:
                self.final_repo.remove(self.repo_to_delete)
                for j in range(len(x_path)):
                    if index == j:
                        delete = self.browser.find_element_by_xpath(x_path[index])
                        delete.click()
                        self.browser.get('https://github.com/{}/{}/settings'.format(self.username, repo_name))
                        delete_button = self.browser.find_element_by_xpath('//*[@id="options_bucket"]/div[10]'
                                                                           '/ul/li[4]/details/summary')
                        delete_button.click()
                        delete_button = self.browser.find_element_by_xpath('//*[@id="options_bucket"]'
                                                                           '/div[10]/ul/li[4]/details/'
                                                                           'details-dialog/div[3]/form/p/input')
                        delete_button.send_keys('{}/{}'.format(self.username, repo_name))

                        delete_button = self.browser.find_element_by_xpath('//*[@id="options_bucket"]/div[10]/ul/li[4]/'
                                                                           'details/details-dialog/div[3]/form/button')
                        delete_button.click()
            index += 1

        if self.repo_to_delete not in self.final_repo:
                print("'{}' has been deleted from the remote repository...".format(self.repo_to_delete))

    def del_local(self):
        """ This method is used to deleted the local repository. """
        path = 'C:\\Users\\Sinan\\Desktop\\git_repos\\{}'.format('delete')
        # os.system('cmd /c rmdir /s /q {}'.format(path))
        try:
            shutil.rmtree(path)
            if self.repo_to_delete not in os.listdir('C:\\Users\\Sinan\\Desktop\\git_repos'):
                print("Local repository {} deleted from the local repository list...".format(self.repo_to_delete))

        except FileNotFoundError:
            print("Local repository '{}' not found...".format(self.repo_to_delete))


if __name__ == '__main__':
    delete_repo = RepoDeleter('*******', '********')
    delete_repo.login()
    delete_repo.create_repo_list()
    delete_repo.repo_delete(repo_name=input("Which repository you want to delete?\n"))
    delete_repo.del_local()
