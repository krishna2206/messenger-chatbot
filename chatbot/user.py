
import os
import shutil

import config


class User:
    instances = []

    def __init__(self, user_id: str) -> None:
        self.__user_id = user_id
        self.__temp_folder_location = f"{config.TEMP_FOLDER}/user_{user_id}"

        self.__setup_user_space()

    def __setup_user_space(self):
        print(f"Creating space for user {self.__user_id} ...")

        user_already_exists = self.__check_temp_folder()

        if user_already_exists is False:
            self.__create_temp_folder()
            User.instances.append(self.__user_id)
        else:
            print("User space already exists.")
            User.instances.append(self.__user_id)

    # * Check if the user temp folder already exists
    def __check_temp_folder(self):
        user_space_folder = f"user_{self.__user_id}"
        if user_space_folder not in os.listdir(config.TEMP_FOLDER):
            return False
        return True

    def __create_temp_folder(self):
        os.mkdir(self.__temp_folder_location)

    def __delete_temp_folder(self):
        shutil.rmtree(self.__temp_folder_location)

    def __del__(self):
        """
        If the user is the only instance of the class, delete his temp folder,
        otherwise just remove his instance from the list
        """
        if self.__get_user_instances() == 1:
            self.__delete_temp_folder()
            User.instances.remove(self.__user_id)
        else:
            User.instances.remove(self.__user_id)

    def __get_user_instances(self):
        user_instances = 0
        for user_id in User.instances:
            if user_id == self.__user_id:
                user_instances += 1

        return user_instances

    def get_id(self):
        return self.__user_id

    def get_temp_folder(self):
        return self.__temp_folder_location
