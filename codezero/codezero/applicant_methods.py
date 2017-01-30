import random
import string

try:
    from .models import *
except Exception:
    from models import *


def generate_random():
    existing_ids = get_all_applicant_id()
    generated = ''
    generated += random.choice(string.ascii_lowercase)
    generated += random.choice(string.ascii_lowercase)
    generated += random.choice(string.digits)
    generated += random.choice(string.ascii_uppercase)
    generated += random.choice(string.digits)
    if generated in existing_ids:
        generate_random()
    return generated


def get_all_applicant_id():
    id_list = []
    all_id = Applicant.select().where(Applicant.applicant_id.is_null(False))
    for item in all_id:
        id_list.append(item.applicant_id)
    return id_list


def get_applicants_without_id():
    id_list = []
    without_id = Applicant.select().where(Applicant.applicant_id.is_null(True))
    for item in without_id:
        id_list.append(item.id)
    return id_list


# MAIN FUNCTION ##### checks, generates and assignes new applicant_ids


def assign_id():
    applicant_id = get_applicants_without_id()
    # print(len(applicant_id))
    for i in range(len(applicant_id)):
        new_id = generate_random()
        query = Applicant.update(applicant_id=new_id).where(Applicant.id == applicant_id[i])
        query.execute()
    print("done")


def assign_school():
    query = Applicant.\
        select(Applicant.id.alias('applicant_id'), School.id.alias('school_id')).\
        join(City, on=City.city_name == Applicant.city).join(School).naive()
    for item in query:
        # print(item.applicant_id,item.school_id)
        Applicant.update(school=item.school_id).where(
            (Applicant.id == item.applicant_id) & (Applicant.school.is_null(True))).execute()


def display_all_data():
    applicants = Applicant.select(Applicant.applicant_id, Applicant.name, Applicant.city,
                                  Applicant.status, Applicant.school, School.name.alias("school_name")).\
        join(School).naive()

    for person in applicants:
        print("\nAPPLICANT ID: {}\nNAME: {}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
              .format(person.applicant_id, person.name, person.city, person.status, person.school_name))


def filter_by_status(string):
    applicants = Applicant.select(Applicant.applicant_id, Applicant.name, Applicant.city,
                                  Applicant.status, Applicant.school, School.name.alias("school_name")).\
        join(School).where(Applicant.status == string).naive()

    for person in applicants:
        print("\nAPPLICANT ID: {}\nNAME: {}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
              .format(person.applicant_id, person.name, person.city, person.status, person.school_name))


def filter_by_location(string):
    applicants = Applicant.select(Applicant.applicant_id, Applicant.name, Applicant.city,
                                  Applicant.status, Applicant.school, School.name.alias("school_name")).\
        join(School).where(Applicant.city == string).naive()

    for person in applicants:
        print("\nAPPLICANT ID: {}\nNAME: {}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
              .format(person.applicant_id, person.name, person.city, person.status, person.school_name))


def filter_by_school(string):
    applicants = Applicant.select(Applicant.applicant_id, Applicant.name, Applicant.city,
                                  Applicant.status, Applicant.school, School.name.alias("school_name")).\
        join(School).where(School.name == string).naive()

    for person in applicants:
        print("\nAPPLICANT ID: {}\nNAME: {}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
              .format(person.applicant_id, person.name, person.city, person.status, person.school_name))


# assign_id()
# assign_school()
# display_all_data()
# filter_by_status("approved")
# filter_by_location("Budapest")
# filter_by_school("Budapest")

def get_list():
    assign_id()
    table = Applicant.select(Applicant.applicant_id, Applicant.name, Applicant.city, Applicant.status)
    lista = [("APPLICANT ID", "NAME", "CITY", "STATUS")]
    for item in table:
        lista.append((item.applicant_id, item.name, item.city, item.status))
    return lista














