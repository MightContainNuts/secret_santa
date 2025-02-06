import random
import json
from typing import Tuple
from logger import setup_logger

logger = setup_logger(__name__)


Partner_1 = dict
Partner_2 = dict
FILE = "participants.json"

class SecretSanta:

    def __init__(self, year):
        self.partner_pairs = []
        self.year = str(year)
        self.file = FILE
        self.menu = {
            1: ["Assign Secret Santa", self.create_santa_list],
            2: ["Add Non Partner", self.add_non_partner_to_list],
            3: ["Add new Participant", self.add_new_participant],
            4: ["Print participants", self._print_participants],
            5: ["Exit", exit]
        }
        logger.info(f"Secret Santa for {self.year} started")

    def __enter__(self):
        self.data = self.read_json()
        logger.info(f"Data loaded from {self.file}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.write_json()
        logger.info(f"Data written to {self.file}")
        logger.info(f"Secret Santa for {self.year} ended")


    def read_json(self):
        """read data from json"""
        with open(self.file, "r") as file:
            data = json.load(file)
            logger.info(f"Data read from {self.file}")
        return data

    def write_json(self):
        """write data to json"""
        with open(FILE, "w") as file:
            json.dump(self.data, file, indent=4)
            logger.info(f"Data written to {self.file}")

    def assign_secret_santa(self,partner_1:Partner_1)->Tuple[Partner_1,Partner_2]:
        """randomly assign secret santa to each participant"""
        potential_partners = self._create_potential_partners(partner_1)
        partner_2 = random.choice(potential_partners)
        logger.info(f"{partner_1} secret santa is {partner_2}")
        self.data[partner_1][self.year] = partner_2
        try:
            self.write_json()
        except Exception as e:
            logger.error(f"Error writing to {self.file}")
            print(e)
        return partner_1, partner_2

    def create_santa_list(self):
        for participant in self.data:
            partner_pair = self.assign_secret_santa(participant)
            self.partner_pairs.append(partner_pair)
            logger.info(f"Secret Santa partner pair creates: {partner_pair}")
        self._print_secret_santa()
        return self.partner_pairs

    def add_non_partner_to_list(self):
        while True:
            participant = input("Enter participant: ")
            if self._check_if_partner_exists(participant):
                non_partner = input("Enter non_partner: ")
                if self._check_if_partner_exists(non_partner):
                    self._append_non_partner(participant, non_partner)
                    break
                else:
                    print(f"{non_partner} does not exist in the data")
                    logger.warning(f"{non_partner} does not exist in the data")
            else:
                print(f"{participant} does not exist in the data")
                logger.warning(f"{participant} does not exist in the data")

    def add_new_participant(self):
        """add new participant to the data"""
        participant = input("Enter participant: ")
        if self._check_if_partner_exists(participant):
            print(f"{participant} already exists in the data")
            logger.warning(f"{participant} already exists in the data")
        else:
            self.data[participant] = {
                "non_partner": []
            }
            self.write_json()
            print(f"{participant} added to the data")

    # private methods
    def _create_potential_partners(self, partner_1:Partner_1)->list[str]:
        """create a list of potential partners for each participant"""
        potential_partners = list(self.data.keys())
        potential_partners.remove(partner_1)
        logger.info(f"Potential partners for {partner_1}: {potential_partners}")

        already_partnered = self.__get_already_partnered()
        potential_partners = list(filter(lambda p: p not in already_partnered,
                                         potential_partners))
        logger.info(f"Potential partners for {partner_1} after removing already partnered: {potential_partners}")

        previous_year_partner = self.__get_previous_year_partner(partner_1)
        if previous_year_partner in potential_partners:
            potential_partners.remove(previous_year_partner)
        logger.info(f"Potential partners for {partner_1} after removing previous year partner: {potential_partners}")

        non_partners = self.__get_non_partners(partner_1)
        if non_partners:
            potential_partners = list(filter(lambda p: p not in non_partners,
                                             potential_partners))
        logger.info(f"Potential partners for {partner_1} after removing non partners: {potential_partners}")
        return potential_partners


    def __get_already_partnered(self)->list:
        return [self.data[participant][self.year]
                             for participant in self.data
                             if self.data[participant].get(self.year)]

    def __get_previous_year_partner(self, partner_1:Partner_1)->str:
        previous_year = str(int(self.year) -1)
        return self.data[partner_1].get(previous_year)

    def __get_non_partners(self, partner_1:Partner_1)->list:
        return self.data[partner_1].get("non_partner", [])

    def _append_non_partner(self, participant:str, non_partner:str):
        """append partner_2 to the non_partner list of partner_1"""
        if 'non_partner' not in self.data[participant]['non_partner']:
            self.data[participant]['non_partner'].append(non_partner)
            self.write_json()
            print(f"{non_partner} added to {participant}'s non partner list")
            logger.info(f"{non_partner} added to {participant}'s non partner list")
        else:
            print(f"{non_partner} already in {participant}'s non partner list")
            logger.warning(f"{non_partner} already in {participant}'s non partner list")

    def _check_if_partner_exists(self, participant:str)->bool:
        """check if partner_1 exists in the data"""
        return participant in self.data


    def _print_secret_santa(self)->None:
        print(f"\n\n🎅🏽: Secret Santa for {self.year}")
        print("="*30)
        for partner_1, partner_2 in self.partner_pairs:
            print(f"🎁: {partner_1}'s secret 🎅  for {self.year} is {partner_2} 🚀")
        print("="*30)
        print("\n\n")

    def _print_menu(self)->None:
        print("\n\n")
        print("="*30)
        print("🎅🏽: Secret Santa Menu")
        print("="*30)
        for key, value in self.menu.items():
            print(f"{key}: {value[0]}")
        print("=" * 30)
        print("\n\n")

    def _print_participants(self)->None:
        print("\n\n")
        print("="*30)
        print("🎅🏽: Participants")
        print("="*30)
        for participant in self.data:
            print(participant)
        print("=" * 30)
        print("\n\n")


    def run(self)->None:
        while True:
            self._print_menu()
            choice = int(input("Enter choice: "))
            func = self.menu.get(choice)[1]
            func()


if __name__ == '__main__':
    with SecretSanta(2025) as santa:
        santa.run()
