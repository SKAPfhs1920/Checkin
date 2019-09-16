class Person:
    uuid = "134872533245-2345-2345-2435-2-45-54"
    name = "Odd Stråbø"
    room = 406
    phone = "0000" # Varsling på tlf. / email
    email = "test@example.com"
    # Koblet opp mot LDAP bruker?
    # App som viser hvor man er forventet å møte når?
    groups = 'backref:Group'

class Group:
    uuid = "123412341341234"
    name = "Teknologi"
    people = [] # List of people

class Location:
    uuid = "3452345-542-234-52344-5-45"
    key = "FBSADF==" # public key
    name = "Konferanserommet"

class Event:
    uuid = "5322345-354-543235-324"
    name = "SKAP Talk"
    group = Group("Alle")
    location = Location("Konferanserommet")
    start = "2019-09-12 08:30"
    end = "2019-09-12 09:00"

class Scan:
    person = Person()
    location = Location()
    time = "2019-09-12 08:27"
