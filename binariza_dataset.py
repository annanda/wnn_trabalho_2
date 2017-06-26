# coding: utf-8

import rows
import calendar
import holidays
from collections import OrderedDict


def get_animal_has_name(row):
    if len(row.name):
        has_name = 1
    else:
        has_name = 0

    return has_name


def get_animal_is_free_day(row):
    week_day = calendar.day_name[row.datetime.weekday()]
    us_holidays = holidays.UnitedStates()
    holiday = row.datetime in us_holidays

    if (week_day == "Sunday" or week_day == "Saturday" or holiday == True):
        free_day = 1
    else:
        free_day = 0

    return free_day


def get_animal_castration_columns(row):
    if row.sexuponoutcome and row.sexuponoutcome != u'Unknown':
        castration = row.sexuponoutcome.split()[0]
    else:
        castration = u'Unknown'

    # Spayed e Neutered são dois nomes para a mesma coisa, por isso viraram 'Castration'
    if (castration == 'Spayed' or castration == 'Neutered'):
        castration = 'Castration'

    columns = OrderedDict({
        'Castration_Unknown': 0,
        'Castration_Intact': 0,
        'Castration_Castration': 0
    })

    columns['Castration_' + castration] = 1

    return columns


def get_animal_age(row):
    if row.ageuponoutcome == '':
        return -1

    how_many, period = row.ageuponoutcome.split()

    how_many = int(how_many)
    # remove plural
    period = period[:-1] if period.endswith('s') else period

    daysInPeriod = {
        'year': 365,
        'month': 31,
        'week': 7,
        'day': 1
    }.get(period)

    return how_many * daysInPeriod


def get_cat_age_group(row):
    age = get_animal_age(row)

    if (age == -1): return 'cat_unknown'
    # ate 1 ano
    if 0 <= age <= 365:
        return "cat_kitten"
    # de 1 a 7 anos
    elif 366 <= age <= 2920:
        return "cat_adult"
    # mais que 7 ano
    elif age > 2920:
        return "cat_senior"


def get_dog_age_group(row):
    age = get_animal_age(row)

    if (age == -1): return 'dog_unknown'
    # ate 1 ano
    if 0 <= age <= 365:
        return "dog_puppy"
    # de 1 a 8 anos
    elif 366 <= age <= 3285:
        return "dog_adult"
    # mais que 8 anos
    elif age > 3285:
        return "dog_aging"


def get_animal_sex_columns(row):
    if row.sexuponoutcome and row.sexuponoutcome != u'Unknown':
        sex = row.sexuponoutcome.split()[1]
    else:
        sex = u'Unknown'

    columns = OrderedDict({
        'Sex_Unknown': 0,
        'Sex_Male': 0,
        'Sex_Female': 0
    })

    columns['Sex_' + sex] = 1

    return columns


def get_cat_breed_columns(row):
    # Perceba que todos com Rex no nome da raça vão ter 'Rex' como 1, não só os que são só 'Rex'
    # Mix foi incluido para facilitar o algoritmo, mas tecnicamente não é uma raça por si só
    know_breeds = [
        "Mix",
        "Domestic Shorthair", "Rex", "Domestic Medium Hair", "Himalayan", "Domestic Longhair", "Munchkin Longhair",
        "Norwegian Forest Cat", "Sphynx", "Cymric", "American Shorthair", "Maine Coon", "Balinese", "Cornish Rex",
        "Japanese Bobtail", "Ragdoll", "Snowshoe", "Manx", "Angora", "Havana Brown", "Tonkinese", "Siamese",
        "Pixiebob Shorthair", "Russian Blue", "Burmese", "Javanese", "Bengal", "Exotic Shorthair", "Turkish Van",
        "British Shorthair", "Ocicat", "Persian", "Abyssinian", "Devon Rex", "Bombay"]
    column_titles = know_breeds

    columns = OrderedDict()
    for title in column_titles:
        columns['breed_' + title.replace(' ', '')] = 1 if title in row.breed else 0

    return columns


def get_dog_breed_columns(row):
    # Alguns vão ter 3 raças porque o nome de uma está incluido no nome de outra
    # Mix foi incluido para facilitar o algoritmo, mas tecnicamente não é uma raça por si só
    know_breeds = [
        "Mix",
        "American Staffordshire Terrier", "English Pointer", "Unknown", "Bedlington Terr", "Smooth Fox Terrier",
        "Basenji", "Black Mouth Cur",
        "Leonberger", "Norwegian Elkhound", "Canaan Dog", "Beauceron", "Schipperke", "American Bulldog",
        "Redbone Hound", "Cane Corso", "Afghan Hound",
        "Cocker Spaniel", "Treeing Tennesse Brindle", "American Pit Bull Terrier", "Patterdale Terr",
        "Queensland Heeler", "Havanese", "Miniature Schnauzer",
        "Spinone Italiano", "English Cocker Spaniel", "English Setter", "Irish Setter", "Australian Cattle Dog",
        "Manchester Terrier", "Yorkshire Terrier",
        "Brittany", "Pharaoh Hound", "Swedish Vallhund", "Otterhound", "Alaskan Husky", "Yorkshire",
        "Parson Russell Terrier", "Saluki",
        "Greater Swiss Mountain Dog", "Shih Tzu", "Greyhound", "Swiss Hound", "Ibizan Hound", "Norwich Terrier",
        "Presa Canario", "Shiba Inu",
        "Flat Coat Retriever", "Airedale Terrier", "Pekingese", "Weimaraner", "Shetland Sheepdog", "Samoyed",
        "Jack Russell Terrier",
        "Glen Of Imaal", "Entlebucher", "Soft Coated Wheaten Terrier", "Standard Poodle", "Landseer", "Great Pyrenees",
        "Carolina Dog",
        "Port Water Dog", "Jindo", "Boston Terrier", "Schnauzer Giant", "Pug", "Belgian Tervuren", "Belgian Malinois",
        "Finnish Spitz", "Irish Terrier",
        "Feist", "Collie Rough", "Welsh Springer Spaniel", "Collie Smooth", "Dalmatian", "Standard Schnauzer",
        "Doberman Pinsch", "Bull Terrier Miniature",
        "St Bernard Rough Coat", "Borzoi", "Staffordshire", "Affenpinscher", "Welsh Terrier", "Norfolk Terrier",
        "Rat Terrier", "Spanish Water Dog", "Border Collie", "Lowchen",
        "West Highland", "American Foxhound", "Labrador Retriever", "German Shepherd", "Bullmastiff",
        "Mexican Hairless", "Podengo Pequeno", "Basset Hound",
        "Australian Terrier", "Field Spaniel", "Pointer", "Dachshund", "Keeshond", "Picardy Sheepdog", "Siberian Husky",
        "Hovawart", "Dogo Argentino",
        "Rhod Ridgeback", "Bichon Frise", "Black", "Kuvasz", "Cairn Terrier", "Vizsla", "Wire Hair Fox Terrier",
        "Dachshund Wirehair", "Irish Wolfhound",
        "Pomeranian", "Toy Fox Terrier", "Bulldog", "American Eskimo", "Italian Greyhound", "Newfoundland",
        "Wirehaired Pointing Griffon", "Boxer",
        "Golden Retriever", "English Foxhound", "Treeing Cur", "Catahoula", "Pbgv", "Chow Chow", "Bloodhound",
        "German Pinscher", "English Shepherd",
        "Australian Kelpie", "Miniature Poodle", "Whippet", "Pembroke Welsh Corgi", "Bruss Griffon", "Harrier",
        "Miniature Pinscher", "Skye Terrier",
        "Anatol Shepherd", "Neapolitan Mastiff", "Chihuahua Shorthair", "Old English Bulldog", "Akita",
        "Bluetick Hound", "English Coonhound", "Boerboel",
        "Lhasa Apso", "Cavalier Span", "Tibetan Spaniel", "Rottweiler", "English Springer Spaniel",
        "Chihuahua Longhair", "Papillon", "Belgian Sheepdog",
        "Plott Hound", "Australian Shepherd", "Japanese Chin", "Beagle", "Tibetan Terrier",
        "Nova Scotia Duck Tolling Retriever", "Bernese Mountain Dog",
        "German Wirehaired Pointer", "Alaskan Malamute", "Spanish Mastiff", "Dogue De Bordeaux", "Scottish Terrier",
        "French Bulldog", "Sealyham Terr", "English Bulldog",
        "Tan Hound", "Border Terrier", "Maltese", "Bearded Collie", "Silky Terrier", "Mastiff", "Bull Terrier",
        "Chinese Crested", "Great Dane", "Dutch Shepherd", "Cardigan Welsh Corgi",
        "German Shorthair Pointer", "Chinese Sharpei", "Blue Lacy", "St Bernard Smooth Coat", "Pit Bull",
        "Treeing Walker Coonhound", "Chesa Bay Retr", "Old English Sheepdog",
        "Toy Poodle", "Dachshund Longhair", "Boykin Span"]
    column_titles = know_breeds

    columns = OrderedDict()
    for title in column_titles:
        columns['breed_' + title.replace(' ', '')] = 1 if title in row.breed else 0

    return columns


def get_cat_color_columns(row):
    know_colors = 'Blue Cream Lilac White Brown Gray Black Tan Flame Orange Buff Apricot Chocolate Yellow Pink Silver'.split()
    know_patterns = 'Tabby Tortie Torbie Point Tiger Agouti Calico Seal Lynx Smoke'.split()
    column_titles = know_colors + know_patterns

    columns = OrderedDict()
    for title in column_titles:
        columns['color_' + title] = 1 if title in row.color else 0

    return columns


def get_dog_color_columns(row):
    know_colors = 'Pink Ruddy Fawn Liver Smoke Orange Apricot Yellow White Brown Silver Black Cream Gold Grey Red Blue Buff Tan Chocolate Gray'.split()
    know_patterns = 'Tabby Merle Brindle Sable Tiger Tick'.split()
    column_titles = know_colors + know_patterns

    columns = OrderedDict()
    for title in column_titles:
        columns['color_' + title] = 1 if title in row.color else 0

    return columns


def get_cat_age_columns(row):
    groups = OrderedDict({
        'cat_kitten': 0,
        'cat_adult': 0,
        'cat_senior': 0,
        'cat_unknown': 0
    })

    groups[get_cat_age_group(row)] = 1

    return groups


def get_dog_age_columns(row):
    groups = OrderedDict({
        'dog_puppy': 0,
        'dog_adult': 0,
        'dog_aging': 0,
        'dog_unknown': 0
    })

    groups[get_dog_age_group(row)] = 1

    return groups


def get_animal_outcome(row):
    classifier = {
        'Return_to_owner': 0,
        'Euthanasia': 1,
        'Adoption': 2,
        'Transfer': 3,
        'Died': 4
    }

    return classifier[row.outcometype]


# Columns in train.csv
# AnimalID,Name,DateTime,OutcomeType,OutcomeSubtype,AnimalType,SexuponOutcome,AgeuponOutcome,Breed,Color

table_from = rows.import_from_csv("dataset/train.csv")

new_cat_rows = []
new_dog_rows = []
for row in table_from:
    new_row = OrderedDict()

    # AnimalID: não deve ser importante

    # Name: só interessa se tem ou não nome, não que nome é
    new_row['has_name'] = get_animal_has_name(row)

    # DateTime: só interessa se é feriado ou não, não qual data especifica é
    new_row['is_free_day'] = get_animal_is_free_day(row)

    # OutcomeType é o que queremos prever
    # new_row['outcome_text'] = row.outcometype

    # OutcomeSubtype: não disponivel no conjunto de teste, nem é pedido que seja previsto
    # AnimalType: Vamos criar tabelas separadas para cada tipo de animal

    # SexuponOutcome: separamos em sexo e castração. Criamos um coluna por tipo de cada
    # new_row['sex'] = row.sexuponoutcome
    new_row.update(get_animal_castration_columns(row))
    new_row.update(get_animal_sex_columns(row))

    ### Essas dependem de ser gato ou cachorro

    # AgeuponOutcome: separamos em grupos de idade e criamos uma coluna para cada
    # new_row['age'] = row.ageuponoutcome

    # Breed: Uma coluna para cada
    # new_row['breed'] = row.breed

    # Color: uma coluna para cada cor e padrão
    # new_row['color'] = row.color

    if row.animaltype == 'Cat':
        new_row.update(get_cat_age_columns(row))
        new_row.update(get_cat_breed_columns(row))
        new_row.update(get_cat_color_columns(row))

        new_row['outcome'] = get_animal_outcome(row)

        new_cat_rows.append(new_row)

    if row.animaltype == 'Dog':
        new_row.update(get_dog_age_columns(row))
        # Demora muito
        new_row.update(get_dog_breed_columns(row))
        new_row.update(get_dog_color_columns(row))

        new_row['outcome'] = get_animal_outcome(row)

        new_dog_rows.append(new_row)

new_fields = [(key, rows.fields.IntegerField) for key in new_cat_rows[0].keys()]
table_to = rows.Table(fields=OrderedDict(new_fields))
for row in new_cat_rows:
    table_to.append(row)

rows.export_to_csv(table_to, "retina_cat_train.csv")

new_fields = [(key, rows.fields.IntegerField) for key in new_dog_rows[0].keys()]
table_to = rows.Table(fields=OrderedDict(new_fields))
for row in new_dog_rows:
    table_to.append(row)

rows.export_to_csv(table_to, "retina_dog_train.csv")

##################
# Limpando dados de teste
##################


table_from = rows.import_from_csv("dataset/test.csv")

new_cat_rows = []
new_dog_rows = []
for row in table_from:
    new_row = OrderedDict()

    # AnimalID: importante no teste para que a gente possa juntar os dois datasets (gatos e cachorros) novamente
    new_row['id'] = row.id

    # Name: só interessa se tem ou não nome, não que nome é
    new_row['has_name'] = get_animal_has_name(row)

    # DateTime: só interessa se é feriado ou não, não qual data especifica é
    new_row['is_free_day'] = get_animal_is_free_day(row)

    # OutcomeType é o que queremos prever
    # OutcomeSubtype: não disponivel no conjunto de teste, nem é pedido que seja previsto
    # AnimalType: Vamos criar tabelas separadas para cada tipo de animal

    # SexuponOutcome: separamos em sexo e castração. Criamos um coluna por tipo de cada
    # new_row['sex'] = row.sexuponoutcome
    new_row.update(get_animal_castration_columns(row))
    new_row.update(get_animal_sex_columns(row))

    ### Essas dependem de ser gato ou cachorro

    # AgeuponOutcome: separamos em grupos de idade e criamos uma coluna para cada
    # new_row['age'] = row.ageuponoutcome

    # Breed: Uma coluna para cada
    # new_row['breed'] = row.breed

    # Color: uma coluna para cada cor e padrão
    # new_row['color'] = row.color

    if row.animaltype == 'Cat':
        new_row.update(get_cat_age_columns(row))
        new_row.update(get_cat_breed_columns(row))
        new_row.update(get_cat_color_columns(row))

        new_cat_rows.append(new_row)

    if row.animaltype == 'Dog':
        new_row.update(get_dog_age_columns(row))
        # Demora muito
        new_row.update(get_dog_breed_columns(row))
        new_row.update(get_dog_color_columns(row))

        new_dog_rows.append(new_row)

new_fields = [(key, rows.fields.IntegerField) for key in new_cat_rows[0].keys()]
table_to = rows.Table(fields=OrderedDict(new_fields))
for row in new_cat_rows:
    table_to.append(row)

rows.export_to_csv(table_to, "retina_cat_test.csv")

new_fields = [(key, rows.fields.IntegerField) for key in new_dog_rows[0].keys()]
table_to = rows.Table(fields=OrderedDict(new_fields))
for row in new_dog_rows:
    table_to.append(row)

rows.export_to_csv(table_to, "retina_dog_test.csv")