import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage


from src.api.crm import User


@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)


@pytest.fixture
def user(setup_db):
    u = User('Patrick', 'Martin', '0668500036', '1 rue du chemin, 75000 Paris')
    u.save()
    return u


def test_first_name(user):
    assert user.first_name == 'Patrick'


def test_full_name(user):
    assert user.full_name == 'Patrick Martin'


def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance['first_name'] == 'Patrick'
    assert user.db_instance['last_name'] == 'Martin'
    assert user.db_instance['phone_number'] == '0668500036'
    assert user.db_instance['address'] == '1 rue du chemin, 75000 Paris'


def test_not_db_instance(setup_db):
    u = User('Maxime', 'Lefranc',  '0123456443', '18 rue Sabaneta, 34000 Montpellier')
    assert u.db_instance is None


def test_check_phone_number(setup_db):
    user_good = User('Jean', 'Smith', '0123456789', '1 rue du chemin, 75015, Paris')
    user_bad = User('Jean', 'Smith', 'abcd', '1 rue du chemin, 75015, Paris')

    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()

    assert str(err.value) == 'Numéro de téléphone abcd invalide.'

    user_good.save(validate_data=True)
    assert user_good.exists() is True


def test_check_names_empty(setup_db):
    user_bad = User('', '', '0123456789', '1 rue du chemin, 75015, Paris')
    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert str(err.value) == 'Le prénom et le nom de famille ne peuvent pas être vides.'


def test_check_names_invalid_characters(setup_db):
    user_bad = User('Patrick#@&', '#@&$$', '0123456789', '1 rue du chemin, 75015, Paris')
    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert str(err.value) == 'Nom "Patrick#@& #@&$$" invalide'


def test_exists(user):
    assert user.exists() is True


def test_not_exists(setup_db):
    u = User('Maxime', 'Lefranc',  '0123456443', '18 rue Sabaneta, 34000 Montpellier')
    assert u.exists() is False


def test_delete(user):
    user.save()
    first = user.delete()
    second = user.delete()
    assert len(first) > 0
    assert isinstance(first, list)
    assert len(second) == 0
    assert isinstance(second, list)


def test_save(setup_db):
    user_test = User('John', 'Smith', '1 rue du chemin, 75015, Paris')
    user_test_dup = User('John', 'Smith', '1 rue du chemin, 75015, Paris')
    first = user_test.save()
    second = user_test_dup.save()
    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1
