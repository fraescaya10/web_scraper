import requests
from bs4 import BeautifulSoup


class WhiteoaksfScraper:
    def __init__(self, url):
        self.res = requests.get(url)
        self.soup = BeautifulSoup(self.res.content, 'html.parser')

    def get_manager_job_information(self, role_section):
        manager_job_information = dict()
        job_sections = role_section[0].text.split('\r\n')

        if len(job_sections) == 3:
            manager_job_information['role'] = job_sections[0] + job_sections[1]
            manager_job_information['division'] = job_sections[2]
        else:
            manager_job_information['role'] = job_sections[0]
            manager_job_information['division'] = job_sections[1]

        role_with_department = manager_job_information['role'].split(',')

        if len(role_with_department) == 2:
            manager_job_information['role'] = role_with_department[0]
            manager_job_information['department'] = role_with_department[1]
        else:
            manager_job_information['department'] = 'Not specified'

        return manager_job_information

    def scrap_managers(self):
        manager_list = []
        management_people = self.soup.find(
            'div', {'class': 'team team--management'}).findAll('div', {'class': 'team-member'})

        for manager in management_people:
            person = dict()
            person['image'] = manager.find(
                'div', {'class': 'team-memberPhoto'})["style"][22:-1]
            information_section = manager.find(
                'div', {'class': 'team-memberInfo'})
            role_section = information_section.find('div').findAll('strong')
            person['name'] = information_section.find('h3').text
            person['company'] = 'White Oak'
            person['city'] = role_section[1].text
            person['type'] = 'manager'
            person.update(self.get_manager_job_information(role_section))
            manager_list.append(person)
        return manager_list

    def scrap_employees(self):
        employee_list = []
        employee_people = self.soup.find('div', {'class': 'team-table'}).findAll(
            'div', {'class': 'team-tableRow', 'data-expand': 'employees'})
        for employee in employee_people:
            person = dict()
            role_with_division = employee.find(
                'div', {'class': 'team-tableCol--title'}).text.strip().split(',')
            person['name'] = employee.find(
                'div', {'class': 'team-tableCol--name'}).text.strip()
            person['company'] = 'White Oak'
            person['city'] = employee.find(
                'div', {'class': 'team-tableCol--location'}).text.strip()
            person['role'] = role_with_division[0] if len(
                role_with_division) == 2 else role_with_division[0] + role_with_division[1]
            person['division'] = role_with_division[1].strip() if len(
                role_with_division) == 2 else role_with_division[2].strip()
            person['department'] = employee.find(
                'div', {'class': 'team-tableCol--department'}).text.strip()
            person['type'] = 'employee'
            employee_list.append(person)
        return employee_list
